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

def noncitizen_remove(form):

    passportID = form.get("passportID")
    if(not passportID): return "--"
    
    return f"""
            START TRANSACTION;
            DELETE FROM CROSSES WHERE PassportID = '{passportID}';
            DELETE FROM SUBMITS WHERE PassportID = '{passportID}';
            DELETE FROM TransitVisa WHERE PassportID = '{passportID}';
            DELETE FROM VisitorVisa WHERE PassportID = '{passportID}';
            DELETE FROM Visa WHERE PassportID = '{passportID}';
            DELETE FROM StudyPermit WHERE PassportID = '{passportID}';
            DELETE FROM WorkPermit WHERE PassportID = '{passportID}';
            DELETE FROM Permit WHERE PassportID = '{passportID}';
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