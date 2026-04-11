from flask import Flask, render_template, redirect, url_for, request
from db import get_connection
from query_builders import permit, visa, noncitizen, bordercrossing, application

app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/select", methods=["POST"])
def select():
    print("SELECTED")
    entity = request.form.get("entity")
    action = request.form.get("action")

    if entity == "Visa" and action == "Query":
        return redirect(url_for("visa_query"))
    elif entity == "Permit" and action == "Query":
        return redirect(url_for("permit_query"))
    elif entity == "Application" and action == "Query":
        return redirect(url_for("application_query"))
    elif entity == "Border Crossing" and action == "Query":
        return redirect(url_for("bordercrossing_query"))
    elif entity == "Non-Citizen" and action == "Query":
        return redirect(url_for("noncitizen_query"))

    if entity == "Visa" and action == "Remove":
        return redirect(url_for("visa_remove"))
    elif entity == "Permit" and action == "Remove":
        return redirect(url_for("permit_remove"))
    elif entity == "Application" and action == "Remove":
        return redirect(url_for("application_remove"))
    elif entity == "Border Crossing" and action == "Remove":
        return redirect(url_for("bordercrossing_remove"))
    elif entity == "Non-Citizen" and action == "Remove":
        return redirect(url_for("noncitizen_remove"))
    
    if entity == "Visa" and action == "Add":
        return redirect(url_for("visa_add"))
    elif entity == "Permit" and action == "Add":
        return redirect(url_for("permit_add"))
    elif entity == "Application" and action == "Add":
        return redirect(url_for("application_add"))
    elif entity == "Border Crossing" and action == "Add":
        return redirect(url_for("bordercrossing_add"))
    elif entity == "Non-Citizen" and action == "Add":
        return redirect(url_for("noncitizen_add"))

    return f"You selected {entity} + {action}"

## VISA ACTIONS
@app.route("/visa/query", methods=["GET", "POST"])
def visa_query():
    if request.method == "POST":
        sql = visa.get_visa_query(request.form)
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(sql)
        results = cursor.fetchall()
        return render_template("visa/query.html", results=results)
        
    return render_template("visa/query.html", results=None)

@app.route("/visa/remove", methods=["GET", "POST"])
def visa_remove():
    if request.method == "POST":
        sql = visa.visa_remove(request.form)
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(sql)
        
    return render_template("visa/remove.html", results=None)

@app.route("/visa/add", methods=["GET", "POST"])
def visa_add():
    if request.method == "POST":
        sql = visa.visa_add(request.form)
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)

        type = request.form.get("visaType")
        id = request.form.get("visaID")

        if(type == "Transit Visa"):
            sql = f"""
                    START TRANSACTION;
                    DELETE from VisitorVisa WHERE VisaID = '{id}';
                    COMMIT;
                    """
        elif(type == "Visitor Visa"):
            sql = f"""
                    START TRANSACTION;
                    DELETE from TransitVisa WHERE VisaID = '{id}';
                    COMMIT;
                    """
        else:
            sql = "--"

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        
    return render_template("visa/add.html", results=None)

## PERMIT ACTIONS
@app.route("/permit/query", methods=["GET", "POST"])
def permit_query():
    if request.method == "POST":
        sql = permit.get_permit_query(request.form)
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(sql)
        results = cursor.fetchall()
        return render_template("permit/query.html", results=results)
    
    return render_template("permit/query.html", results=None)

@app.route("/permit/remove", methods=["GET", "POST"])
def permit_remove():
    if request.method == "POST":
        sql = permit.permit_remove(request.form)
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
    
    return render_template("permit/remove.html", results=None)

@app.route("/permit/add", methods=["GET", "POST"])
def permit_add():
    if request.method == "POST":
        sql = permit.permit_add(request.form)
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)

        type = request.form.get("permitType")
        id = request.form.get("permitID")

        if(type == "Study Permit"):
            sql = f"""
                    START TRANSACTION;
                    DELETE from WorkPermit WHERE PermitID = '{id}';
                    COMMIT;
                    """
        elif(type == "Work Permit"):
            sql = f"""
                    START TRANSACTION;
                    DELETE from StudyPermit WHERE PermitID = '{id}';
                    COMMIT;
                    """
        else:
            sql = "--"

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
    
    return render_template("permit/add.html", results=None)

## APPLICATION ACTIONS
@app.route("/application/query", methods=["GET", "POST"])
def application_query():
    return render_template("application/query.html")

@app.route("/application/remove", methods=["GET", "POST"])
def application_remove():
    if request.method == "POST":
        sql = application.application_remove(request.form)
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
    
    return render_template("application/remove.html", results=None)

@app.route("/application/add", methods=["GET", "POST"])
def application_add():
    if request.method == "POST":
        sql = application.application_add(request.form)
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
    
    return render_template("application/add.html", results=None)

## BORDER CROSSING ACTIONS
@app.route("/bordercrossing/query", methods=["GET", "POST"])
def bordercrossing_query():
    return render_template("bordercrossing/query.html")

@app.route("/bordercrossing/remove", methods=["GET", "POST"])
def bordercrossing_remove():
    if request.method == "POST":
        sql = bordercrossing.bordercrossing_remove(request.form)
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
    
    return render_template("bordercrossing/remove.html", results=None)

@app.route("/bordercrossing/add", methods=["GET", "POST"])
def bordercrossing_add():
    if request.method == "POST":
        sql = bordercrossing.bordercrossing_add(request.form)
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
    
    return render_template("bordercrossing/add.html", results=None)

## NON-CITIZEN ACTIONS
@app.route("/noncitizen/query", methods=["GET", "POST"])
def noncitizen_query():
    return render_template("noncitizen/query.html")

@app.route("/noncitizen/remove", methods=["GET", "POST"])
def noncitizen_remove():
    if request.method == "POST":
        sql = noncitizen.noncitizen_remove(request.form)
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
    
    return render_template("noncitizen/remove.html", results=None)

@app.route("/noncitizen/add", methods=["GET", "POST"])
def noncitizen_add():
    if request.method == "POST":
        sql = noncitizen.noncitizen_add(request.form)
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
    
    return render_template("noncitizen/add.html", results=None)

if __name__ == "__main__":
    app.run(debug=True)