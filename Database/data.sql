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

INSERT INTO Visa
(PassportID, VisaID, IssueDate, ExpiryDate, StayStatus, ApplicationID)
VALUES
('AB123456', 'VA123456', '2015-05-10', '2016-05-10', 'Valid', 1),
('CD234567', 'VB234567', '2016-07-28', '2017-07-28', 'Expired', 2),
('EF345678', 'VC345678', '2017-02-15', '2018-02-15', 'Valid', 3),
('GH456789', 'VD456789', '2018-03-01', '2019-03-01', 'Revoked', 4),
('IJ567890', 'VE567890', '2019-11-12', '2020-11-12', 'Valid', 5),
('AB123456', 'VF678901', '2020-01-15', '2021-01-15', 'Expired', 1),
('CD234567', 'VG789012', '2021-03-20', '2022-03-20', 'Expired', 2),
('EF345678', 'VH890123', '2022-06-10', '2023-06-10', 'Valid', 3),
('GH456789', 'VI901234', '2023-02-05', '2024-02-05', 'Valid', 4),
('IJ567890', 'VJ012345', '2024-07-12', '2025-07-12', 'Valid', 5);

INSERT INTO TransitVisa
(PassportID, VisaID)
VALUES
('AB123456', 'VA123456'),
('CD234567', 'VB234567'),
('EF345678', 'VC345678'),
('GH456789', 'VD456789'),
('IJ567890', 'VE567890');

INSERT INTO VisitorVisa
(PassportID, VisaID)
VALUES
('AB123456', 'VF678901'),
('CD234567', 'VG789012'),
('EF345678', 'VH890123'),
('GH456789', 'VI901234'),
('IJ567890', 'VJ012345');

INSERT INTO Permit
(PassportID, PermitID, IssueDate, ExpiryDate, ApplicationID)
VALUES
('AB123456', 'S123456789', '2015-06-01', '2019-06-01', 1),
('CD234567', 'S234567890', '2016-09-01', '2020-09-01', 2),
('EF345678', 'S345678901', '2017-03-01', '2021-03-01', 3),
('GH456789', 'S456789012', '2018-04-01', '2022-04-01', 4),
('IJ567890', 'S567890123', '2019-12-01', '2023-12-01', 5),
('AB123456', 'W678901234', '2020-01-01', '2024-01-01', 1),
('CD234567', 'W789012345', '2021-02-01', '2025-02-01', 2),
('EF345678', 'W890123456', '2022-05-01', '2026-05-01', 3),
('GH456789', 'W901234567', '2023-03-01', '2027-03-01', 4),
('IJ567890', 'W012345678', '2024-08-01', '2028-08-01', 5);

INSERT INTO StudyPermit
(PassportID, PermitID)
VALUES
('AB123456', 'S123456789'),
('CD234567', 'S234567890'),
('EF345678', 'S345678901'),
('GH456789', 'S456789012'),
('IJ567890', 'S567890123');

INSERT INTO WorkPermit
(PassportID, PermitID)
VALUES
('AB123456', 'W678901234'),
('CD234567', 'W789012345'),
('EF345678', 'W890123456'),
('GH456789', 'W901234567'),
('IJ567890', 'W012345678');