def get_application_query(form):
    action = form.get("action")
    field = form.get("appField")
    appID = form.get("appID")
    appStatus = form.get("appStatus")
    countDocsCondition = form.get("countDocsCondition")
    countDocs = form.get("countDocsValue")

    print(field)

    selection = ""
    if action == "Find":
        selection = "*"
    elif action == "Count":
        selection = "COUNT(*)"
    
    if field == "none":
        return f"SELECT {selection} FROM Application;", ()
    elif field == "id":
        return f"SELECT {selection} FROM Application WHERE Application.ApplicationID = %s;", (appID,)
    elif field == "status":
        return f"SELECT {selection} FROM Application WHERE Application.Status = %s;", (appStatus,)
    elif field == "countDocs":
        if countDocsCondition == "lessThan":
            if selection == "*":
                return f"""SELECT Application.*, COUNT(SupportingDocuments.ApplicationID) AS DocumentCount
                        FROM Application 
                        LEFT JOIN SupportingDocuments ON SupportingDocuments.ApplicationID = Application.ApplicationID
                        GROUP BY Application.ApplicationID
                        HAVING COUNT(SupportingDocuments.ApplicationID) < %s;""", (countDocs,)
            elif selection == "COUNT(*)":
                return f"""SELECT COUNT(*)
                        FROM (
                            SELECT Application.ApplicationID
                            FROM Application 
                            LEFT JOIN SupportingDocuments ON SupportingDocuments.ApplicationID = Application.ApplicationID
                            GROUP BY Application.ApplicationID
                            HAVING COUNT(SupportingDocuments.ApplicationID) < %s
                        ) AS Subquery;""", (countDocs,)
        
        elif countDocsCondition == "equal":
            if selection == "*":
                return f"""SELECT Application.*, COUNT(SupportingDocuments.ApplicationID) AS DocumentCount
                        FROM Application 
                        LEFT JOIN SupportingDocuments ON SupportingDocuments.ApplicationID = Application.ApplicationID
                        GROUP BY Application.ApplicationID
                        HAVING COUNT(SupportingDocuments.ApplicationID) = %s;""", (countDocs,)
            elif selection == "COUNT(*)":
                return f"""SELECT COUNT(*)
                        FROM (
                            SELECT Application.ApplicationID
                            FROM Application 
                            LEFT JOIN SupportingDocuments ON SupportingDocuments.ApplicationID = Application.ApplicationID
                            GROUP BY Application.ApplicationID
                            HAVING COUNT(SupportingDocuments.ApplicationID) = %s
                        ) AS Subquery;""", (countDocs,)
        
        elif countDocsCondition == "greaterThan":
            if selection == "*":
                return f"""SELECT Application.*, COUNT(SupportingDocuments.ApplicationID) AS DocumentCount
                        FROM Application 
                        LEFT JOIN SupportingDocuments ON SupportingDocuments.ApplicationID = Application.ApplicationID
                        GROUP BY Application.ApplicationID
                        HAVING COUNT(SupportingDocuments.ApplicationID) > %s;""", (countDocs,)
            elif selection == "COUNT(*)":
                return f"""SELECT COUNT(*)
                        FROM (
                            SELECT Application.ApplicationID
                            FROM Application 
                            LEFT JOIN SupportingDocuments ON SupportingDocuments.ApplicationID = Application.ApplicationID
                            GROUP BY Application.ApplicationID
                            HAVING COUNT(SupportingDocuments.ApplicationID) > %s
                        ) AS Subquery;""", (countDocs,)
            
def update_query(form):
    application_id = form.get("applicationID")
    status_value = form.get("statusValue")

    if not application_id or not status_value:
        return None, None, "Please fill in all fields."

    query = """
        UPDATE Application
        SET Status = %s
        WHERE ApplicationID = %s
    """

    params = (status_value, application_id)

    return query, params, None