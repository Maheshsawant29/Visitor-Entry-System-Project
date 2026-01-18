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
