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

def get_bordercrossing_query(form):
    action = form.get("action")
    field = form.get("field")
    dateCondition = form.get("dateCondition")
    date = form.get("dateValue")
    timeCondition = form.get("timeCondition")
    time = form.get("timeValue")
    ncCondition = form.get("ncCondition")
    textValue = form.get("textValue")

    selection = ""
    if action == "Find":
        selection = "*"
    elif action == "Count":
        selection = "COUNT(*)"
    elif action == "Max":
        if field == "date":
            return f"SELECT * FROM BorderCrossing WHERE Date = (SELECT MAX(Date) FROM BorderCrossing);", ()
        elif field == "time":
            return f"SELECT * FROM BorderCrossing WHERE Time = (SELECT MAX(Time) FROM BorderCrossing);", ()
        else:
            selection = "*"
    elif action == "Min":
        if field == "date":
            return f"SELECT * FROM BorderCrossing WHERE Date = (SELECT MIN(Date) FROM BorderCrossing);", ()
        elif field == "time":
            return f"SELECT * FROM BorderCrossing WHERE Time = (SELECT MIN(Time) FROM BorderCrossing);", ()
        else:
            selection = "*"

    if field == "none":
        return f"SELECT {selection} FROM BorderCrossing;", ()
    elif field == "date":
        if dateCondition == "Before":
            return f"SELECT {selection} FROM BorderCrossing WHERE BorderCrossing.Date < %s;", (date,)
        elif dateCondition == "On":
            return f"SELECT {selection} FROM BorderCrossing WHERE BorderCrossing.Date = %s;", (date,)
        elif dateCondition == "After":
            return f"SELECT {selection} FROM BorderCrossing WHERE BorderCrossing.Date > %s;", (date,)
    elif field == "time":
        if timeCondition == "Before":
            return f"SELECT {selection} FROM BorderCrossing WHERE BorderCrossing.Time < %s;", (time,)
        elif timeCondition == "On":
            return f"SELECT {selection} FROM BorderCrossing WHERE BorderCrossing.Time = %s;", (time,)
        elif timeCondition == "After":
            return f"SELECT {selection} FROM BorderCrossing WHERE BorderCrossing.Time > %s;", (time,)
    elif field == "city":
        return f"SELECT {selection} FROM BorderCrossing WHERE BorderCrossing.City = %s;", (textValue,)
    elif field == "province":
        return f"SELECT {selection} FROM BorderCrossing WHERE BorderCrossing.Province = %s;", (textValue,)
    elif field == "postal":
        return f"SELECT {selection} FROM BorderCrossing WHERE BorderCrossing.PostalCode = %s;", (textValue,)
    elif field == "entry":
        return f"SELECT {selection} FROM BorderCrossing WHERE BorderCrossing.EntryOrExit = %s;", ("Entry",)
    elif field == "exit":
        return f"SELECT {selection} FROM BorderCrossing WHERE BorderCrossing.EntryOrExit = %s;", ("Exit",)
    elif field == "nc":
        if ncCondition == "First Name":
            if selection == "*":
                return f"""SELECT BorderCrossing.*, NonCitizen.FirstName
                        FROM BorderCrossing
                        JOIN CROSSES ON BorderCrossing.Date = CROSSES.CrossingDate AND BorderCrossing.Time = CROSSES.CrossingTime
                        JOIN NonCitizen ON CROSSES.PassportID = NonCitizen.PassportID
                        WHERE NonCitizen.FirstName = %s;""", (textValue,)
            elif selection == "COUNT(*)":
                return f"""SELECT COUNT(*) AS Count
                        FROM BorderCrossing
                        JOIN CROSSES ON BorderCrossing.Date = CROSSES.CrossingDate AND BorderCrossing.Time = CROSSES.CrossingTime
                        JOIN NonCitizen ON CROSSES.PassportID = NonCitizen.PassportID
                        WHERE NonCitizen.FirstName = %s;""", (textValue,)
        elif ncCondition == "Last Name":
            if selection == "*":
                return f"""SELECT BorderCrossing.*, NonCitizen.LastName
                    FROM BorderCrossing
                    JOIN CROSSES ON BorderCrossing.Date = CROSSES.CrossingDate AND BorderCrossing.Time = CROSSES.CrossingTime
                    JOIN NonCitizen ON CROSSES.PassportID = NonCitizen.PassportID
                    WHERE NonCitizen.LastName = %s;""", (textValue,)
            elif selection == "COUNT(*)":
                return f"""SELECT COUNT(*) AS Count
                    FROM BorderCrossing
                    JOIN CROSSES ON BorderCrossing.Date = CROSSES.CrossingDate AND BorderCrossing.Time = CROSSES.CrossingTime
                    JOIN NonCitizen ON CROSSES.PassportID = NonCitizen.PassportID
                    WHERE NonCitizen.LastName = %s;""", (textValue,)
        elif ncCondition == "City":
            if selection == "*":
                return f"""SELECT BorderCrossing.*, NonCitizen.City
                    FROM BorderCrossing
                    JOIN CROSSES ON BorderCrossing.Date = CROSSES.CrossingDate AND BorderCrossing.Time = CROSSES.CrossingTime
                    JOIN NonCitizen ON CROSSES.PassportID = NonCitizen.PassportID
                    WHERE NonCitizen.City = %s;""", (textValue,)
            elif selection == "COUNT(*)":
                return f"""SELECT COUNT(*) AS Count
                    FROM BorderCrossing
                    JOIN CROSSES ON BorderCrossing.Date = CROSSES.CrossingDate AND BorderCrossing.Time = CROSSES.CrossingTime
                    JOIN NonCitizen ON CROSSES.PassportID = NonCitizen.PassportID
                    WHERE NonCitizen.City = %s;""", (textValue,)
        elif ncCondition == "Province":
            if selection == "*":
                return f"""SELECT BorderCrossing.*, NonCitizen.Province
                    FROM BorderCrossing
                    JOIN CROSSES ON BorderCrossing.Date = CROSSES.CrossingDate AND BorderCrossing.Time = CROSSES.CrossingTime
                    JOIN NonCitizen ON CROSSES.PassportID = NonCitizen.PassportID
                    WHERE NonCitizen.Province = %s;""", (textValue,)
            elif selection == "COUNT(*)":
                return f"""SELECT COUNT(*) AS Count
                    FROM BorderCrossing
                    JOIN CROSSES ON BorderCrossing.Date = CROSSES.CrossingDate AND BorderCrossing.Time = CROSSES.CrossingTime
                    JOIN NonCitizen ON CROSSES.PassportID = NonCitizen.PassportID
                    WHERE NonCitizen.Province = %s;""", (textValue,)
        elif ncCondition == "Country of Origin":
            if selection == "*":
                return f"""SELECT BorderCrossing.*, NonCitizen.CountryOfOrigin
                    FROM BorderCrossing
                    JOIN CROSSES ON BorderCrossing.Date = CROSSES.CrossingDate AND BorderCrossing.Time = CROSSES.CrossingTime
                    JOIN NonCitizen ON CROSSES.PassportID = NonCitizen.PassportID
                    WHERE NonCitizen.CountryOfOrigin = %s;""", (textValue,)
            elif selection == "COUNT(*)":
                return f"""SELECT COUNT(*) AS Count
                    FROM BorderCrossing
                    JOIN CROSSES ON BorderCrossing.Date = CROSSES.CrossingDate AND BorderCrossing.Time = CROSSES.CrossingTime
                    JOIN NonCitizen ON CROSSES.PassportID = NonCitizen.PassportID
                    WHERE NonCitizen.CountryOfOrigin = %s;""", (textValue,)
def bordercrossing_remove(form):
    date = form.get("date")
    time = form.get("time")

    if(not date): return None
    if(not time): return None

    return f"""
            START TRANSACTION;
            DELETE FROM BorderCrossing WHERE Date = '{date}' AND Time = '{time + ":00"}';
            COMMIT;
            """

def bordercrossing_add(form):
    passportID = form.get("passportID")
    date = form.get("date")
    time = form.get("time")
    city = form.get("city")
    province = form.get("province")
    postal = form.get("postal")
    crossing = form.get("crossing")

    if(len(passportID) < 8): return None
    if(not date): return None
    if(not time): return None
    if(not city): return None
    if(province == "- Select Province -"): return None
    if(len(postal) < 7): return None

    return f"""
            START TRANSACTION;
            INSERT INTO BorderCrossing (Date, Time, City, Province, PostalCode, EntryOrExit)
            VALUES ('{date}', '{time + ":00"}', '{city}', '{province}', '{postal}', '{crossing}');
            INSERT INTO CROSSES (CrossingDate, CrossingTime, PassportID)
            VALUES ('{date}', '{time + ":00"}', '{passportID}');
            COMMIT;
            """
