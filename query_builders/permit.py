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
    permitID = form.get("permitID")

    if(len(permitID) < 10): return None

    return f"""
            START TRANSACTION;         
            DELETE from Permit WHERE PermitID = '{permitID}';
            COMMIT;
            """

def permit_add(form):
    passportID = form.get("passportID")
    permitID = form.get("permitID")
    applicationID = form.get("applicationID")  
    issueDate = form.get("issueDate")
    expiryDate = form.get("expiryDate")

    if(len(passportID) < 8): return None
    if(len(permitID) < 10): return None
    if(not applicationID): return None 
    if(not issueDate): return None
    if(not expiryDate): return None

    return f"""
            START TRANSACTION;
            INSERT INTO Permit (PassportID, PermitID, IssueDate, ExpiryDate, ApplicationID)
            VALUES ('{passportID}', '{permitID}', '{issueDate}', '{expiryDate}', {applicationID});
            COMMIT;
            """