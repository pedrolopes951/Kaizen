from flask import Flask
from dataModels.dataModels import db

class KaizenApp:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kaizen.db'  # Use SQLITE as the engine foor this databse file
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()


    def run(self):
        self.app.run(debug=True)
