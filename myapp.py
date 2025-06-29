from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import json

app = Flask(__name__)  # referencing to the current file
# database URL, other databases can be used
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)  # initialize the database


class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(200), nullable=False)
    people = db.Column(db.Text) # store as a json string
    plan_date = db.Column(db.DateTime, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),
                             default=lambda: datetime.now(timezone.utc))
    
    def set_people(self, people_list):
        self.people = json.dumps(people_list)
    def get_people(self):
        return json.loads(self.people)
    
    def __repr__(self):
        return f'<Plan {self.id}>'


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        activity_content = request.form['activity']
        people_content = request.form['people']
        plan_date_str = request.form['date']
        
        plan_date = datetime.fromisoformat(plan_date_str)
        if plan_date <= datetime.now():
            return "Unless it's today or you can go back in time.... pick a future date"
        
        people_list = [p.strip() for p in people_content.split(',') if p.strip()]
        
        new_activity = Plan(activity=activity_content, plan_for = plan_date)
        new_activity.set_people(people_list)
        
        try:
            db.session.add(new_activity)
            db.session.commit()
            return redirect('/')
        except:
            "Err.. trouble adding the activity to the plan"
    else:
        activities = Plan.query.order_by(Plan.date_created).all()
        return render_template('index.html', activities = activities)


if __name__ == '__main__':
    app.run(debug=True)
