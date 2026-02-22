CREATE DATABASE IF NOT EXISTS cansatdb;

USE cansatdb;

CREATE TABLE IF NOT EXISTS measurements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    type CHAR(1),
    temperature FLOAT,
    pressure FLOAT,
    altitude FLOAT
);