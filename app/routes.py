import flask_login
from flask import render_template, request, redirect, session, flash, url_for, g, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from datetime import timedelta, datetime
from app import app, db, bcrypt
import flask
from app import models

from app.models import User, db_session, Event


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
            user.active = True
            current_db_sessions = db_session.object_session(user)
            current_db_sessions.add(user)
            current_db_sessions.commit()
            session.permanent = True
            login_user(user, remember=False)
            if not current_user.is_active():
                flash('Detected user is inactive.')
            return redirect(url_for('dashboard'))
    return render_template('login.html', title="Login")


@app.route('/logout')
def logout():
    user = User.query.get(current_user.email)
    user.authenticated = False
    current_db_sessions = db_session.object_session(user)
    current_db_sessions.add(user)
    current_db_sessions.commit()
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
    page = request.args.get('page', 1, type=int)
    events = db.session.query(models.Event).paginate(page, 4, False)
    next_url = url_for('dashboard', page=events.next_num) if events.has_next else None
    prev_url = url_for('dashboard', page=events.prev_num) if events.has_prev else None
    isEvent = user_have_events()
    return render_template('dashboard.html', title="Dashboard", events=events.items, isEvent=isEvent,
                           next_url=next_url, prev_url=prev_url)


def user_have_events():
    events = db.session.query(Event).all()
    for event in events:
        if event.author_email == current_user.email:
            return True
        else:
            return False


@login_required
@app.route('/create_event')
def create_event():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == "POST":
        redirect(url_for('logout'))
    return render_template('createEvent.html', title="Crete event")


@app.route('/subject_description', methods=["POST"])
def update():
    if request.method == "POST":
        author = current_user.email
        data = {
            "subject": '',
            "description": '',
            "start_time": '',
            "end_time": ''
        }

        if request.form['subject']:
            data['subject'] = request.form['subject']
        if request.form['description']:
            data['description'] = request.form['description']
        if request.form['start_time']:
            data['start_time'] = request.form['start_time']
        if request.form['end_time']:
            data['end_time'] = request.form['end_time']

        if data["subject"] and data['description'] and data['start_time'] and data['end_time']:
            event = Event(subject=data['subject'], description=data['description'], author=User.query.get(author),
                          start_time=datetime.strptime(data['start_time'], "%Y-%m-%d").date(),
                          end_time=datetime.strptime(data['end_time'], "%Y-%m-%d").date())
            current_db_sessions = db_session.object_session(current_user)
            current_db_sessions.add(event)
            current_db_sessions.commit()
            return jsonify(data)
    return jsonify({'result': 'error'})


@app.route('/events_list', methods=["GET"])
def events_list():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    events = Event.query.all()
    return render_template('eventList.html', title='Event List', events=events)


@app.route('/event_edit/<int:event_id>', methods=["GET", "POST"])
def event_edit(event_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    current_db_sessions = db_session.object_session(current_user)
    event = current_db_sessions.query(Event).filter(Event._id == int(event_id)).first()
    if request.method == "POST":
        new_subject = request.form.get('new_subject')
        new_desc = request.form.get('new_description')
        new_start_time = request.form.get('new_start_time')
        new_end_time = request.form.get('new_end_time')
        if (new_subject and new_desc) and (not new_start_time and not new_end_time):
            event.subject = new_subject
            event.description = new_desc
            current_db_sessions.add(event)
            current_db_sessions.commit()
        else:
            event.subject = new_subject
            event.description = new_desc
            event.start_time = datetime.strptime(new_start_time, "%Y-%m-%d").date()
            event.end_time = datetime.strptime(new_end_time, "%Y-%m-%d").date()
            current_db_sessions.add(event)
            current_db_sessions.commit()
        return redirect(url_for('dashboard'))
    return render_template('eventEdit.html', title='Edit event', event=event)
