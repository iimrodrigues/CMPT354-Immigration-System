def update_query(form):
    field = form.get("field")
    passport_id = form.get("passportID")
    value = form.get("value")

    if not passport_id or not field or field == "none":
        return None, None, "Please fill in all fields."

    field_map = {
        "FirstName": "FirstName",
        "MiddleName": "MiddleName",
        "LastName": "LastName",
        "HasCriminalRecord": "HasCriminalRecord",
        "CountryOfOrigin": "CountryOfOrigin",
        "StreetName": "StreetName",
        "City": "City",
        "Province": "Province",
        "PostalCode": "PostalCode"
    }

    if field not in field_map:
        return None, None, "Invalid field selected."

    sql_field = field_map[field]

    if not value:
        return None, None, "Please provide a value."

    query = f"""
        UPDATE NonCitizen
        SET {sql_field} = %s
        WHERE PassportID = %s
    """

    params = (value, passport_id)

    return query, params, None