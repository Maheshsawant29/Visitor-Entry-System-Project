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
