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

def get_noncitizen_query(form):
    action = form.get("action")
    field = form.get("field")
    attribute = form.get("attribute")
    visaOptions = form.get("visa")
    permitOptions = form.get("permit")
    applicationOptions = form.get("application")
    borderOptions = form.get("border")
    textValue = form.get("textValue")
    dateValue = form.get("dateValue")
    dateCondition = form.get("dateCondition")
    visaType = form.get("visaType")
    stayStatus = form.get("stayStatus")
    permitType = form.get("permitType")
    appStatus = form.get("appStatus")
    booleanValue = form.get("booleanValue")

    selection = "*"
    if action == "Find":
        selection = "*"
    elif action == "Count":
        selection = "COUNT(*)"
    
    ## BASIC INFORMATION SELECTIONS
    if field == "none":
        return f"SELECT {selection} FROM NonCitizen", ()
    elif field == "basic":
        if attribute == "countryOfOrigin":
            return f"SELECT {selection} FROM NonCitizen WHERE NonCitizen.CountryOfOrigin = %s", (textValue,)
        elif attribute == "dob":
            if dateCondition == "Before":
                return f"SELECT {selection} FROM NonCitizen WHERE NonCitizen.DateOfBirth < %s", (dateValue,)
            elif dateCondition == "After":
                return f"SELECT {selection} FROM NonCitizen WHERE NonCitizen.DateOfBirth > %s", (dateValue,)
            elif dateCondition == "On":
                return f"SELECT {selection} FROM NonCitizen WHERE NonCitizen.DateOfBirth = %s", (dateValue,)
        elif attribute == "passportID":
            return f"SELECT {selection} FROM NonCitizen WHERE NonCitizen.PassportID = %s", (textValue,)
        elif attribute == "criminalRecord":
            return f"SELECT {selection} FROM NonCitizen WHERE NonCitizen.HasCriminalRecord = %s", (booleanValue,)
        elif attribute == "firstName":
            return f"SELECT {selection} FROM NonCitizen WHERE NonCitizen.FirstName = %s", (textValue,)
        elif attribute == "middleName":
            return f"SELECT {selection} FROM NonCitizen WHERE NonCitizen.MiddleName = %s", (textValue,)
        elif attribute == "lastName":
            return f"SELECT {selection} FROM NonCitizen WHERE NonCitizen.LastName = %s", (textValue,)
        elif attribute == "streetName":
            return f"SELECT {selection} FROM NonCitizen WHERE NonCitizen.StreetName = %s", (textValue,)
        elif attribute == "city":
            return f"SELECT {selection} FROM NonCitizen WHERE NonCitizen.City = %s", (textValue,)
        elif attribute == "province":
            return f"SELECT {selection} FROM NonCitizen WHERE NonCitizen.Province = %s", (textValue,)
        elif attribute == "postalCode":
            return f"SELECT {selection} FROM NonCitizen WHERE NonCitizen.PostalCode = %s", (textValue,)

    ## VISA SELECTIONS
    elif field == "visa":
        if visaOptions == "type":
            if visaType == "none":
                return f"""SELECT {selection}
                        FROM NonCitizen
                        WHERE NOT EXISTS (
                            SELECT *
                            FROM Visa
                            WHERE Visa.PassportID = NonCitizen.PassportID
                        )""", ()
            elif visaType == "all":
                return f"""SELECT {selection}
                        FROM NonCitizen
                        WHERE EXISTS (
                            SELECT *
                            FROM TransitVisa
                            WHERE TransitVisa.PassportID = NonCitizen.PassportID
                        ) AND EXISTS (
                            SELECT *
                            FROM VisitorVisa
                            WHERE VisitorVisa.PassportID = NonCitizen.PassportID
                        )""", ()
            elif visaType == "transit":
                return f"""SELECT {selection}
                        FROM NonCitizen
                        WHERE EXISTS (
                            SELECT *
                            FROM TransitVisa
                            WHERE TransitVisa.PassportID = NonCitizen.PassportID
                        )""", ()
            elif visaType == "visitor":
                return f"""SELECT {selection}
                        FROM NonCitizen
                        WHERE EXISTS (
                            SELECT *
                            FROM VisitorVisa
                            WHERE VisitorVisa.PassportID = NonCitizen.PassportID
                        )""", ()
        elif visaOptions == "status":
            if stayStatus == "valid":
                return f"SELECT {selection} FROM NonCitizen JOIN Visa ON NonCitizen.PassportID = Visa.PassportID WHERE Visa.StayStatus = 'Valid'", ()
            elif stayStatus == "expired":
                return f"SELECT {selection} FROM NonCitizen JOIN Visa ON NonCitizen.PassportID = Visa.PassportID WHERE Visa.StayStatus = 'Expired'", ()
            elif stayStatus == "revoked":
                return f"SELECT {selection} FROM NonCitizen JOIN Visa ON NonCitizen.PassportID = Visa.PassportID WHERE Visa.StayStatus = 'Revoked'", ()
        elif visaOptions == "expiry":
            if selection == "*":
                selection = "NonCitizen.*, Visa.ExpiryDate"

            if dateCondition == "Before":
                return f"""SELECT {selection}
                        FROM NonCitizen
                        JOIN Visa ON NonCitizen.PassportID = Visa.PassportID
                        WHERE Visa.ExpiryDate < %s""", (dateValue,)
            elif dateCondition == "On":
                return f"""SELECT {selection}
                        FROM NonCitizen
                        JOIN Visa ON NonCitizen.PassportID = Visa.PassportID
                        WHERE Visa.ExpiryDate = %s""", (dateValue,)
            elif dateCondition == "After":
                return f"""SELECT {selection}
                        FROM NonCitizen
                        JOIN Visa ON NonCitizen.PassportID = Visa.PassportID
                        WHERE Visa.ExpiryDate > %s""", (dateValue,)
        elif visaOptions == "issue":
            if selection == "*":
                selection = "NonCitizen.*, Visa.IssueDate"

            if dateCondition == "Before":
                return f"""SELECT {selection}
                        FROM NonCitizen
                        JOIN Visa ON NonCitizen.PassportID = Visa.PassportID
                        WHERE Visa.IssueDate < %s""", (dateValue,)
            elif dateCondition == "On":
                return f"""SELECT {selection}
                        FROM NonCitizen
                        JOIN Visa ON NonCitizen.PassportID = Visa.PassportID
                        WHERE Visa.IssueDate = %s""", (dateValue,)
            elif dateCondition == "After":
                return f"""SELECT {selection}
                        FROM NonCitizen
                        JOIN Visa ON NonCitizen.PassportID = Visa.PassportID
                        WHERE Visa.IssueDate > %s""", (dateValue,)
        
    ## PERMIT SELECTIONS
    elif field == "permit":
        if permitOptions == "type":
            if permitType == "none":
                return f"""SELECT {selection}
                        FROM NonCitizen
                        WHERE NOT EXISTS (
                            SELECT *
                            FROM Permit
                            WHERE Permit.PassportID = NonCitizen.PassportID
                        )""", ()
            elif permitType == "all":
                return f"""SELECT {selection}
                        FROM NonCitizen
                        WHERE EXISTS (
                            SELECT *
                            FROM StudyPermit
                            WHERE StudyPermit.PassportID = NonCitizen.PassportID
                        ) AND EXISTS (
                            SELECT *
                            FROM WorkPermit
                            WHERE WorkPermit.PassportID = NonCitizen.PassportID
                        )""", ()
            elif permitType == "study":
                return f"""SELECT {selection}
                        FROM NonCitizen
                        WHERE EXISTS (
                            SELECT *
                            FROM StudyPermit
                            WHERE StudyPermit.PassportID = NonCitizen.PassportID
                        )""", ()
            elif permitType == "work":
                return f"""SELECT {selection}
                        FROM NonCitizen
                        WHERE EXISTS (
                            SELECT *
                            FROM WorkPermit
                            WHERE WorkPermit.PassportID = NonCitizen.PassportID
                        )""", ()
        elif permitOptions == "expiry":
            if selection == "*":
                selection = "NonCitizen.*, Permit.ExpiryDate"

            if dateCondition == "Before":
                return f"""SELECT {selection}
                    FROM NonCitizen
                    JOIN Permit ON NonCitizen.PassportID = Permit.PassportID
                    WHERE Permit.ExpiryDate < %s""", (dateValue,)
            elif dateCondition == "On":
                return f"""SELECT {selection}
                    FROM NonCitizen
                    JOIN Permit ON NonCitizen.PassportID = Permit.PassportID
                    WHERE Permit.ExpiryDate = %s""", (dateValue,)
            elif dateCondition == "After":
                return f"""SELECT {selection}
                    FROM NonCitizen
                    JOIN Permit ON NonCitizen.PassportID = Permit.PassportID
                    WHERE Permit.ExpiryDate > %s""", (dateValue,)
        elif permitOptions == "issue":
            if selection == "*":
                selection = "NonCitizen.*, Permit.IssueDate"

            if dateCondition == "Before":
                return f"""SELECT {selection}
                    FROM NonCitizen
                    JOIN Permit ON NonCitizen.PassportID = Permit.PassportID
                    WHERE Permit.IssueDate < %s""", (dateValue,)
            elif dateCondition == "On":
                return f"""SELECT {selection}
                    FROM NonCitizen
                    JOIN Permit ON NonCitizen.PassportID = Permit.PassportID
                    WHERE Permit.IssueDate = %s""", (dateValue,)
            elif dateCondition == "After":
                return f"""SELECT {selection}
                    FROM NonCitizen
                    JOIN Permit ON NonCitizen.PassportID = Permit.PassportID
                    WHERE Permit.IssueDate > %s""", (dateValue,)
            
    ## APPLICATION SELECTION
    elif field == "application":
        if applicationOptions == "submission":
            if selection == "*":
                selection = "NonCitizen.*, SUBMITS.SubmissionDate"
            if dateCondition == "Before":
                return f"""SELECT {selection}
                    FROM NonCitizen
                    JOIN SUBMITS ON NonCitizen.PassportID = SUBMITS.PassportID
                    WHERE SUBMITS.SubmissionDate < %s""", (dateValue,)
            elif dateCondition == "On":
                return f"""SELECT {selection}
                    FROM NonCitizen
                    JOIN SUBMITS ON NonCitizen.PassportID = SUBMITS.PassportID
                    WHERE SUBMITS.SubmissionDate = %s""", (dateValue,)
            elif dateCondition == "After":
                return f"""SELECT {selection}
                    FROM NonCitizen
                    JOIN SUBMITS ON NonCitizen.PassportID = SUBMITS.PassportID
                    WHERE SUBMITS.SubmissionDate > %s""", (dateValue,)
            
        elif applicationOptions == "status":
            if selection == "*":
                selection = "NonCitizen.*, Application.Status"

            if appStatus == "in progress":
                return f"""SELECT {selection}
                    FROM NonCitizen
                    JOIN SUBMITS ON NonCitizen.PassportID = SUBMITS.PassportID
                    JOIN Application ON SUBMITS.ApplicationID = Application.ApplicationID
                    WHERE Application.Status = 'In Progress'""", ()
            elif appStatus == "approved":
                return f"""SELECT {selection}
                    FROM NonCitizen
                    JOIN SUBMITS ON NonCitizen.PassportID = SUBMITS.PassportID
                    JOIN Application ON SUBMITS.ApplicationID = Application.ApplicationID
                    WHERE Application.Status = 'Approved'""", ()
            elif appStatus == "rejected":
                return f"""SELECT {selection}
                    FROM NonCitizen
                    JOIN SUBMITS ON NonCitizen.PassportID = SUBMITS.PassportID
                    JOIN Application ON SUBMITS.ApplicationID = Application.ApplicationID
                    WHERE Application.Status = 'Rejected'""", ()
            elif appStatus == "submitted":
                return f"""SELECT {selection}
                    FROM NonCitizen
                    JOIN SUBMITS ON NonCitizen.PassportID = SUBMITS.PassportID
                    JOIN Application ON SUBMITS.ApplicationID = Application.ApplicationID
                    WHERE Application.Status = 'Submitted'""", ()
        
    ## BORDER CROSSING SELECTION
    elif field == "border":
        if borderOptions == "date":
            if dateCondition == "Before":
                return f"""SELECT {selection}
                        FROM NonCitizen
                        JOIN CROSSES ON NonCitizen.PassportID = CROSSES.PassportID
                        WHERE CROSSES.CrossingDate < %s;""", (dateValue,)
            elif dateCondition == "On":
                return f"""SELECT {selection}
                        FROM NonCitizen
                        JOIN CROSSES ON NonCitizen.PassportID = CROSSES.PassportID
                        WHERE CROSSES.CrossingDate = %s;""", (dateValue,)
            elif dateCondition == "After":
                return f"""SELECT {selection}
                        FROM NonCitizen
                        JOIN CROSSES ON NonCitizen.PassportID = CROSSES.PassportID
                        WHERE CROSSES.CrossingDate > %s;""", (dateValue,)
        if borderOptions == "hasEntered":
            if selection == "*":
                selection = "NonCitizen.*, COUNT(*) AS EntryCount"

            return f"""SELECT {selection}
                    FROM NonCitizen
                    JOIN CROSSES ON NonCitizen.PassportID = CROSSES.PassportID
                    JOIN BorderCrossing ON CROSSES.CrossingDate = BorderCrossing.Date AND CROSSES.CrossingTime = BorderCrossing.Time
                    WHERE BorderCrossing.EntryOrExit = 'Entry'
                    GROUP BY NonCitizen.PassportID;""", ()
        
        if borderOptions == "hasExited":
            if selection == "*":
                selection = "NonCitizen.*, COUNT(*) AS EntryCount"

            return f"""SELECT {selection}
                    FROM NonCitizen
                    JOIN CROSSES ON NonCitizen.PassportID = CROSSES.PassportID
                    JOIN BorderCrossing ON CROSSES.CrossingDate = BorderCrossing.Date AND CROSSES.CrossingTime = BorderCrossing.Time
                    WHERE BorderCrossing.EntryOrExit = 'Exit'
                    GROUP BY NonCitizen.PassportID;""", ()
        
        if borderOptions == "allCrossingTypes":

            return f"""SELECT DISTINCT NonCitizensWithAllCrossingTypes.*
                    FROM (
                        SELECT NonCitizen.*
                        FROM NonCitizen
                        WHERE NOT EXISTS (
                            SELECT CrossingTypes.EntryOrExit
                            FROM (
                                SELECT BorderCrossing.EntryOrExit
                                FROM BorderCrossing
                                GROUP BY BorderCrossing.EntryOrExit
                                ) CrossingTypes
                            WHERE NOT EXISTS (
                                SELECT 1
                                FROM CROSSES
                                JOIN BorderCrossing ON BorderCrossing.Date = CROSSES.CrossingDate AND BorderCrossing.Time = CROSSES.CrossingTime
                                WHERE NonCitizen.PassportID = CROSSES.PassportID AND BorderCrossing.EntryOrExit = CrossingTypes.EntryOrExit
                                )
                            )
                        ) NonCitizensWithAllCrossingTypes;""", ()
    
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
