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
            return f"SELECT * FROM Visa WHERE IssueDate = (SELECT MAX(IssueDate) FROM Visa);"
        elif field == "expiry":
            return f"SELECT * FROM Visa WHERE ExpiryDate = (SELECT MAX(ExpiryDate) FROM Visa);"
        else:
            selection = "*"
    elif action == "Min":
        if field == "issue":
            return f"SELECT * FROM Visa WHERE IssueDate = (SELECT MIN(IssueDate) FROM Visa);"
        elif field == "expiry":
            return f"SELECT * FROM Visa WHERE ExpiryDate = (SELECT MIN(ExpiryDate) FROM Visa);"
        else:
            selection = "*"

    if field == "none":
        return f"SELECT {selection} FROM Visa;"
    elif field == "type":
        if type == "All":
            return f"SELECT {selection} FROM Visa;"
        elif type == "Transit Visa":
            return f"SELECT {selection} FROM Visa JOIN TransitVisa ON Visa.VisaID = TransitVisa.VisaID;"
        elif type == "Visitor Visa":
            return f"SELECT {selection} FROM Visa JOIN VisitorVisa ON Visa.VisaID = VisitorVisa.VisaID;"
    elif field == "issue":
        if dateCondition == "Before":
            return f"SELECT {selection} FROM Visa WHERE Visa.IssueDate < '{date}';"
        elif dateCondition == "On":
            return f"SELECT {selection} FROM Visa WHERE Visa.IssueDate = '{date}';"
        elif dateCondition == "After":
            return f"SELECT {selection} FROM Visa WHERE Visa.IssueDate > '{date}';"
    elif field == "expiry":
        if dateCondition == "Before":
            return f"SELECT {selection} FROM Visa WHERE Visa.ExpiryDate < '{date}';"
        elif dateCondition == "On":
            return f"SELECT {selection} FROM Visa WHERE Visa.ExpiryDate = '{date}';"
        elif dateCondition == "After":
            return f"SELECT {selection} FROM Visa WHERE Visa.ExpiryDate > '{date}';"
    elif field == "id":
        return f"SELECT {selection} FROM Visa WHERE Visa.VisaID = '{id}';"

def get_visa_remove(form):
    id = form.get("visaID")

    return f"""
            START TRANSACTION;
            -- SELECT * FROM Visa WHERE VisaID = '{id}';
            DELETE from TransitVisa WHERE PassportID = (SELECT PassportID FROM Visa WHERE VisaID = '{id}');
            DELETE from VisitorVisa WHERE PassportID = (SELECT PassportID FROM Visa WHERE VisaID = '{id}');            
            DELETE from Visa WHERE VisaID = '{id}';
            -- DELETE FROM SUBMITS WHERE ApplicationID = (SELECT ApplicationID FROM Visa WHERE VisaID = '{id}');
            -- DELETE FROM Application WHERE ApplicationID = (SELECT ApplicationID FROM Visa WHERE VisaID = '{id}');
            COMMIT
            """
