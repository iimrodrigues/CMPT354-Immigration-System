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