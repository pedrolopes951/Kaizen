from kaizen import KaizenApp
from flask import request


kaizen_app = KaizenApp()

# Decorator makes funcitons should be called whenm a request is made to the root URL '/' of the Flask
# I am telling Flask object that when a request comes in with a spcecified URL pattern like '/' index() is called
@kaizen_app.app.route('/')
def hello():
    return "<p>This is Kaizen App prototype!</p>"


#API endPoints
#User 
@kaizen_app.app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Logic to retrieve user data from the database
    return kaizen_app.get_user(user_id)

@kaizen_app.app.route('/user', methods=['POST'])
def create_user():
    # Logic to create a new user in the database
    data = request.json  # Assuming JSON data is sent in the request
    # Process data and save it to the database
    username = data.get('username')
    email = data.get('email')
    return kaizen_app.create_user(username,email)

#TrainingSession 
@kaizen_app.app.route('/training_sessions')
def trainingSession():
    return "<p>Training session Page</p>"
#AttendanceRecord 
@kaizen_app.app.route('/attendance_record')
def attendanceRecord():
    return "<p>Attendance record Page</p>"
#Note 
@kaizen_app.app.route('/note')
def note():
    return "<p>Notes Page</p>"



if __name__ == '__main__':
    kaizen_app.run()

