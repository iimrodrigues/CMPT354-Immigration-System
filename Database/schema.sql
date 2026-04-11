CREATE DATABASE immigration_db;
USE immigration_db;

CREATE TABLE NonCitizen (
	PassportID CHAR(8),
    FirstName VARCHAR(25),
    MiddleName VARCHAR(25),
    LastName VARCHAR(25),
    HasCriminalRecord BOOLEAN,
    DateOfBirth DATE,
    CountryOfOrigin VARCHAR(25),
    StreetName VARCHAR(25),
    City VARCHAR(25),
    Province VARCHAR(25),
    PostalCode CHAR(7),
    PRIMARY KEY(PassportID));

CREATE TABLE BorderCrossing (
	Date DATE,
    Time TIME,
    City VARCHAR(25),
    Province VARCHAR(25),
    PostalCode CHAR(7),
    EntryOrExit CHAR(5),
    PRIMARY KEY(Date, Time));
    
CREATE TABLE Application (
	ApplicationID INT,
    Status VARCHAR(25),
    PRIMARY KEY(ApplicationID));
    
CREATE TABLE SupportingDocuments (
	ApplicationID INT,
    DocumentNumber INT,
    PRIMARY KEY(ApplicationID, DocumentNumber),
    FOREIGN KEY(ApplicationID) REFERENCES Application(ApplicationID) ON DELETE CASCADE);
    
CREATE TABLE CROSSES (
	CrossingDate DATE,
    CrossingTime TIME,
    PassportID CHAR(8),
    PRIMARY KEY(CrossingDate, CrossingTime, PassportID),
    FOREIGN KEY(CrossingDate, CrossingTime) REFERENCES BorderCrossing(Date, Time) ON DELETE CASCADE,
    FOREIGN KEY(PassportID) REFERENCES NonCitizen(PassportID) ON DELETE CASCADE);
    
CREATE TABLE SUBMITS (
	ApplicationID INT,
    PassportID CHAR(8),
    SubmissionDate DATE,
    PRIMARY KEY(ApplicationID, PassportID),
    FOREIGN KEY(ApplicationID) REFERENCES Application(ApplicationID) ON DELETE CASCADE,
    FOREIGN KEY(PassportID) REFERENCES NonCitizen(PassportID) ON DELETE CASCADE);

CREATE TABLE Visa (
    PassportID CHAR(8),
    VisaID CHAR(8),
    IssueDate DATE,
    ExpiryDate DATE,
    StayStatus VARCHAR(25), 
    ApplicationID INT,
    PRIMARY KEY(PassportID, VisaID),
    FOREIGN KEY(PassportID) REFERENCES NonCitizen(PassportID) ON DELETE CASCADE,
    FOREIGN KEY(ApplicationID) REFERENCES Application(ApplicationID) ON DELETE CASCADE);

CREATE TABLE TransitVisa (
    PassportID CHAR(8),
    VisaID CHAR(8),
    PRIMARY KEY(PassportID, VisaID),
    FOREIGN KEY(PassportID) REFERENCES Visa(PassportID) ON DELETE CASCADE);

CREATE TABLE VisitorVisa (
    PassportID CHAR(8),
    VisaID CHAR(8),
    PRIMARY KEY(PassportID, VisaID),
    FOREIGN KEY(PassportID) REFERENCES Visa(PassportID) ON DELETE CASCADE);

CREATE TABLE Permit (
    PassportID CHAR(8),
    PermitID CHAR(10),
    IssueDate DATE,
    ExpiryDate DATE,
    ApplicationID INT,
    PRIMARY KEY(PassportID, PermitID),
    FOREIGN KEY(PassportID) REFERENCES NonCitizen(PassportID) ON DELETE CASCADE,
    FOREIGN KEY(ApplicationID) REFERENCES Application(ApplicationID) ON DELETE CASCADE);

CREATE TABLE StudyPermit (
    PassportID CHAR(8),
    PermitID CHAR(10),
    PRIMARY KEY(PassportID, PermitID),
    FOREIGN KEY(PassportID) REFERENCES Permit(PassportID) ON DELETE CASCADE);

CREATE TABLE WorkPermit (
    PassportID CHAR(8),
    PermitID CHAR(10),
    PRIMARY KEY(PassportID, PermitID),
    FOREIGN KEY(PassportID) REFERENCES Permit(PassportID) ON DELETE CASCADE);