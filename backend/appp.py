# backend/app.py

from flask import Flask, request, jsonify, g
from flask_cors import CORS
import mysql.connector
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
import jwt
import os
import functools # Crucial for fixing the AssertionError

app = Flask(__name__)
CORS(app)

# --- Database Configuration ---
# IMPORTANT: These credentials should match your MySQL setup.
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'M@yu292407',
    'database': 'visitor_entry_db'
}

# --- Flask App Configuration ---
# Generate a strong, random secret key for JWT in production!
# For development, this is fine, but CHANGE IT for deployment.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_super_secret_jwt_key_please_change_this_in_production_12345')

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

def get_db_connection():
    """Establishes and returns a new database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

# --- JWT Authentication Decorator ---
def token_required(f):
    """
    Decorator to ensure a valid JWT is present in the request header
    and to extract user information from it.
    """
    @functools.wraps(f) # This line fixes the "AssertionError: View function mapping is overwriting"
    def decorated(*args, **kwargs):
        token = None
        # JWT is typically sent in the Authorization header as "Bearer <token>"
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401 # Unauthorized

        try:
            # Decode the token using the secret key
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # Store user info in Flask's global request context 'g'
            g.current_user = data
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid!"}), 401
        except Exception as e:
            print(f"Token error: {e}")
            return jsonify({"message": "An error occurred during token validation."}), 500
        
        # If token is valid, proceed to the original route function
        return f(*args, **kwargs)
    return decorated


# --- API Endpoints ---

@app.route('/register', methods=['POST'])
def register_user():
    """
    Registers a new user (admin/guard) for a specific building.
    Requires: username, password, user_role, building_id.
    """
    data = request.json
    if not data:
        return jsonify({"message": "No data provided"}), 400

    username = data.get('username')
    password = data.get('password')
    user_role = data.get('user_role')
    building_id = data.get('building_id')

    if not all([username, password, user_role, building_id]):
        return jsonify({"message": "Missing required fields"}), 400
    
    # Validate role
    if user_role not in ['super_admin', 'admin', 'guard']:
        return jsonify({"message": "Invalid user role"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor()
    try:
        # Check if username already exists
        cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({"message": "Username already exists"}), 409 # Conflict

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert new user
        sql = "INSERT INTO users (username, password_hash, user_role, building_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (username, hashed_password, user_role, building_id))
        conn.commit()
        return jsonify({"message": "User registered successfully", "user_id": cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Error registering user: {err}")
        return jsonify({"message": "Error registering user", "error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login_user():
    """
    Authenticates a user and returns a JWT.
    Requires: username, password.
    """
    data = request.json
    if not data:
        return jsonify({"message": "No data provided"}), 400

    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({"message": "Missing username or password"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        # Fetch user by username
        cursor.execute("SELECT user_id, username, password_hash, user_role, building_id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"message": "Invalid credentials"}), 401 # Unauthorized

        # Check password
        if bcrypt.check_password_hash(user['password_hash'], password):
            # Generate JWT
            token_payload = {
                'user_id': user['user_id'],
                'username': user['username'],
                'user_role': user['user_role'],
                'building_id': user['building_id'],
                'exp': datetime.utcnow() + timedelta(hours=24) # Token expires in 24 hours
            }
            token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm="HS256")
            
            return jsonify({
                "message": "Login successful",
                "token": token,
                "user": {
                    "user_id": user['user_id'],
                    "username": user['username'],
                    "user_role": user['user_role'],
                    "building_id": user['building_id']
                }
            }), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    except mysql.connector.Error as err:
        print(f"Error logging in user: {err}")
        return jsonify({"message": "Error logging in", "error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/buildings', methods=['GET', 'POST']) # Added 'POST' method for building registration
def buildings_management():
    """
    Handles fetching all building names and IDs (GET)
    and registering new buildings (POST).
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute("SELECT building_id, building_name FROM buildings ORDER BY building_name")
            buildings = cursor.fetchall()
            return jsonify(buildings), 200
        
        elif request.method == 'POST':
            data = request.json
            if not data:
                return jsonify({"message": "No data provided"}), 400
            
            building_name = data.get('building_name')
            building_address = data.get('building_address', '') # Optional address

            if not building_name:
                return jsonify({"message": "Building name is required"}), 400
            
            # Check if building name already exists
            cursor.execute("SELECT building_id FROM buildings WHERE building_name = %s", (building_name,))
            if cursor.fetchone():
                return jsonify({"message": "Building name already exists"}), 409 # Conflict

            sql = "INSERT INTO buildings (building_name, building_address) VALUES (%s, %s)"
            cursor.execute(sql, (building_name, building_address))
            conn.commit()
            return jsonify({"message": "Building registered successfully", "building_id": cursor.lastrowid}), 201

    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Error managing buildings: {err}")
        return jsonify({"message": "Error managing buildings", "error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/visitor', methods=['POST'])
@token_required
def add_visitor():
    """
    Adds a new visitor entry to the database, linked to the user's building.
    Requires: name, room_number, purpose, visitor_mobile, room_owner_mobile, photo_url.
    Building ID is taken from the authenticated user's token.
    """
    data = request.json
    if not data:
        return jsonify({"message": "No data provided"}), 400

    building_id = g.current_user.get('building_id')
    if not building_id:
        return jsonify({"message": "User not associated with a building."}), 403

    name = data.get('name')
    room_number = data.get('room_number')
    purpose = data.get('purpose')
    visitor_mobile = data.get('visitor_mobile')
    room_owner_mobile = data.get('room_owner_mobile')
    
    photo_url = data.get('photo_url', 'https://placehold.co/150x150/cccccc/000000?text=No+Image')

    if not all([name, room_number, purpose, visitor_mobile, room_owner_mobile]):
        return jsonify({"message": "Missing required fields"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor()
    try:
        sql = """
        INSERT INTO visitors (name, room_number, purpose, visitor_mobile, room_owner_mobile, photo_url, entry_time, status, building_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        entry_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(sql, (name, room_number, purpose, visitor_mobile, room_owner_mobile, photo_url, entry_time, 'IN', building_id))
        conn.commit()
        return jsonify({"message": "Visitor added successfully", "visitor_id": cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Error adding visitor: {err}")
        return jsonify({"message": "Error adding visitor", "error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/visitors', methods=['GET'])
@token_required
def get_visitors():
    """
    Fetches visitor entries filtered by the logged-in user's building ID.
    """
    building_id = g.current_user.get('building_id')
    user_role = g.current_user.get('user_role')

    conn = get_db_connection()
    if conn is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        sql = """
        SELECT v.id, v.name, v.room_number, v.purpose, v.visitor_mobile, v.room_owner_mobile,
               v.photo_url, v.entry_time, v.exit_time, v.status, b.building_name
        FROM visitors v
        JOIN buildings b ON v.building_id = b.building_id
        WHERE v.building_id = %s
        ORDER BY v.entry_time DESC
        """
        cursor.execute(sql, (building_id,))
        visitors = cursor.fetchall()

        for visitor in visitors:
            if visitor['entry_time']:
                visitor['entry_time'] = visitor['entry_time'].strftime('%Y-%m-%d %H:%M:%S')
            if visitor['exit_time']:
                visitor['exit_time'] = visitor['exit_time'].strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify(visitors), 200
    except mysql.connector.Error as err:
        print(f"Error fetching visitors: {err}")
        return jsonify({"message": "Error fetching visitors", "error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/visitor/<int:visitor_id>/checkout', methods=['PUT'])
@token_required
def checkout_visitor(visitor_id):
    """
    Updates a visitor's status to 'OUT' and sets their exit_time,
    only if the visitor belongs to the user's building.
    """
    building_id = g.current_user.get('building_id')
    if not building_id:
        return jsonify({"message": "User not associated with a building."}), 403

    conn = get_db_connection()
    if conn is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor()
    try:
        sql = """
        UPDATE visitors
        SET status = 'OUT', exit_time = %s
        WHERE id = %s AND building_id = %s
        """
        exit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(sql, (exit_time, visitor_id, building_id))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Visitor not found or not in your building, or already checked out"}), 404
        return jsonify({"message": f"Visitor {visitor_id} checked out successfully"}), 200
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Error checking out visitor: {err}")
        return jsonify({"message": "Error checking out visitor", "error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)