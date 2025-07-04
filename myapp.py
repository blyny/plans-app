from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import json
import requests
load_dotenv()

TOKEN = os.getenv("webhook")
app = Flask(__name__)  # referencing to the current file
# database URL, other databases can be used
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)  # initialize the database


class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(300), nullable=False)
    people = db.Column(db.Text)  # store as a json string
    plan_date = db.Column(db.DateTime, nullable=False)

    def set_people(self, people_list):
        self.people = json.dumps(people_list)

    def get_people(self):
        return json.loads(self.people)

    def __repr__(self):
        return f'<Plan {self.id}>'


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        pass
    else:
        activities = Plan.query.order_by(Plan.plan_date).all()
        return render_template('index.html', activities=activities)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        activity_content = request.form['activity']
        location_content = request.form['location']
        people_content = request.form['people']
        plan_date_str = request.form['plan_for']

        if plan_date_str:
            plan_date = datetime.fromisoformat(plan_date_str)
            if plan_date <= datetime.now():
                return "Unless it's today or you can go back in time.... pick a future date"
        else:
            return "Did you fill everything out?"

        people_list = [p.strip()
                       for p in people_content.split(',') if p.strip()]

        new_activity = Plan(activity=activity_content,
                            location=location_content, plan_date=plan_date)
        new_activity.set_people(people_list)

        try:
            db.session.add(new_activity)
            db.session.commit()
            send_discord_notification()
            return redirect('/')
        except:
            "Err.. trouble adding the activity to the plan"
    else:
        return render_template('create.html')


@app.route('/delete/<int:id>')
def delete(id):
    plan_to_delete = Plan.query.get_or_404(id)
    try:
        db.session.delete(plan_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "We cant delete it?"


def send_discord_notification():
    webhook_url = TOKEN
    data = {
        "content": f"📆Test!!"
    }
    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:
        print("Notification sent!")
    else:
        print(f"Failed to send: {response.status_code}, {response.text}")


if __name__ == '__main__':
    app.run(debug=True)
