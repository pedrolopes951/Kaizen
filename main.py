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

@kaizen_app.app.route('/list_training_sessions', methods=['GET'])
def list_training_sessions():
    sessions = kaizen_app.list_training_sessions()
    return render_template('list_training_sessions.html', sessions=sessions)

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

@kaizen_app.app.route('/list_attendance_records', methods=['GET'])
def list_attendance_records():
    records = kaizen_app.list_attendance_records()
    return render_template('list_attendance_records.html', records=records)

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

@kaizen_app.app.route('/list_notes', methods=['GET'])
def list_notes():
    notes = kaizen_app.list_notes()
    return render_template('list_notes.html', notes=notes)

@kaizen_app.app.route('/user_details/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    return jsonify(kaizen_app.get_user_details(user_id))

@kaizen_app.app.route('/update_note', methods=['GET', 'POST'])
def update_note_form():
    if request.method == 'POST':
        note_id = int(request.form.get('note_id'))
        content = request.form.get('content')
        result = kaizen_app.update_note(note_id, content)
        flash(result, 'success')
        return redirect(url_for('update_note_form'))
    return render_template('update_note.html')

@kaizen_app.app.route('/delete_note', methods=['GET', 'POST'])
def delete_note_form():
    if request.method == 'POST':
        note_id = int(request.form.get('note_id'))
        result = kaizen_app.delete_note(note_id)
        flash(result, 'success')
        return redirect(url_for('delete_note_form'))
    return render_template('delete_note.html')

@kaizen_app.app.route('/training_session_details/<int:session_id>', methods=['GET'])
def get_training_session_details(session_id):
    return jsonify(kaizen_app.get_training_session_details(session_id))

if __name__ == '__main__':
    kaizen_app.run()