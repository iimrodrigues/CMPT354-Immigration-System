def update_query(form):
    field = form.get("field")
    date = form.get("date")
    time = form.get("time")
    value = form.get("value")

    if not date or not time or not field or field == "none":
        return None, None, "Please fill in all fields."

    field_map = {
        "City": "City",
        "Province": "Province",
        "PostalCode": "PostalCode",
        "EntryOrExit": "EntryOrExit"
    }

    if field not in field_map:
        return None, None, "Invalid field selected."

    sql_field = field_map[field]

    if not value:
        return None, None, "Please provide a value."

    query = f"""
        UPDATE BorderCrossing
        SET {sql_field} = %s
        WHERE Date = %s AND Time = %s
    """

    params = (value, date, time)

    return query, params, None