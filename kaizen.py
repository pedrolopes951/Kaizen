import os
from flask import Flask, abort, request
from dataModels.dataModels import db, User, TrainingSession,AttendanceRecord,Note
from utils.dataLoaderJson import DataLLoader
from datetime import datetime


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
    
    def get_user_details(self, user_id: int) -> dict:
        with self.app.app_context():
            user = User.query.get(user_id)
            if not user:
                abort(404, f"User with ID {user_id} not found")
            attendance_records = AttendanceRecord.query.filter_by(user_id=user_id).all()
            notes = Note.query.filter_by(user_id=user_id).all()
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "attendance_records": [{"id": record.id, "session_id": record.session_id} for record in attendance_records],
                "notes": [{"id": note.id, "content": note.content} for note in notes]
            }
    
    def update_note(self, note_id: int, content: str) -> str:
        with self.app.app_context():
            note = Note.query.get(note_id)
            if note:
                note.content = content
                db.session.commit()
                return f"Note with Id: {note_id} updated"
            else:
                abort(404, f"Note with ID {note_id} not found")
            
    def create_training_session(self, date: str) -> str:
        with self.app.app_context():
            try:
                session_date = datetime.strptime(date, '%Y-%m-%d').date()
                new_session = TrainingSession(date=session_date)
                db.session.add(new_session)
                db.session.commit()
                return f"Training session created with Id: {new_session.id}", 201
            except Exception as e:
                raise Exception(f"Error creating new Training Session: {e}")

    def list_training_sessions(self) -> list:
        with self.app.app_context():
            sessions = TrainingSession.query.all()
            return [{"id": session.id, "date": session.date.strftime('%Y-%m-%d')} for session in sessions]

    def create_attendance_record(self, user_id: int, session_id: int) -> str:
        with self.app.app_context():
            try:
                new_record = AttendanceRecord(user_id=user_id, session_id=session_id)
                db.session.add(new_record)
                db.session.commit()
                return f"Attendance record created with Id: {new_record.id}", 201
            except Exception as e:
                raise Exception(f"Error creating new Attendance Record: {e}")

    def list_attendance_records(self) -> list:
        with self.app.app_context():
            records = AttendanceRecord.query.all()
            return [{"id": record.id, "user_id": record.user_id, "session_id": record.session_id} for record in records]

            
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
                
    def create_note(self, user_id: int, content: str) -> str:
        with self.app.app_context():
            try:
                new_note = Note(user_id=user_id, content=content)
                db.session.add(new_note)
                db.session.commit()
                return f"Note created with Id: {new_note.id}", 201
            except Exception as e:
                raise Exception(f"Error creating new Note: {e}")

    def list_notes(self) -> list:
        with self.app.app_context():
            notes = Note.query.all()
            return [{"id": note.id, "user_id": note.user_id, "content": note.content} for note in notes]
        
    def delete_note(self, note_id: int) -> str:
        with self.app.app_context():
            note = Note.query.get(note_id)
            if note:
                db.session.delete(note)
                db.session.commit()
                return f"Note with Id: {note_id} deleted"
            else:
                abort(404, f"Note with ID {note_id} not found")
                
    def get_training_session_details(self, session_id: int) -> dict:
        with self.app.app_context():
            session = TrainingSession.query.get(session_id)
            if not session:
                abort(404, f"Training session with ID {session_id} not found")
            attendance_records = AttendanceRecord.query.filter_by(session_id=session_id).all()
            attendees = [User.query.get(record.user_id) for record in attendance_records]
            return {
                "id": session.id,
                "date": session.date.strftime('%Y-%m-%d'),
                "attendees": [{"id": attendee.id, "username": attendee.username, "email": attendee.email} for attendee in attendees if attendee]
            }


    def run(self):
        self.app.run(debug=True)
