from flask import Flask, render_template, request
from cs50 import SQL
from wtforms import Form, StringField,TextAreaField, RadioField, validators
from datetime import datetime

from markupsafe import Markup

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Set-up DB
db = SQL("sqlite:///incidents.db")

# Form Class for WTForms
class ReportForm(Form):
    uName = StringField("Name", validators=[validators.InputRequired(), validators.Length(min=2, max=10)])

    plate = StringField("License Plate", validators=[validators.DataRequired("Required"), validators.Regexp(r'^[A-Z]{2,3}\d{2,4}[A-Z]$', message="Invalid license plate")])

    content = TextAreaField("Report", validators=[validators.InputRequired(), validators.length(max=200)])

    type = RadioField("Type", validators=[validators.InputRequired()], choices=[("Good", Markup('<i class="fa-regular fa-face-laugh-beam fa-xl"></i>')),
    ("Bad", Markup('<i class="fa-regular fa-face-frown-open fa-xl"></i>')),
    ("Neutral", Markup('<i class="fa-regular fa-face-meh fa-xl"></i>'))
    ])

# Routes & Controller
@app.route("/", methods=["GET", "POST"])
def index():
    form = ReportForm(request.form)

    if request.method == "GET":
        print('GET')
    if request.method == "POST" and form.validate():
        db.execute("INSERT INTO incidents (name, plate, content, type) VALUES (?, ?, ?, ?)", form.uName.data, form.plate.data, form.content.data, form.type.data)
        form = ReportForm(formdata=None)

    incidents = _get_recent_incidents()
    top_plates = _get_top_plates()
    top_count = _get_top_count()

    return render_template("index.html", form=form, incidents=incidents, top_plates=top_plates, top_count=top_count)

# @app.route("/reports")
# def reports():
#     user = db.execute("SELECT * FROM users")
#     return render_template("reports.html", user=user)

# Private Methods
def _get_recent_incidents():
    incidents = db.execute("SELECT * FROM incidents ORDER BY id DESC LIMIT 5;")
    formatted_results = []
    for row in incidents:
        created_at_str = row['created_at']
        created_at_datetime = datetime.strptime(created_at_str, '%Y-%m-%d %H:%M:%S')
        formatted_created_at = created_at_datetime.strftime('%b %d, %Y %I:%M %p')
        formatted_row = {**row, 'formatted_created_at': formatted_created_at}
        formatted_results.append(formatted_row)
    return formatted_results

def _get_top_plates():
    return db.execute("SELECT plate, COUNT(*) AS good_count FROM incidents WHERE type = 'Good' GROUP BY plate ORDER BY good_count DESC LIMIT 5;")

def _get_top_count():
    return db.execute("SELECT COUNT(*) AS top_count FROM incidents WHERE type = 'Good' GROUP BY plate ORDER BY top_count DESC LIMIT 1;")[0]['top_count']

if __name__ == "__main__":
    app.run(debug=True)
