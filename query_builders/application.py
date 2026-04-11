def application_remove(form):
    applicationID = form.get("applicationID")  

    if(not applicationID): return None 

    return f"""
            START TRANSACTION;
            DELETE FROM Application WHERE ApplicationID = {applicationID};
            COMMIT;
            """

def application_add(form):
    applicationID = form.get("applicationID")  
    passportID = form.get("passportID")
    submissionDate = form.get("submissionDate")
    documentNumber = form.get("document")
    status = form.get("status")

    if(not applicationID): return None
    if(len(passportID) < 8): return None
    if(not submissionDate): return None
    if(not documentNumber): return None
    if(status == "- Select Application Status -"): return None

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