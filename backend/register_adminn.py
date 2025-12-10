# register_admin.py

import requests
import json

# --- Configuration for your new admin user ---
# IMPORTANT: Change these values!

# 1. Choose a unique username for your admin
ADMIN_USERNAME = "mahesh" # e.g., "building_A_admin" or "mahesh_super_admin"

# 2. Choose a strong password for this admin user. REMEMBER THIS!
ADMIN_PASSWORD = "1234" # e.g., "SecurePass123!"

# 3. Define the role for this user.
#    - 'super_admin': (Future) Can manage everything across all buildings.
#    - 'admin': Can manage users and view/manage visitors for their specific building_id.
#    - 'guard': Can only check-in/check-out visitors for their specific building_id.
ADMIN_ROLE = "admin" # You can start with 'admin' or 'super_admin'

# 4. IMPORTANT: Replace '1' with an actual building_id from your 'buildings' table.
#    To find valid IDs: Open MySQL Workbench, connect to 'visitor_entry_db', and run 'SELECT * FROM buildings;'.
#    Use the 'building_id' from the row you want this admin to manage.
ADMIN_BUILDING_ID = 1 # Example: If 'Main Campus Hostel' has building_id 1, use 1.

# Backend API endpoint for registration
REGISTER_URL = "http://127.0.0.1:5000/register"

def register_admin_user():
    """Sends a POST request to register a new admin user."""
    payload = {
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD,
        "user_role": ADMIN_ROLE,
        "building_id": ADMIN_BUILDING_ID
    }

    print(f"Attempting to register user: {ADMIN_USERNAME} for Building ID: {ADMIN_BUILDING_ID} with role: {ADMIN_ROLE}")
    print(f"Sending request to: {REGISTER_URL}")

    try:
        response = requests.post(REGISTER_URL, json=payload)
        response_data = response.json()

        if response.status_code == 201:
            print(f"SUCCESS: {response_data.get('message')}. User ID: {response_data.get('user_id')}")
        elif response.status_code == 409:
            print(f"WARNING: {response_data.get('message')}. User '{ADMIN_USERNAME}' probably already exists.")
        else:
            print(f"ERROR: Failed to register user. Status Code: {response.status_code}, Message: {response_data.get('message', 'No message provided')}")
            if 'error' in response_data:
                print(f"Detailed Error: {response_data['error']}")
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the Flask backend. Is it running on http://127.0.0.1:5000?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    register_admin_user()