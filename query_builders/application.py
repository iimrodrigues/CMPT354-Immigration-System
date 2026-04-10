def application_remove(form):
    return "--"

def application_add(form):
    applicationID = form.get("applicationID")  
    status = form.get("status")

    if(not applicationID): return "--" 
    if(status == "- Select Application Status -"): return "--"

    return f"""
            START TRANSACTION;
            INSERT INTO Application (ApplicationID, Status)
            VALUES ({applicationID}, '{status}');
            COMMIT;
            """