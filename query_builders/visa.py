def update_query(form):
    field = form.get("field")
    passport_id = form.get("passportID")
    visa_id = form.get("visaID")
    date_value = form.get("dateValue")
    stay_value = form.get("stayStatus")

    if not passport_id or not visa_id or not field or field == "none":
        return None, None, "Please fill in all fields."

    field_map = {
        "IssueDate": "IssueDate",
        "ExpiryDate": "ExpiryDate",
        "StayStatus": "StayStatus"
    }

    if field not in field_map:
        return None, None, "Invalid field selected."

    sql_field = field_map[field]

    # Decide value type
    value = date_value if field in ["IssueDate", "ExpiryDate"] else stay_value

    if not value:
        return None, None, "Please provide a value."

    query = f"""
        UPDATE Visa
        SET {sql_field} = %s
        WHERE PassportID = %s AND VisaID = %s
    """

    params = (value, passport_id, visa_id)

    return query, params, None

def get_visa_query(form):
    action = form.get("action")
    field = form.get("field")
    dateCondition = form.get("dateCondition")
    date = form.get("dateValue")
    type = form.get("visaType")
    id = form.get("visaID")

    selection = ""
    if action == "Find":
        selection = "*"
    elif action == "Count":
        selection = "COUNT(*)"
    elif action == "Max":
        if field == "issue":
            return f"SELECT * FROM Visa WHERE IssueDate = (SELECT MAX(IssueDate) FROM Visa);", ()
        elif field == "expiry":
            return f"SELECT * FROM Visa WHERE ExpiryDate = (SELECT MAX(ExpiryDate) FROM Visa);", ()
        else:
            selection = "*"
    elif action == "Min":
        if field == "issue":
            return f"SELECT * FROM Visa WHERE IssueDate = (SELECT MIN(IssueDate) FROM Visa);", ()
        elif field == "expiry":
            return f"SELECT * FROM Visa WHERE ExpiryDate = (SELECT MIN(ExpiryDate) FROM Visa);", ()
        else:
            selection = "*"

    if field == "none":
        return f"SELECT {selection} FROM Visa;", ()
    elif field == "type":
        if type == "All":
            return f"SELECT {selection} FROM Visa;", ()
        elif type == "Transit Visa":
            return f"SELECT {selection} FROM Visa JOIN TransitVisa ON Visa.VisaID = TransitVisa.VisaID;", ()
        elif type == "Visitor Visa":
            return f"SELECT {selection} FROM Visa JOIN VisitorVisa ON Visa.VisaID = VisitorVisa.VisaID;", ()
    elif field == "issue":
        if dateCondition == "Before":
            return f"SELECT {selection} FROM Visa WHERE Visa.IssueDate < %s;", (date,)
        elif dateCondition == "On":
            return f"SELECT {selection} FROM Visa WHERE Visa.IssueDate = %s;", (date,)
        elif dateCondition == "After":
            return f"SELECT {selection} FROM Visa WHERE Visa.IssueDate > %s;", (date,)
    elif field == "expiry":
        if dateCondition == "Before":
            return f"SELECT {selection} FROM Visa WHERE Visa.ExpiryDate < %s;", (date,)
        elif dateCondition == "On":
            return f"SELECT {selection} FROM Visa WHERE Visa.ExpiryDate = %s;", (date,)
        elif dateCondition == "After":
            return f"SELECT {selection} FROM Visa WHERE Visa.ExpiryDate > %s;", (date,)
    elif field == "id":
            return f"SELECT {selection} FROM Visa WHERE Visa.VisaID = %s;", (id,)

def visa_remove(form):
    id = form.get("visaID")

    if(not id): return "--"

    return f"""
            START TRANSACTION;
            DELETE from TransitVisa WHERE PassportID = (SELECT PassportID FROM Visa WHERE VisaID = '{id}');
            DELETE from VisitorVisa WHERE PassportID = (SELECT PassportID FROM Visa WHERE VisaID = '{id}');            
            DELETE from Visa WHERE VisaID = '{id}';
            COMMIT;
            """

def visa_add(form):
    passportID = form.get("passportID")
    visaID = form.get("visaID")
    applicationID = form.get("applicationID")  
    issueDate = form.get("issueDate")
    expiryDate = form.get("expiryDate")
    stayStatus = form.get("stayStatus")
    type = form.get("visaType")

    if(not passportID): return "--"
    if(not visaID): return "--"
    if(not applicationID): return "--"
    if(not issueDate): return "--"
    if(not expiryDate): return "--"

    if(type == "All"):
        return f"""
                START TRANSACTION;
                INSERT INTO Visa (PassportID, VisaID, IssueDate, ExpiryDate, StayStatus, ApplicationID)
                VALUES ('{passportID}', '{visaID}', '{issueDate}', '{expiryDate}', '{stayStatus}', {applicationID});
                COMMIT;
                """
    elif(type == "Transit Visa"):
        return f"""
                START TRANSACTION;
                INSERT INTO Visa (PassportID, VisaID, IssueDate, ExpiryDate, StayStatus, ApplicationID)
                VALUES ('{passportID}', '{visaID}', '{issueDate}', '{expiryDate}', '{stayStatus}', {applicationID});
                COMMIT;
                """
    elif(type == "Visitor Visa"):
        return f"""
                START TRANSACTION;
                INSERT INTO Visa (PassportID, VisaID, IssueDate, ExpiryDate, StayStatus, ApplicationID)
                VALUES ('{passportID}', '{visaID}', '{issueDate}', '{expiryDate}', '{stayStatus}', {applicationID});
                COMMIT;
                """