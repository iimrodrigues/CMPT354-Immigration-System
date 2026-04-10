    START TRANSACTION;
    -- SELECT * FROM Visa WHERE VisaID = 'VA123456';
    DELETE from TransitVisa WHERE PassportID = (SELECT PassportID FROM Visa WHERE VisaID = 'VA123456');
    DELETE from VisitorVisa WHERE PassportID = (SELECT PassportID FROM Visa WHERE VisaID = 'VA123456');            
    DELETE from Visa WHERE VisaID = 'VA123456';
    -- DELETE FROM SUBMITS WHERE ApplicationID = (SELECT ApplicationID FROM Visa WHERE VisaID = 'VA123456');
    -- DELETE FROM Application WHERE ApplicationID = (SELECT ApplicationID FROM Visa WHERE VisaID = 'VA123456');
    COMMIT;