from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)  # referencing to the current file
# database URL, other databases can be used
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)  # initialize the database

if __name__ == '__main__':
    app.run(debug=True)


class plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(200), nullable=False)
    people = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),
                             default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Task {self.id}>'


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        pass
    else:
        pass


if __name__ == '__main__':
    app.run(debug=True)
