from flask import Flask,abort
from dataModels.dataModels import db, User
from utils.dataLoaderJson import DataLLoader
import os
class KaizenApp:
    def __init__(self, testingData : bool = True ,pathJson='templates/testingData.json') -> None:
        self.app = Flask(__name__)
        self.testingData = testingData
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kaizen.db'  # Use SQLITE as the engine foor this databse file
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
        #Load the data Json for tersting purposes
        self.__cleardb__()
        self.__load_test_data__(pathJson)

    def __cleardb__(self)->None:
        try:
            db_file = os.path.join('instance/kaizen.db')
            if os.path.exists(db_file):
                os.remove(db_file)
        except Exception as e:
            raise Exception(f"File {db_file} not found!")

    def __load_test_data__(self,pathJson)->None:
        """ Load test data from a JSON file.

        Args:
            pathJson (str): Path to the JSON file containing test data.
        """
        try:
            test_data = DataLLoader(pathJson)
            #Create list of tuple to store the user and email
            self.users_data = []
            for user_data in test_data.get_data() :
                username = user_data.get('username')
                email = user_data.get('email')
                self.users_data.append((username,email))
        except Exception as e:
            print(f"Error loading test data: {e}")
    
    def isDataTesting(self)->bool:
        return self.testingData    

    def get_user(self,user_id:int)->int:
        user = User.query.get(user_id)
        if user:
            return user_id
        else:
            abort(404,f"User with ID {user_id} not found")
    
    def create_user(self,username:str='',email:str='')->str:
        with self.app.app_context():
            if self.isDataTesting():
                str_template = "User created with Id: "
                str_user = ""
                for idx,user_data in enumerate(self.users_data):
                    try:
                        new_user = User()
                        new_user.username = user_data[0]
                        new_user.email = user_data[1]
                        db.session.add(new_user) # Adds  the new_user object to the current session during the next flush operation
                        db.session.commit()# commits th current transation making any pedning changes like inserts updates or deletes permanet in the db
                        if idx == len(self.users_data) - 1:
                            str_user += f"{new_user.id}"
                        else:
                            str_user += f"{new_user.id},"
                    except Exception as e:
                        raise Exception(f"Error creating new User: {e}")
                return str_template + str_user
            else:
                new_user = User()
                new_user.username = username
                new_user.email = email

                db.session.add(new_user) # Adds  the new_user object to the current session during the next flush operation
                db.session.commit()# commits th current transation making any pedning changes like inserts updates or deletes permanet in the db
                return f"User created with Id: {new_user.id}"

    def run(self):
        self.app.run(debug=True)
    
