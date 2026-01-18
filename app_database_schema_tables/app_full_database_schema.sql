CREATE DATABASE visitor_entry_db;

-- ======================================
-- TABLE 1: buildings
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
-- TABLE 2: users
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
-- TABLE 3: visitors
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
