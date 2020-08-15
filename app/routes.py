import flask_login
from flask import render_template, request, redirect, session, flash, url_for, g
from flask_login import login_user, login_required, logout_user, current_user
from datetime import timedelta
from app import app, db, bcrypt
import flask

from app.models import User, db_session


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
    flask.session.modified = True
    flask.g.user = flask_login.current_user


@app.route('/', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == "POST":
        user_email = request.form.get('email')
        user = User.query.get(user_email)
        input_data_password = request.form.get('password')
        if user is not None and bcrypt.check_password_hash(user.password, input_data_password):
            user.authenticated = True
            current_db_sessions = db_session.object_session(user)
            current_db_sessions.add(user)
            db.session.commit()
            session.permanent = True
            login_user(user, remember=False)
            if not current_user.is_active():
                flash('Detected user is inactive.')
            return redirect(url_for('dashboard'))
    return render_template('login.html', title="Login")


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
    return render_template('registration.html', title="Registration")


@login_required
@app.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('dashboard.html', title="Dashboard")


@login_required
@app.route('/create_event')
def create_event():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('createEvent.html', title="Crete event")
