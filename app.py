from flask import Flask, render_template, redirect, url_for, request
from db import get_connection
from query_builders import application, permit, visa, bordercrossing, noncitizen

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

@app.route('/visa/update', methods=['GET', 'POST'])
def visa_update():
    if request.method == 'POST':
        (sql, params, error) = visa.update_query(request.form)

        if error:
            return render_template('visa/update.html', message=error, results=None)

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        passport_id = request.form.get("passportID")
        visa_id = request.form.get("visaID")

        cursor.execute(
            "SELECT 1 FROM Visa WHERE PassportID = %s AND VisaID = %s",
            (passport_id, visa_id)
        )
        if not cursor.fetchone():
            return render_template('visa/update.html', message="Visa does not exist.", results=None)

        cursor.execute(sql, params)
        conn.commit()

        cursor.execute(
            "SELECT * FROM Visa WHERE PassportID = %s AND VisaID = %s",
            (passport_id, visa_id)
        )
        results = cursor.fetchall()

        return render_template(
            'visa/update.html',
            message="Visa updated successfully.",
            results=results
        )

    return render_template('visa/update.html', results=None)

## PERMIT ACTIONS
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
    if request.method == 'POST':
        (sql, params, error) = permit.update_query(request.form)

        if error:
            return render_template(
                'permit/update.html',
                message=error,
                results=None
            )

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        passport_id = request.form.get("passportID")
        permit_id = request.form.get("permitID")

        cursor.execute(
            "SELECT 1 FROM Permit WHERE PassportID = %s AND PermitID = %s",
            (passport_id, permit_id)
        )
        exists = cursor.fetchone()

        if not exists:
            return render_template(
                'permit/update.html',
                message="Permit does not exist.",
                results=None
            )
        
        cursor.execute(sql, params)
        conn.commit()

        cursor.execute(
            "SELECT * FROM Permit WHERE PassportID = %s AND PermitID = %s",
            (passport_id, permit_id)
        )
        results = cursor.fetchall()

        return render_template(
            'permit/update.html',
            message="Permit updated successfully.",
            results=results
        )

    return render_template('permit/update.html', results=None)

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

@app.route('/application/update', methods=['GET', 'POST'])
def application_update():
    if request.method == 'POST':
        (sql, params, error) = application.update_query(request.form)

        if error:
            return render_template('application/update.html', message=error, results=None)

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        application_id = request.form.get("applicationID")

        cursor.execute(
            "SELECT 1 FROM Application WHERE ApplicationID = %s",
            (application_id,)
        )
        if not cursor.fetchone():
            return render_template('application/update.html', message="Application does not exist.", results=None)

        cursor.execute(sql, params)
        conn.commit()

        cursor.execute(
            "SELECT * FROM Application WHERE ApplicationID = %s",
            (application_id,)
        )
        results = cursor.fetchall()

        return render_template(
            'application/update.html',
            message="Application updated successfully.",
            results=results
        )

    return render_template('application/update.html', results=None)

## BORDER CROSSING ACTIONS
@app.route("/bordercrossing/query", methods=["GET", "POST"])
def bordercrossing_query():
    return render_template("bordercrossing/query.html")

@app.route('/bordercrossing/update', methods=['GET', 'POST'])
def bordercrossing_update():
    if request.method == 'POST':
        (sql, params, error) = bordercrossing.update_query(request.form)

        if error:
            return render_template('bordercrossing/update.html', message=error, results=None)

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        date = request.form.get("date")
        time = request.form.get("time")

        cursor.execute(
            "SELECT 1 FROM BorderCrossing WHERE Date = %s AND Time = %s",
            (date, time)
        )
        if not cursor.fetchone():
            return render_template('bordercrossing/update.html', message="Record does not exist.", results=None)

        cursor.execute(sql, params)
        conn.commit()

        cursor.execute(
            "SELECT * FROM BorderCrossing WHERE Date = %s AND Time = %s",
            (date, time)
        )
        results = cursor.fetchall()

        return render_template(
            'bordercrossing/update.html',
            message="Border crossing updated successfully.",
            results=results
        )

    return render_template('bordercrossing/update.html', results=None)

## NON-CITIZEN ACTIONS
@app.route("/noncitizen/query", methods=["GET", "POST"])
def noncitizen_query():
    return render_template("noncitizen/query.html")

@app.route('/noncitizen/update', methods=['GET', 'POST'])
def noncitizen_update():
    if request.method == 'POST':
        (sql, params, error) = noncitizen.update_query(request.form)

        if error:
            return render_template('noncitizen/update.html', message=error, results=None)

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        passport_id = request.form.get("passportID")

        cursor.execute(
            "SELECT 1 FROM NonCitizen WHERE PassportID = %s",
            (passport_id,)
        )
        if not cursor.fetchone():
            return render_template('noncitizen/update.html', message="Non-Citizen does not exist.", results=None)
        
        cursor.execute(sql, params)
        conn.commit()

        cursor.execute(
            "SELECT * FROM NonCitizen WHERE PassportID = %s",
            (passport_id,)
        )
        results = cursor.fetchall()

        return render_template(
            'noncitizen/update.html',
            message="Non-Citizen updated successfully.",
            results=results
        )

    return render_template('noncitizen/update.html', results=None)

if __name__ == "__main__":
    app.run(debug=True)