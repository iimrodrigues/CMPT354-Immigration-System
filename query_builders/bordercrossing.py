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