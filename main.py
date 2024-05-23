from kaizen import KaizenApp
from flask import request, jsonify

kaizen_app = KaizenApp()

@kaizen_app.app.route('/')
def hello():
    return "<p>This is Kaizen App prototype!</p>"

@kaizen_app.app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify({"user_id": kaizen_app.get_user(user_id)})

@kaizen_app.app.route('/username/<int:user_id>', methods=['GET'])
def get_username(user_id):
    return jsonify({"username": kaizen_app.get_username(user_id)})

@kaizen_app.app.route('/email/<int:user_id>', methods=['GET'])
def get_email(user_id):
    return jsonify({"email": kaizen_app.get_email(user_id)})



@kaizen_app.app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    print(f"Received data: {data}")
    return kaizen_app.create_user(username, email)

if __name__ == '__main__':
    kaizen_app.run()
