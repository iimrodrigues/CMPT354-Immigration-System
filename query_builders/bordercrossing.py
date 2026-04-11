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

def bordercrossing_remove(form):
    date = form.get("date")
    time = form.get("time")

    if(not date): return "--"
    if(not time): return "--"

    return f"""
            START TRANSACTION;
            DELETE FROM CROSSES WHERE CrossingDate = '{date}' AND CrossingTime = '{time + ":00"}';
            DELETE FROM BorderCrossing WHERE Date = '{date}' AND Time = '{time + ":00"}';
            COMMIT;
            """

def bordercrossing_add(form):
    date = form.get("date")
    time = form.get("time")
    city = form.get("city")
    province = form.get("province")
    postal = form.get("postal")
    crossing = form.get("crossing")

    if(not date): return "--"
    if(not time): return "--"
    if(not city): return "--"
    if(province == "- Select Province -"): return "--"
    if(len(postal) < 7): return "--"

    return f"""
            START TRANSACTION;
            INSERT INTO BorderCrossing (Date, Time, City, Province, PostalCode, EntryOrExit)
            VALUES ('{date}', '{time + ":00"}', '{city}', '{province}', '{postal}', '{crossing}');
            COMMIT;
            """