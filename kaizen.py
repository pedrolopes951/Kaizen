from flask import Flask,abort
from dataModels.dataModels import db, User

class KaizenApp:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kaizen.db'  # Use SQLITE as the engine foor this databse file
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
    
    def get_user(self,user_id:int)->int:
        user = User.query.get(user_id)
        if user:
            return user_id
        else:
            abort(404,f"User with ID {user_id} not found")
    
    def create_user(self,username:str,email:str)->str:
        if not username or not email:
            return "Username and email are requiered",400
        
        new_user = User()
        new_user.username = username
        new_user.email = email


        db.session.add(new_user) # Adds  the new_user object to the current session during the next flush operation
        db.session.commit()# commits th current transation making any pedning changes like inserts updates or deletes permanet in the db
        return f"User created with Id: {new_user.id}"
    
    def run(self):
        self.app.run(debug=True)
    
