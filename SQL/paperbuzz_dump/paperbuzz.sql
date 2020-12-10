CREATE DATABASE paperbuzzeventdata;
USE paperbuzzeventdata;

CREATE TABLE `event_data_json` (
  `json` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `insert_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=71362733 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
