from flask_sqlalchemy import SQLAlchemy

#Init SQLAlchemy object, use to interacting with the database within the Flask application.
db = SQLAlchemy()


# Different Databae Models
class User(db.Model):
    #Each attribute represents Columns on the Table
    id = db.Column(db.Integer, primary_key=True)
    # nullable=False specifies that a column cannot contain null values (i.e., it must always have a value).
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class TrainingSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)

class AttendanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id is a foreign key column in the AttendanceRecord table, which references the id column of the User table.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('training_session.id'), nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

