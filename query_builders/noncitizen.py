def noncitizen_remove(form):

    passportID = form.get("passportID")
    if(not passportID): return "--"
    
    return f"""
            START TRANSACTION;
            DELETE FROM NonCitizen WHERE PassportID = '{passportID}';
            COMMIT;
            """

def noncitizen_add(form):
    passportID = form.get("passportID")
    firstName = form.get("firstName")
    middleName = form.get("middleName")
    lastName = form.get("lastName")
    dob = form.get("dob")
    country = form.get("country")
    street = form.get("street")
    city = form.get("city")
    province = form.get("province")
    postal = form.get("postal")
    criminalRecord = form.get("criminalRecord")

    if(not passportID): return "--"
    if(not firstName): return "--"
    if(not lastName): return "--"
    if(not dob): return "--"
    if(not country): return "--"
    if(not street): return "--"
    if(not city): return "--"
    if(province == "- Select Province -"): return "--"
    if(len(postal) < 7): return "--"

    if(criminalRecord == "Yes"): criminalRecord = "True"
    elif(criminalRecord == "No"): criminalRecord = "False"
    else: return "--"

    return f"""
            START TRANSACTION;
            INSERT INTO NonCitizen (PassportID, FirstName, MiddleName, LastName, HasCriminalRecord, DateOfBirth, CountryOfOrigin, StreetName, City, Province, PostalCode) 
            VALUES ('{passportID}', '{firstName}', '{middleName}', '{lastName}', {criminalRecord}, '{dob}', '{country}', '{street}', '{city}', '{province}', '{postal}');
            COMMIT;
            """