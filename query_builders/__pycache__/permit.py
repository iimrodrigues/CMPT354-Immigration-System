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
            return f"SELECT * FROM Permit WHERE IssueDate = (SELECT MAX(IssueDate) FROM Permit);", ()
        elif field == "expiry":
            return f"SELECT * FROM Permit WHERE ExpiryDate = (SELECT MAX(ExpiryDate) FROM Permit);", ()
        else:
            selection = "*"
    elif action == "Min":
        if field == "issue":
            return f"SELECT * FROM Permit WHERE IssueDate = (SELECT MIN(IssueDate) FROM Permit);", ()
        elif field == "expiry":
            return f"SELECT * FROM Permit WHERE ExpiryDate = (SELECT MIN(ExpiryDate) FROM Permit);", ()
        else:
            selection = "*"

    if field == "none":
        return f"SELECT {selection} FROM Permit;", ()
    elif field == "type":
        if type == "All":
            return f"SELECT {selection} FROM Permit;", ()
        elif type == "Work Permit":
            return f"SELECT {selection} FROM Permit JOIN WorkPermit ON Permit.PermitID = WorkPermit.PermitID;", ()
        elif type == "Study Permit":
            return f"SELECT {selection} FROM Permit JOIN StudyPermit ON Permit.PermitID = StudyPermit.PermitID;", ()
    elif field == "issue":
        if dateCondition == "Before":
            return f"SELECT {selection} FROM Permit WHERE Permit.IssueDate < %s;", (date,)
        elif dateCondition == "On":
            return f"SELECT {selection} FROM Permit WHERE Permit.IssueDate = %s;", (date,)
        elif dateCondition == "After":
            return f"SELECT {selection} FROM Permit WHERE Permit.IssueDate > %s;", (date,)
    elif field == "expiry":
        if dateCondition == "Before":
            return f"SELECT {selection} FROM Permit WHERE Permit.ExpiryDate < %s;", (date,)
        elif dateCondition == "On":
            return f"SELECT {selection} FROM Permit WHERE Permit.ExpiryDate = %s;", (date,)
        elif dateCondition == "After":
            return f"SELECT {selection} FROM Permit WHERE Permit.ExpiryDate > %s;", (date,)
    elif field == "id":
        return f"SELECT {selection} FROM Permit WHERE Permit.PermitID = %s;", (id,)

def get_permit_update_query(form):
    field = form.get("field")
    passport_id = form.get("passportID")
    permit_id = form.get("permitID")
    new_date = form.get("dateUpdateValue")

    # Validate inputs
    if not passport_id or not permit_id or field == "none":
        return None, None, "Please fill in all fields."

    if not new_date:
        return None, None, "Please select a new date."

    if field not in ["StartDate", "ExpiryDate"]:
        return None, None, "Invalid field selected."

    # Safe SQL (field is controlled, values are parameterized)
    query = f"""
        UPDATE Permit
        SET {field} = %s
        WHERE PassportID = %s AND PermitID = %s
    """

    params = (new_date, passport_id, permit_id)

    return query, params, None