from flask import render_template, request, redirect, session, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from app import app, db, bcrypt, login_manager

from app.models import User, db_session, UserSchema


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_email = request.form.get('email')
        user = User.query.get(user_email)
        if user:
            input_data_password = request.form.get('password')
            if bcrypt.check_password_hash(user.password, input_data_password):
                print(user.authenticated)
                user.authenticated = True
                print(user.authenticated)
                session["email"] = user
                current_db_sessions = db_session.object_session(user)
                current_db_sessions.add(user)
                # db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect('/dashboard')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/registration', methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User(
            email=email,
            password=bcrypt.generate_password_hash(password).decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('registration.html')


@login_required
@app.route('/dashboard')
def dashboard():
    user = User.query.first()
    user_schema = UserSchema()
    output = user_schema.dump(user).data
    json_output = jsonify({"output": output})
    return render_template('dashboard.html', user=json_output)


@login_required
@app.route('/create')
def create_event():
    return render_template('eventCreate.html')
