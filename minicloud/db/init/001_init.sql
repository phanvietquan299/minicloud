CREATE DATABASE IF NOT EXISTS minicloud;
USE minicloud;

CREATE TABLE IF NOT EXISTS notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO notes(title) VALUES ('Hello from MariaDB!');

CREATE DATABASE IF NOT EXISTS studentdb;
USE studentdb;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    fullname VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    major VARCHAR(100) NOT NULL
);

INSERT INTO students (student_id, fullname, dob, major) VALUES
('SV001', 'Nguyen Van An', '2003-01-15', 'Computer Science'),
('SV002', 'Tran Thi Bich', '2003-03-22', 'Information Systems'),
('SV003', 'Le Minh Chau', '2002-11-08', 'Network Engineering');
