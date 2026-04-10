def get_permit_query(form):
    action = form.get("action")
    field = form.get("field")
    dateCondition = form.get("dateCondition")
    date = form.get("dateValue")
    type = form.get("permitType")
    id = form.get("permitID")

    selection = ""
    if action == "Find":
        selection = "*"
    elif action == "Count":
        selection = "COUNT(*)"
    elif action == "Max":
        if field == "issue":
            return f"SELECT * FROM Permit WHERE IssueDate = (SELECT MAX(IssueDate) FROM Permit);"
        elif field == "expiry":
            return f"SELECT * FROM Permit WHERE ExpiryDate = (SELECT MAX(ExpiryDate) FROM Permit);"
        else:
            selection = "*"
    elif action == "Min":
        if field == "issue":
            return f"SELECT * FROM Permit WHERE IssueDate = (SELECT MIN(IssueDate) FROM Permit);"
        elif field == "expiry":
            return f"SELECT * FROM Permit WHERE ExpiryDate = (SELECT MIN(ExpiryDate) FROM Permit);"
        else:
            selection = "*"

    if field == "none":
        return f"SELECT {selection} FROM Permit;"
    elif field == "type":
        if type == "All":
            return f"SELECT {selection} FROM Permit;"
        elif type == "Work Permit":
            return f"SELECT {selection} FROM Permit JOIN WorkPermit ON Permit.PermitID = WorkPermit.PermitID;"
        elif type == "Study Permit":
            return f"SELECT {selection} FROM Permit JOIN StudyPermit ON Permit.PermitID = StudyPermit.PermitID;"
    elif field == "issue":
        if dateCondition == "Before":
            return f"SELECT {selection} FROM Permit WHERE Permit.IssueDate < '{date}';"
        elif dateCondition == "On":
            return f"SELECT {selection} FROM Permit WHERE Permit.IssueDate = '{date}';"
        elif dateCondition == "After":
            return f"SELECT {selection} FROM Permit WHERE Permit.IssueDate > '{date}';"
    elif field == "expiry":
        if dateCondition == "Before":
            return f"SELECT {selection} FROM Permit WHERE Permit.ExpiryDate < '{date}';"
        elif dateCondition == "On":
            return f"SELECT {selection} FROM Permit WHERE Permit.ExpiryDate = '{date}';"
        elif dateCondition == "After":
            return f"SELECT {selection} FROM Permit WHERE Permit.ExpiryDate > '{date}';"
    elif field == "id":
        return f"SELECT {selection} FROM Permit WHERE Permit.PermitID = '{id}';"

def permit_remove(form):
    id = form.get("permitID")

    if(not id): return "--"

    return f"""
            START TRANSACTION;
            DELETE from StudyPermit WHERE PassportID = (SELECT PassportID FROM Permit WHERE PermitID = '{id}');
            DELETE from WorkPermit WHERE PassportID = (SELECT PassportID FROM Permit WHERE PermitID = '{id}');            
            DELETE from Permit WHERE PermitID = '{id}';
            COMMIT;
            """

def permit_add(form):
    passportID = form.get("passportID")
    permitID = form.get("permitID")
    applicationID = form.get("applicationID")  
    issueDate = form.get("issueDate")
    expiryDate = form.get("expiryDate")
    permitType = form.get("permitType")

    if(not passportID): return "--"
    if(not permitID): return "--"
    if(not applicationID): return "--" 
    if(not issueDate): return "--"
    if(not expiryDate): return "--"

    if(permitType == "All"):
        return f"""
                START TRANSACTION;
                INSERT INTO Permit (PassportID, PermitID, IssueDate, ExpiryDate, ApplicationID)
                VALUES ('{passportID}', '{permitID}', '{issueDate}', '{expiryDate}', {applicationID});
                INSERT INTO WorkPermit (PassportID, PermitID)
                VALUES ('{passportID}', '{permitID}');
                INSERT INTO StudyPermit (PassportID, PermitID)
                VALUES ('{passportID}', '{permitID}');
                COMMIT;
                """
    elif(permitType == "Work Permit"):
        return f"""
                START TRANSACTION;
                INSERT INTO Permit (PassportID, PermitID, IssueDate, ExpiryDate, ApplicationID)
                VALUES ('{passportID}', '{permitID}', '{issueDate}', '{expiryDate}', {applicationID});
                INSERT INTO WorkPermit (PassportID, PermitID)
                VALUES ('{passportID}', '{permitID}');
                COMMIT;
                """
    elif(permitType == "Study Permit"):
        return f"""
                START TRANSACTION;
                INSERT INTO Permit (PassportID, PermitID, IssueDate, ExpiryDate, ApplicationID)
                VALUES ('{passportID}', '{permitID}', '{issueDate}', '{expiryDate}', {applicationID});
                INSERT INTO StudyPermit (PassportID, PermitID)
                VALUES ('{passportID}', '{permitID}');
                COMMIT;
                """