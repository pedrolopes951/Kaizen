import os
from flask import Flask, abort, request
from dataModels.dataModels import db, User
from utils.dataLoaderJson import DataLLoader

class KaizenApp:
    def __init__(self, testingData: bool = True, pathJson='templates/testingData.json') -> None:
        self.app = Flask(__name__)
        self.testingData = testingData

        # Get the absolute path for the database file
        db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'kaizen.db')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        self.app.config['SECRET_KEY'] = os.urandom(24)  # Set a random secret key
        db.init_app(self.app)
        with self.app.app_context():
            self.__cleardb()
            db.create_all()
        # Load the data JSON for testing purposes
        self.users_data = []  # Initialize users_data
        self.__load_test_data(pathJson)

    def __cleardb(self) -> None:
        db_file = os.path.join(self.app.instance_path, 'kaizen.db')
        if os.path.exists(db_file):
            os.chmod(db_file, 0o666)  # Set file to be writable
            os.remove(db_file)

    def __load_test_data(self, pathJson) -> None:
        try:
            test_data = DataLLoader(pathJson)
            for user_data in test_data.get_data():
                username = user_data.get('username')
                email = user_data.get('email')
                self.users_data.append((username, email))
        except Exception as e:
            print(f"Error loading test data: {e}")

    def isDataTesting(self) -> bool:
        return self.testingData    

    def get_user(self, user_id: int) -> int:
        user = User.query.get(user_id)
        if user:
            return user_id
        else:
            abort(404, f"User with ID {user_id} not found")

    def get_username(self, user_id: int) -> str:
        user = User.query.get(user_id)
        if user:
            return  user.username
        else:
            abort(404, f"username with ID {user_id} not found")

    def get_email(self, user_id: int) -> str:
        user = User.query.get(user_id)
        if user:
            return user.email
        else:
            abort(404, f"email with ID {user_id} not found")

    def create_user(self, username: str = '', email: str = '') -> tuple:
        with self.app.app_context():
            if self.isDataTesting() and not username and not email:
                str_template = "User created with Id: "
                str_user = ""
                for idx, user_data in enumerate(self.users_data):
                    try:
                        existing_user = User.query.filter(
                            (User.email == user_data[1]) | (User.username == user_data[0])
                        ).first()
                        if existing_user:
                            continue  # Skip if user already exists
                        new_user = User(username=user_data[0], email=user_data[1])
                        db.session.add(new_user)
                        db.session.commit()
                        if idx == len(self.users_data) - 1:
                            str_user += f"{new_user.id}"
                        else:
                            str_user += f"{new_user.id},"
                    except Exception as e:
                        raise Exception(f"Error creating new User: {e}")
                return str_template + str_user, 201
            else:
                existing_user = User.query.filter(
                    (User.email == email) | (User.username == username)
                ).first()
                if existing_user:
                    return f"Error: User with username {username} or email {email} already exists.", 400
                new_user = User(username=username, email=email)
                db.session.add(new_user)
                db.session.commit()
                return f"User created with Id: {new_user.id}", 201

            
    def update_user(self, user_id: int, username: str, email: str) -> str:
        with self.app.app_context():
            user = User.query.get(user_id)
            if user:
                user.username = username
                user.email = email
                db.session.commit()
                return f"User with Id: {user_id} updated"
            else:
                abort(404, f"User with ID {user_id} not found")

    def delete_user(self, user_id: int) -> str:
        with self.app.app_context():
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return f"User with Id: {user_id} deleted"
            else:
                abort(404, f"User with ID {user_id} not found")

    def run(self):
        self.app.run(debug=True)
