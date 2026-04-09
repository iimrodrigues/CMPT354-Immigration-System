from flask import Flask, render_template, request
from db import get_connection

app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- NON-CITIZEN ----------------
@app.route("/noncitizen", methods=["GET", "POST"])
def noncitizen():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    results = []

    if request.method == "POST":
        city = request.form.get("city")

        cursor.execute("""
            SELECT * FROM NonCitizen
            WHERE City = %s
        """, (city,))

        results = cursor.fetchall()

    return render_template("noncitizen.html", results=results)


# ---------------- VISA ----------------
@app.route("/visa", methods=["GET", "POST"])
def visa():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    results = []

    if request.method == "POST":
        passport = request.form.get("passport")

        cursor.execute("""
            SELECT * FROM Visa
            WHERE PassportID = %s
        """, (passport,))

        results = cursor.fetchall()

    return render_template("visa.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)