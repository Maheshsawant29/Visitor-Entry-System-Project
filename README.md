# Visitor Entry Management System (VEMS) 🚀

**Secure Entry, Safe Society: Revolutionizing visitor entry management with technology.**

## 📋 Table of Contents
- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [System Architecture](#-system-architecture)
- [Installation & Setup](#-installation--setup)
- [Database Schema](#-database-schema)
- [Future Scope](#-future-scope)
- [Team Members](#-team-members)
- [References](#-references)

---

## 📖 About the Project

The **Visitor Entry Management System** is a modern, web-based application designed to replace traditional, inefficient paper-based logbooks. 

Manual systems are often slow, insecure, and lack real-time tracking. Our solution streamlines the process by digitizing visitor records, verifying identities via **OTP**, capturing visitor **photos**, and sending real-time **WhatsApp notifications** to room owners. This ensures a safer and more efficient campus/society environment.

---

## ✨ Key Features

*   **🔒 Secure Verification:** Validates visitor mobile numbers via OTP to prevent fake entries.
*   **📸 Image Capture:** Captures visitor photos using the device camera for visual identification.
*   **💬 Real-Time Alerts:** Instantly sends visitor details (Name, Purpose, Photo) to the Room Owner via WhatsApp.
*   **🏢 Multi-Tenant Support:** Capable of managing multiple buildings with specific admin roles.
*   **📊 Admin Dashboard:** A centralized panel to view logs, manage entries, and track visitor history.
*   **☁️ Digital Record Keeping:** All data is securely stored in a MySQL database for easy auditing and retrieval.

---

## 🛠 Technology Stack

### Frontend
*   **HTML5:** Structure of web pages.
*   **CSS3 (Tailwind):** Styling and responsive design.
*   **JavaScript:** Interactivity, camera access, and API communication.

### Backend
*   **Python:** Core logic.
*   **Flask:** Web framework for API endpoints.
*   **Flask-CORS:** Handling Cross-Origin Resource Sharing.
*   **Flask-Bcrypt:** Secure password hashing.
*   **PyJWT:** JSON Web Tokens for secure authentication.

### Database
*   **MySQL:** Relational database management system.

---

## ⚙️ System Architecture

1.  **Registration:** Admin registers a Building and creates User credentials.
2.  **Login:** Security Guard/Admin logs in.
3.  **Entry:** Guard fills visitor details and captures a photo.
4.  **Verification:** Visitor verifies identity via OTP sent to their mobile.
5.  **Notification:** System sends details to the host via WhatsApp.
6.  **Storage:** Data is saved to MySQL.
7.  **Exit:** Guard marks the visitor as "OUT" via the dashboard.

---

## 🚀 Installation & Setup

Follow these steps to run the project locally.

### Prerequisites
*   Python 3.x
*   MySQL Server

### Step 1: Clone the Repository
```bash
git clone [https://github.com/your-username/Visitor-Entry-Management-System.git](https://github.com/your-username/Visitor-Entry-Management-System.git)
cd Visitor-Entry-Management-System

Step 2: Set Up Virtual Environment

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

Step 3: Install Dependencies
pip install Flask Flask-Cors mysql-connector-python Flask-Bcrypt PyJWT requests

Step 4: Configure Database
Open your MySQL Client (e.g., Workbench).

Create the database:

CREATE DATABASE visitor_entry_db;

-- ======================================
-- TABLE: buildings
-- ======================================
CREATE TABLE `buildings` (
  `building_id` INT NOT NULL AUTO_INCREMENT,
  `building_name` VARCHAR(255) NOT NULL,
  `building_address` TEXT,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`building_id`),
  UNIQUE KEY `building_name` (`building_name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ======================================
-- TABLE: users
-- ======================================
CREATE TABLE `users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(100) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `user_role` ENUM('super_admin', 'admin', 'guard') NOT NULL,
  `building_id` INT DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  KEY `building_id` (`building_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`building_id`) REFERENCES `buildings` (`building_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- ======================================
-- TABLE: visitors
-- ======================================
CREATE TABLE `visitors` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `room_number` VARCHAR(50) NOT NULL,
  `purpose` TEXT,
  `visitor_mobile` VARCHAR(20) NOT NULL,
  `room_owner_mobile` VARCHAR(20) NOT NULL,
  `building_id` INT DEFAULT NULL,
  `photo_url` VARCHAR(512) DEFAULT NULL,
  `entry_time` DATETIME NOT NULL,
  `exit_time` DATETIME DEFAULT NULL,
  `status` ENUM('IN', 'OUT') NOT NULL DEFAULT 'IN',
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_building_id` (`building_id`),
  CONSTRAINT `fk_building_id` FOREIGN KEY (`building_id`) REFERENCES `buildings` (`building_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

Update the database credentials in app.py:
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_root_user',
    'password': 'your_password',
    'database': 'visitor_entry_db'
}

Step 5: Run the Application

1)Start the Backend: python app.py
2) Create Admin User: Open a new terminal and run: python register_admin.py
3) Run Frontend: Open index.html (Login Page) using Live Server in VS Code.

🗄 Database Schema
The system uses three main tables:
Buildings: Stores building names and addresses.
Users: Stores admin/guard credentials (hashed passwords) and roles.
Visitors: Stores visitor details, entry/exit times, photo URLs, and status.

🔮 Future Scope
Smart Security (AI/ML)
1)Facial Recognition: Auto-fill details for returning visitors.
2)Anomaly Detection: Flag unusual entry times or prolonged stays.
3)Predictive Analysis: Forecast peak visitor hours for better staff management.

Operational Efficiency
1)Mobile App: Dedicated native app for guards.
2)QR Code Pass: automated QR generation for touchless exit.
3)Pre-Registration: Portal for residents to approve guests in advance.
