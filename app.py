from flask import Flask, render_template, request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Set-up DB

@app.route("/")
def index():
    return render_template("index.html")
