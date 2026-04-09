from flask import Flask, render_template, request
from db import get_connection

app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/select", methods=["POST"])
def select():
    entity = request.form.get("entity")
    action = request.form.get("action")

    print(entity, action)

    return f"You selected {entity} + {action}"