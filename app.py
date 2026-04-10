from flask import Flask, render_template, redirect, url_for, request
from db import get_connection
from query_builders import application, permit, visa

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

    return f"You selected {entity} + {action}"

## VISA ACTIONS
@app.route("/visa/query", methods=["GET", "POST"])
def visa_query():
    if request.method == "POST":
        (sql, params) = visa.get_visa_query(request.form)
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(sql, params)
        results = cursor.fetchall()
        return render_template("visa/query.html", results=results)
        
    return render_template("visa/query.html", results=None)

## PERMIT ACTIONS
@app.route("/permit/query", methods=["GET", "POST"])
def permit_query():
    if request.method == "POST":
        (sql, params) = permit.get_permit_query(request.form)
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(sql, params)
        results = cursor.fetchall()
        return render_template("permit/query.html", results=results)
    
    return render_template("permit/query.html", results=None)

## APPLICATION ACTIONS
@app.route("/application/query", methods=["GET", "POST"])
def application_query():
    if request.method == "POST":
        (sql, params) = application.get_application_query(request.form)
        print(sql, params)
            
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
    
        cursor.execute(sql, params)
        results = cursor.fetchall()
        return render_template("application/query.html", results=results)
        
    return render_template("application/query.html", results=None)

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