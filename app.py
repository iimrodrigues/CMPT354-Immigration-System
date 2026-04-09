from flask import Flask, render_template, redirect, url_for, request
from db import get_connection

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

    return f"You selected {entity} + {action}"

## VISA ACTIONS
@app.route("/visa/query", methods=["GET", "POST"])
def visa_query():
    return render_template("visa/query.html")

## PERMIT ACTIONS
@app.route("/permit/query", methods=["GET", "POST"])
def permit_query():
    return render_template("permit/query.html")

## APPLICATION ACTIONS
@app.route("/application/query", methods=["GET", "POST"])
def application_query():
    return render_template("application/query.html")

if __name__ == "__main__":
    app.run(debug=True)