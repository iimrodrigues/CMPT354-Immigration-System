from flask import Flask, render_template, redirect, url_for, request
from db import get_connection
from query_builders import permit, visa

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
        results = cursor.fetchall()
        if(results): return render_template("visa/remove.html", results=results)
        
    return render_template("visa/remove.html", results=None)

@app.route("/visa/add", methods=["GET", "POST"])
def visa_add():
    if request.method == "POST":
        sql = visa.visa_add(request.form)
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(sql)
        results = cursor.fetchall()
        if(results): return render_template("visa/add.html", results=results)
        
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
        results = cursor.fetchall()
        if(results): return render_template("permit/remove.html", results=results)
    
    return render_template("permit/remove.html", results=None)

## APPLICATION ACTIONS
@app.route("/application/query", methods=["GET", "POST"])
def application_query():
    return render_template("application/query.html")

## BORDER CROSSING ACTIONS
@app.route("/bordercrossing/query", methods=["GET", "POST"])
def bordercrossing_query():
    return render_template("bordercrossing/query.html")

## NON-CITIZEN ACTIONS
@app.route("/noncitizen/query", methods=["GET", "POST"])
def noncitizen_query():
    return render_template("noncitizen/query.html")

if __name__ == "__main__":
    app.run(debug=True)