-- Create the database
CREATE DATABASE IF NOT EXISTS StudentIdentityManagement;
USE StudentIdentityManagement;

-- Create tables
CREATE TABLE IF NOT EXISTS Student (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    EnrollmentDate DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Address (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Street VARCHAR(100) NOT NULL,
    City VARCHAR(50) NOT NULL,
    State VARCHAR(50) NOT NULL,
    Zipcode VARCHAR(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS Department (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Office VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Course (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Code VARCHAR(20) NOT NULL,
    Grade DECIMAL(4, 2),
    DepartmentId INT NOT NULL,
    FOREIGN KEY (DepartmentId) REFERENCES Department(Id)
);

CREATE TABLE IF NOT EXISTS Enrollment (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    EnrollDate DATE NOT NULL,
    StudentId INT NOT NULL,
    CourseId INT NOT NULL,
    FOREIGN KEY (StudentId) REFERENCES Student(Id),
    FOREIGN KEY (CourseId) REFERENCES Course(Id)
);

CREATE TABLE IF NOT EXISTS AuditLog (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    EntityType VARCHAR(50) NOT NULL,
    Operation VARCHAR(50) NOT NULL,
    EntityId INT NOT NULL,
    OperationDate DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS Admin (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Users (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(100) NOT NULL,
    Password_Hash VARCHAR(255) NOT NULL,
    Role ENUM('admin', 'student') NOT NULL
);

-- Insert initial data into tables
INSERT INTO Student (FirstName, LastName, EnrollmentDate) VALUES 
('John', 'Doe', '2023-01-15'), 
('Jane', 'Smith', '2023-05-20');

INSERT INTO Address (Street, City, State, Zipcode) VALUES 
('123 Elm Str', 'Springfield', 'IL', '62701'), 
('456 Oak Str', 'Chicago', 'IL', '60601'),
('123 Main St', 'Springfield', 'IL', '62704'), 
('456 Oak St', 'Madison', 'WI', '53703'),
('789 Pine St', 'Austin', 'TX', '73301'), 
('101 Maple Ave', 'Denver', 'CO', '80202'),
('202 Birch Rd', 'Seattle', 'WA', '98101'), 
('303 Elm Dr', 'Miami', 'FL', '33101'),
('404 Cedar Ln', 'Boston', 'MA', '02108'), 
('505 Walnut St', 'Chicago', 'IL', '60601'),
('606 Ash St', 'Portland', 'OR', '97201'), 
('707 Fir St', 'San Diego', 'CA', '92101');

INSERT INTO Department (Name, Office) VALUES 
('Computer Science', 'Room 101'), 
('Mathematics', 'Room 202'),
('Physics', 'Room 102'), 
('Chemistry', 'Room 103'),
('Biology', 'Room 104'), 
('History', 'Room 105'),
('English', 'Room 106'), 
('Art', 'Room 107'),
('Music', 'Room 108'), 
('Philosophy', 'Room 110');

INSERT INTO Course (Name, Code, Grade, DepartmentId) VALUES 
('Data Structures', 'CS101', NULL, 1), 
('Calculus', 'MATH101', NULL, 2),
('Math 101','MATH101' ,85.50,1),
('Physics 101','PHYS101' ,90.00 ,2),
('Chemistry 101','CHEM101' ,88.00 ,3),
('Biology 101','BIOL101' ,92.00 ,4),
('History 101','HIST101' ,84.00 ,5),
('English 101','ENG101' ,89.50 ,6),
('Art 101','ART101' ,78.00 ,7),
('Music 101','MUS101' ,80.00 ,8),
('Computer Science 101','CS101' ,95.00 ,9),
('Philosophy 101','PHIL101' ,85.00 ,10);

INSERT INTO Enrollment (EnrollDate, StudentId, CourseId) VALUES 
('2023-08-01', 1, 1), 
('2023-08-15', 2, 2),
('2024-09-01',1,1),
('2024-09-02 ',2,2),
('2024-09-03 ',3,3),
('2024-09-04 ',4,4),
('2024-09-05 ',5,5),
('2024-09-06 ',6,6),
('2024-09-07 ',7,7),
('2024-09-08 ',8,8),
('2024-09-09 ',9,9),
('2024-09-10 ',10,10);

INSERT INTO AuditLog (EntityType, Operation, EntityId, OperationDate) VALUES 
('Student','INSERT' ,1,'2023-01-15 10:00:00'),
 ('Course','UPDATE' ,1,'2023-08-01 14:30:00'),
 ('student','CREATE' ,1,'2024-11-01 10:00:00'),
 ('course','UPDATE' ,2,'2024-11-02 11:30:00'),
 ('admin','DELETE' ,3,'2024-11-03 09:15:00');

INSERT INTO Admin (Username, Password) VALUES 
 ('admin','SHA2("adminpassword",256)'), 
 ('admin1','password1'),
 ('admin2','password2'),
 ('admin3','password3'),
 ('admin4','password4'),
 ('admin5','password5'),
 ('admin6','password6'),
 ('admin7','password7'),
 ('admin8','password8'),
 ('admin9','password9'),
 ('admin10','password10');

INSERT INTO Users (Username, Password_Hash, Role) VALUES 
 ('user1','hash1','student'), 
 ('user2','hash2','student'), 
 ('user3','hash3','admin'), 
 ('user4','hash4','student');