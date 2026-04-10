def update_query(form):
    field = form.get("field")
    passport_id = form.get("passportID")
    permit_id = form.get("permitID")
    new_date = form.get("dateUpdateValue")

    # Validate inputs
    if not passport_id or not permit_id or not field or field == "none":
        return None, None, "Please fill in all fields."

    if not new_date:
        return None, None, "Please select a new date."

    # Map allowed fields (prevents SQL injection completely)
    field_map = {
        "StartDate": "StartDate",
        "ExpiryDate": "ExpiryDate"
    }

    if field not in field_map:
        return None, None, "Invalid field selected."

    sql_field = field_map[field]

    query = """
        UPDATE Permit
        SET {} = %s
        WHERE PassportID = %s AND PermitID = %s
    """.format(sql_field)

    params = (new_date, passport_id, permit_id)

    return query, params, None

def permit_remove(form):
    id = form.get("permitID")

    return f"""
            START TRANSACTION;
            DELETE from StudyPermit WHERE PassportID = (SELECT PassportID FROM Permit WHERE PermitID = '{id}');
            DELETE from WorkPermit WHERE PassportID = (SELECT PassportID FROM Permit WHERE PermitID = '{id}');            
            DELETE from Permit WHERE PermitID = '{id}';
            COMMIT;
            """