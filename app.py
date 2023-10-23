from flask import Flask, render_template, request
from cs50 import SQL

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Set-up DB
db = SQL("sqlite:///development.db")

@app.route("/")
def index():
    user = db.execute("SELECT * FROM users")
    return render_template("index.html", user=user)

@app.route("/reports")
def reports():
    user = db.execute("SELECT * FROM users")
    return render_template("reports.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)
