-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS kb_content;
USE kb_content;

-- Initialize the database schema

CREATE TABLE IF NOT EXISTS kb_chunks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content LONGTEXT NOT NULL,
    url VARCHAR(512) NOT NULL,
    UNIQUE KEY unique_kb_chunk (title, url),
    embedding VECTOR(1536) NOT NULL,
    VECTOR INDEX (embedding)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SHOW TABLES;

SELECT COUNT(*) as total_rows FROM kb_chunks;