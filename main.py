from kaizen import KaizenApp
from flask import request

kaizen_app = KaizenApp()

@kaizen_app.app.route('/')
def hello():
    return "<p>This is Kaizen App prototype!</p>"

@kaizen_app.app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return kaizen_app.get_user(user_id)

@kaizen_app.app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    return kaizen_app.create_user(username, email)

if __name__ == '__main__':
    kaizen_app.run()
