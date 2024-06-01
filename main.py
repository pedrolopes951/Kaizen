from flask import request, jsonify, render_template, redirect, url_for, flash
from kaizen import KaizenApp

kaizen_app = KaizenApp()

@kaizen_app.app.route('/')
def hello():
    return "<p>This is Kaizen App prototype!</p>"

# User Routes
@kaizen_app.app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify(kaizen_app.get_user(user_id))

@kaizen_app.app.route('/users', methods=['GET'])
def list_users():
    return jsonify(kaizen_app.list_users())

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

# Training Session Routes
@kaizen_app.app.route('/training_session/<int:session_id>', methods=['GET'])
def get_training_session(session_id):
    return jsonify(kaizen_app.get_training_session(session_id))

@kaizen_app.app.route('/training_sessions', methods=['GET'])
def list_training_sessions():
    return jsonify(kaizen_app.list_training_sessions())

@kaizen_app.app.route('/create_training_session', methods=['GET', 'POST'])
def create_training_session():
    if request.method == 'POST':
        date = request.form.get('date')
        result, status_code = kaizen_app.create_training_session(date)
        if status_code == 400:
            flash(result, 'error')
        else:
            flash(result, 'success')
        return redirect(url_for('create_training_session'))
    return render_template('create_training_session.html')

@kaizen_app.app.route('/update_training_session', methods=['GET', 'POST'])
def update_training_session_form():
    if request.method == 'POST':
        session_id = int(request.form.get('session_id'))
        date = request.form.get('date')
        kaizen_app.update_training_session(session_id, date)
        return redirect(url_for('hello'))
    return render_template('update_training_session.html')

@kaizen_app.app.route('/delete_training_session', methods=['GET', 'POST'])
def delete_training_session_form():
    if request.method == 'POST':
        session_id = int(request.form.get('session_id'))
        kaizen_app.delete_training_session(session_id)
        return redirect(url_for('hello'))
    return render_template('delete_training_session.html')

# Attendance Record Routes
@kaizen_app.app.route('/attendance_record/<int:record_id>', methods=['GET'])
def get_attendance_record(record_id):
    return jsonify(kaizen_app.get_attendance_record(record_id))

@kaizen_app.app.route('/attendance_records', methods=['GET'])
def list_attendance_records():
    return jsonify(kaizen_app.list_attendance_records())

@kaizen_app.app.route('/create_attendance_record', methods=['GET', 'POST'])
def create_attendance_record():
    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
        session_id = int(request.form.get('session_id'))
        result, status_code = kaizen_app.create_attendance_record(user_id, session_id)
        if status_code == 400:
            flash(result, 'error')
        else:
            flash(result, 'success')
        return redirect(url_for('create_attendance_record'))
    return render_template('create_attendance_record.html')

@kaizen_app.app.route('/update_attendance_record', methods=['GET', 'POST'])
def update_attendance_record_form():
    if request.method == 'POST':
        record_id = int(request.form.get('record_id'))
        user_id = int(request.form.get('user_id'))
        session_id = int(request.form.get('session_id'))
        kaizen_app.update_attendance_record(record_id, user_id, session_id)
        return redirect(url_for('hello'))
    return render_template('update_attendance_record.html')

@kaizen_app.app.route('/delete_attendance_record', methods=['GET', 'POST'])
def delete_attendance_record_form():
    if request.method == 'POST':
        record_id = int(request.form.get('record_id'))
        kaizen_app.delete_attendance_record(record_id)
        return redirect(url_for('hello'))
    return render_template('delete_attendance_record.html')

# Note Routes
@kaizen_app.app.route('/note/<int:note_id>', methods=['GET'])
def get_note(note_id):
    return jsonify(kaizen_app.get_note(note_id))

@kaizen_app.app.route('/notes', methods=['GET'])
def list_notes():
    return jsonify(kaizen_app.list_notes())

@kaizen_app.app.route('/create_note', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
        content = request.form.get('content')
        result, status_code = kaizen_app.create_note(user_id, content)
        if status_code == 400:
            flash(result, 'error')
        else:
            flash(result, 'success')
        return redirect(url_for('create_note'))
    return render_template('create_note.html')

@kaizen_app.app.route('/update_note', methods=['GET', 'POST'])
def update_note_form():
    if request.method == 'POST':
        note_id = int(request.form.get('note_id'))
        content = request.form.get('content')
        kaizen_app.update_note(note_id, content)
        return redirect(url_for('hello'))
    return render_template('update_note.html')

@kaizen_app.app.route('/delete_note', methods=['GET', 'POST'])
def delete_note_form():
    if request.method == 'POST':
        note_id = int(request.form.get('note_id'))
        kaizen_app.delete_note(note_id)
        return redirect(url_for('hello'))
    return render_template('delete_note.html')

if __name__ == '__main__':
    kaizen_app.run()
