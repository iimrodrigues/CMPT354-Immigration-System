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

    if entity == "Visa" and action == "Update":
        return redirect(url_for("visa_update"))
    elif entity == "Permit" and action == "Update":
        return redirect(url_for("permit_update"))
    elif entity == "Application" and action == "Update":
        return redirect(url_for("application_update"))
    elif entity == "Border Crossing" and action == "Update":
        return redirect(url_for("bordercrossing_update"))
    elif entity == "Non-Citizen" and action == "Update":
        return redirect(url_for("noncitizen_update"))

    print(entity, action)

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

@app.route('/permit/update', methods=['GET', 'POST'])
def permit_update():
    message = None
    results = None

    if request.method == 'POST':
        query, error = get_permit_update_query(request.form)

        if error:
            message = error
        else:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(sql, params)
            results = cursor.fetchall()

            # Show the updated record
            passport_id = request.form.get("passportID")
            permit_id = request.form.get("permitID")
            cursor.execute(
                "SELECT * FROM Permit WHERE PassportID = %s AND PermitID = %s",
                (passport_id, permit_id)
            )
            results = cursor.fetchall()
            message = "Permit updated successfully."

    return render_template('permit/update.html', message=message, results=results)

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