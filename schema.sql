DROP DATABASE testdb; -- Only for testing to avoid database already exists error
CREATE DATABASE testdb;
USE testdb;

CREATE TABLE Student (
	studentID INT, 
	name VARCHAR(50), 
	age INT, 
	PRIMARY KEY(studentID));