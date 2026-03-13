INSERT INTO NonCitizen
(PassportID, FirstName, MiddleName, LastName, HasCriminalRecord, DateOfBirth, CountryOfOrigin, StreetName, City, Province, PostalCode)
VALUES
('AB123456', 'Liam', 'James', 'Smith', FALSE, '1992-04-15', 'USA', '123 Maple Street', 'Vancouver', 'British Columbia', 'V5K 0A1'),
('CD234567', 'Sophia', 'Marie', 'Nguyen', FALSE, '1988-11-22', 'Vietnam', '456 Oak Avenue', 'Toronto', 'Ontario', 'M4B 1B3'),
('EF345678', 'Carlos', 'Miguel', 'Lopez', TRUE, '1990-07-09', 'Mexico', '789 Pine Road', 'Calgary', 'Alberta', 'T2P 1J9'),
('GH456789', 'Aisha', 'Noor', 'Khan', FALSE, '1995-01-30', 'Pakistan', '321 Birch Lane', 'Montreal', 'Quebec', 'H3Z 2Y7'),
('IJ567890', 'Elena', 'Sofia', 'Rossi', FALSE, '1985-06-18', 'Italy', '654 Cedar Drive', 'Halifax', 'Nova Scotia', 'B3H 1A4');

INSERT INTO BorderCrossing
(Date, Time, City, Province, PostalCode, EntryOrExit)
VALUES
('2015-05-12', '08:15:00', 'Vancouver', 'British Columbia', 'V6B 2T4', 'Entry'),
('2016-08-03', '09:30:00', 'Toronto', 'Ontario', 'M5H 3K7', 'Exit'),
('2017-02-20', '14:45:00', 'Calgary', 'Alberta', 'T3J 4S8', 'Entry'),
('2018-03-05', '11:20:00', 'Montreal', 'Quebec', 'H2X 1Y2', 'Exit'),
('2019-11-18', '16:05:00', 'Halifax', 'Nova Scotia', 'B4C 1L9', 'Entry');

INSERT INTO Application
(ApplicationID, Status)
VALUES
(1, 'Submitted'),
(2, 'In Progress'),
(3, 'Approved'),
(4, 'Rejected'),
(5, 'In Progress');

INSERT INTO SupportingDocuments
(ApplicationID, DocumentNumber)
VALUES
(1, 101),
(1, 102),
(2, 201),
(3, 301),
(4, 401);

INSERT INTO CROSSES
(CrossingDate, CrossingTime, PassportID)
VALUES
('2015-05-12', '08:15:00', 'AB123456'),
('2016-08-03', '09:30:00', 'CD234567'),
('2017-02-20', '14:45:00', 'EF345678'),
('2018-03-05', '11:20:00', 'GH456789'),
('2019-11-18', '16:05:00', 'IJ567890');

INSERT INTO SUBMITS
(ApplicationID, PassportID, SubmissionDate)
VALUES
(1, 'AB123456', '2015-05-01'),
(2, 'CD234567', '2016-07-25'),  
(3, 'EF345678', '2017-02-10'),  
(4, 'GH456789', '2018-02-28'),  
(5, 'IJ567890', '2019-11-10');  