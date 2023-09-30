-- ------------------------------------------------------------
-- Database Setup Script for MySQL Database:
-- Create database, user and grant priviledges.
-- ------------------------------------------------------------

DROP DATABASE IF EXISTS pffad_db;
CREATE DATABASE IF NOT EXISTS pffad_db;
CREATE USER IF NOT EXISTS 'pffad_root'@'localhost' IDENTIFIED BY 'pffad_root_pwd';
GRANT ALL PRIVILEGES ON `pffad_db`.* TO 'pffad_root'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'pffad_root'@'localhost';
FLUSH PRIVILEGES;