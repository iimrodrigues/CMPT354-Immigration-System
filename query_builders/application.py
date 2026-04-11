def application_remove(form):
    applicationID = form.get("applicationID")  

    if(not applicationID): return "--" 

    return f"""
            START TRANSACTION;
            DELETE FROM StudyPermit WHERE PassportID = (SELECT PassportID FROM Permit WHERE ApplicationID = {applicationID});
            DELETE FROM WorkPermit WHERE PassportID = (SELECT PassportID FROM Permit WHERE ApplicationID = {applicationID});
            DELETE FROM Permit WHERE ApplicationID = {applicationID};
            DELETE FROM TransitVisa WHERE PassportID = (SELECT PassportID FROM Visa WHERE ApplicationID = {applicationID});
            DELETE FROM VisitorVisa WHERE PassportID = (SELECT PassportID FROM Visa WHERE ApplicationID = {applicationID});
            DELETE FROM Visa WHERE ApplicationID = {applicationID};
            DELETE FROM SUBMITS WHERE ApplicationID = {applicationID};
            DELETE FROM SupportingDocuments WHERE ApplicationID = {applicationID};
            DELETE FROM Application WHERE ApplicationID = {applicationID};
            COMMIT;
            """

def application_add(form):
    applicationID = form.get("applicationID")  
    passportID = form.get("passportID")
    submissionDate = form.get("submissionDate")
    documentNumber = form.get("document")
    status = form.get("status")

    if(not applicationID): return "--"
    if(not passportID): return "--"
    if(not submissionDate): return "--"
    if(not documentNumber): return "--"
    if(status == "- Select Application Status -"): return "--"

    return f"""
            START TRANSACTION;
            INSERT INTO Application (ApplicationID, Status)
            VALUES ({applicationID}, '{status}');
            INSERT INTO SUBMITS (ApplicationID, PassportID, SubmissionDate)
            VALUES ({applicationID}, '{passportID}', '{submissionDate}');
            INSERT INTO SupportingDocuments (ApplicationID, DocumentNumber)
            VALUES ({applicationID}, {documentNumber});
            COMMIT;
            """