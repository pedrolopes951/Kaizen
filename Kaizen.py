from flask import Flask
from flask_sqlalchemy import SQLAlchemy



class KaizenApp:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///keizen.db' # SQLite database file path
        self.db = SQLAlchemy(self.app)

        # Encapsulate the database model within the application class
        class User(self.db.Model): # User class inherits from self.db.Model
            id = self.db.Column(self.db.Integer,primary_key = True)
            username = self.db.Column(self.db.String(80), unique=True, nullable=False)
            email = self.db.Column(self.db.String(120), unique=True, nullable=False)

    def run(self):
        self.app.run(debug=True)


