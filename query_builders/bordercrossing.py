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