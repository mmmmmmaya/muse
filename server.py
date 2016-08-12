import json
import os

from flask import flash, Flask, jsonify, redirect, render_template, request, session
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest

from countries import countries
from model import connect_to_db, db, KeyPress, Recording, User
from utils.authentication import add_session_info, attempt_login, remove_session_info
from utils.general import ALERT_COLORS, flash_message, get_current_user, is_logged_in
from utils.playback import get_recording_by_id
from utils.record import add_keypress_to_db_session, add_recording_to_db, process_raw_keypresses
from utils.register import all_fields_filled, register_user

app = Flask(__name__)
app.secret_key = os.environ['FLASK_APP_SECRET_KEY']


@app.route('/')
def index():
    """Show main music-making page to user."""

    return render_template('index.html')


@app.route('/fetch_recording/<int:recording_id>')
def fetch_recording(recording_id):
    """Fetch recording with matching recording id from database."""

    recording = get_recording_by_id(recording_id)
    keypresses = None

    if recording:
        keypresses = recording.keypresses

    if keypresses:
        response = ({
            'status': 'success',
            'content': keypresses
        })
    else:
        response = ({
            'status': 'failure',
            'content': None
        })

    return jsonify(response)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Show login page."""

    if request.method == 'GET':
        response = render_template('login.html')

    elif request.method == 'POST':
        # TODO add option for redirect url in case user was trying to
        # access a specific page before they got sent to login

        email = request.form.get('email')
        password = request.form.get('password')

        response = attempt_login(email, password)

    return response


@app.route('/logout')
def logout():
    """Remove user info from browser session."""

    if is_logged_in():
        remove_session_info()

    flash_message('You were successfully logged out.', ALERT_COLORS['green'])

    return redirect('/')


@app.route('/profile')
def profile():
    """Return the profile page for the logged in user."""

    if is_logged_in():
        user = get_current_user()

        if user:
            response = render_template('profile.html',
                                       user=user)
        else:
            # in this case, there is a user_id in the session, but that
            # user_id is not in the db. If this happens, we'll log the
            # user out and then ask them to try again.

            remove_session_info()
            flash_message('There was an error. Please log in and try again.',
                          ALERT_COLORS['red'])
            response = redirect('/login')

    else:
        flash_message('Please log in to view your profile.',
                      ALERT_COLORS['yellow'])
        response = redirect('/login')

    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Show the registration page."""

    if request.method == 'GET':
        if is_logged_in():
            flash_message('You are already logged in.', ALERT_COLORS['yellow'])
            response = redirect('/')
        else:
            response = render_template('register.html',
                                       countries=countries)

    elif request.method == 'POST':
        form = request.form

        name = form.get('name')
        email = form.get('email')
        password = form.get('password')
        zipcode = form.get('zipcode')
        country = form.get('country')

        if all_fields_filled(name, email, password):
            response = register_user(name,
                                     email,
                                     password,
                                     zipcode,
                                     country)
        else:
            response = BadRequest('You are missing a field necessary for registration.')

    return response


@app.route('/save_recording', methods=['POST'])
def save_recording():
    """Save recording data to the database."""

    if is_logged_in():
        keypress_json = request.form.get('keypresses', None)
        raw_keypress_list = json.loads(keypress_json)

        if raw_keypress_list:
            recording_id = add_recording_to_db()
            process_raw_keypresses(raw_keypress_list, recording_id)

        return jsonify({'status': 'saved'})

    else:
        return jsonify({'status': 'login_required'})


if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    app.run(host='0.0.0.0')
