from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from kaizen import KaizenApp

kaizen_app = KaizenApp()

kaizen_app = KaizenApp()

@kaizen_app.app.route('/')
def hello():
    return "<p>This is Kaizen App prototype!</p>"

@kaizen_app.app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify(kaizen_app.get_user(user_id))

@kaizen_app.app.route('/user', methods=['POST'])
def create_user():
    data = request.json if request.json else {}
    username = data.get('username', '')
    email = data.get('email', '')
    print(f"Received data: {data}")
    return kaizen_app.create_user(username, email)

@kaizen_app.app.route('/create_user', methods=['GET', 'POST'])
def create_user_form():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        result, status_code = kaizen_app.create_user(username, email)
        if status_code == 400:
            flash(result, 'error')
        else:
            flash(result, 'success')
        return redirect(url_for('create_user_form'))
    return render_template('create_user.html')

@kaizen_app.app.route('/update_user', methods=['GET', 'POST'])
def update_user_form():
    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
        username = request.form.get('username')
        email = request.form.get('email')
        kaizen_app.update_user(user_id, username, email)
        return redirect(url_for('hello'))
    return render_template('update_user.html')

@kaizen_app.app.route('/delete_user', methods=['GET', 'POST'])
def delete_user_form():
    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
        kaizen_app.delete_user(user_id)
        return redirect(url_for('hello'))
    return render_template('delete_user.html')

@kaizen_app.app.route('/username/<int:user_id>', methods=['GET'])
def get_username(user_id):
    return jsonify({"username": kaizen_app.get_username(user_id)})

@kaizen_app.app.route('/email/<int:user_id>', methods=['GET'])
def get_email(user_id):
    return jsonify({"email": kaizen_app.get_email(user_id)})

if __name__ == '__main__':
    kaizen_app.run()