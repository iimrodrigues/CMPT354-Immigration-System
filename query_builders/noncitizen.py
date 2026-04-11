def noncitizen_remove(form):

    passportID = form.get("passportID")
    if(len(passportID) < 8): return None
    
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

    if(len(passportID) < 8): return None
    if(not firstName): return None
    if(not lastName): return None
    if(not dob): return None
    if(not country): return None
    if(not street): return None
    if(not city): return None
    if(province == "- Select Province -"): return None
    if(len(postal) < 7): return None

    if(criminalRecord == "Yes"): criminalRecord = "True"
    elif(criminalRecord == "No"): criminalRecord = "False"
    else: return None

    return f"""
            START TRANSACTION;
            INSERT INTO NonCitizen (PassportID, FirstName, MiddleName, LastName, HasCriminalRecord, DateOfBirth, CountryOfOrigin, StreetName, City, Province, PostalCode) 
            VALUES ('{passportID}', '{firstName}', '{middleName}', '{lastName}', {criminalRecord}, '{dob}', '{country}', '{street}', '{city}', '{province}', '{postal}');
            COMMIT;
            """