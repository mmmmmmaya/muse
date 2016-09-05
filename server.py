import json
import os

from flask import flash, Flask, g, jsonify, redirect, render_template, request
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest

from countries import countries
from model import connect_to_db, db, KeyPress, Recording, User
from utils.authentication import attempt_login, remove_session_info
from utils.edit import delete_recording_by_id, rename_recording, toggle_recording_visibility
from utils.general import ALERT_COLORS, flash_message, get_current_user, is_logged_in
from utils.playback import (add_view_to_db, get_arrow_list, get_popular_recordings,
                            get_recording_by_id, make_keypress_list,
                            recording_belongs_to_user, recording_is_public)
from utils.record import add_keypress_to_db_session, add_recording_to_db, process_raw_keypresses
from utils.register import all_fields_filled, register_user, update_account_info

app = Flask(__name__)
app.secret_key = os.environ['FLASK_APP_SECRET_KEY']
JS_TESTING_MODE = False


@app.before_request
def add_tests():
    g.jasmine_tests = JS_TESTING_MODE


@app.route('/', methods=['GET', 'POST'])
def index():
    """Show main music-making page to user."""

    konami = None

    if request.method == 'POST':
        konami = request.form.get('konami')

    return render_template('index.html',
                           konami=konami)


@app.route('/account')
def account():
    """Show account details."""

    user = get_current_user()

    if user:
        response = render_template('account.html',
                                   user=user,
                                   countries=countries)

    else:
        flash_message('Please log in to view your account.',
                      ALERT_COLORS['yellow'])
        response = redirect('/login')

    return response


@app.route('/delete', methods=['POST'])
def delete():
    """Delete a recording from the db."""

    recording_id = request.form.get('recording_id')

    if recording_id:
        if recording_belongs_to_user(recording_id):
            delete_recording_by_id(recording_id)

            response = jsonify({"status": "success",
                                "id": recording_id})

        else:
            flash_message('Recording can only be deleted by recording author.',
                          ALERT_COLORS['red'])
            response = redirect('/recordings')

    else:
        response = jsonify({'status': 'malformed request'})

    return response


@app.route('/fetch_konami')
def fetch_konami():
    """Return keypresses for konami easter egg."""

    arrows = get_arrow_list()

    if arrows:
        response = {
            'status': 'success',
            'content': arrows
        }

    else:
        response = {
            'status': 'failure',
            'content': None
        }

    return jsonify(response)


@app.route('/fetch_recording/<int:recording_id>')
def fetch_recording(recording_id):
    """Fetch recording with matching recording id from database."""

    recording = get_recording_by_id(recording_id)
    keypresses = None

    if recording:
        keypresses = make_keypress_list(recording.keypresses)

    if keypresses:
        response = {
            'status': 'success',
            'content': keypresses
        }

    else:
        response = {
            'status': 'failure',
            'content': None
        }

    return jsonify(response)


@app.route('/listen/<string:recording_id>')
def listen(recording_id):
    """Playback a recording, given a recording's id."""

    if recording_is_public(recording_id) or recording_belongs_to_user(recording_id):
        response = render_template('listen.html',
                                   recording_id=recording_id)

    else:
        flash_message('It looks like that recording is private or does not exist.',
                      ALERT_COLORS['red'])
        response = redirect('/')

    return response


@app.route('/log_view', methods=['POST'])
def log_view():
    """Store information about recording views."""
    recording_id = request.form.get('recording_id')
    ip_address = request.form.get('ip_address')

    if recording_id:
        add_view_to_db(recording_id, ip_address)
        response = {'status': 'success'}

    else:
        response = {'status': 'malformed request'}

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

    return redirect('/login')


@app.route('/popular')
def popular():
    """Return a page of popular songs."""

    popular_recordings = get_popular_recordings()

    return render_template('popular.html',
                           popular_recordings=popular_recordings)


@app.route('/recordings')
def recordings():
    """Return the recordings page for the logged in user."""

    if is_logged_in():
        user = get_current_user()

        if user:
            response = render_template('recordings.html',
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
        flash_message('Please log in to view your recordings.',
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


@app.route('/rename', methods=['POST'])
def rename():
    """Rename a recording."""

    title = request.form.get('title')
    recording_id = request.form.get('id')

    if recording_id and title:
        if recording_belongs_to_user(recording_id):
            rename_recording(recording_id, title)

            response = jsonify({'status': 'success',
                                'title': title,
                                'recording_id': recording_id})
        else:
            flash_message('Recording name can only be changed by recording author.',
                          ALERT_COLORS['red'])
            response = redirect('/recordings')

    else:
        response = jsonify({'status': 'malformed request'})

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

        response = {'status': 'success'}

    else:
        response = {'status': 'login_required'}

    return jsonify(response)


@app.route('/teapot', methods=['BREW', 'GET', 'PROPFIND', 'WHEN'])
def teapot():
    """Easter egg."""

    method = request.method

    if method == 'BREW':
        return jsonify({'status': 'brewing'})

    elif method == 'GET':
        return render_template('teapot.html'), 418

    elif method == 'PROPFIND':
        return jsonify({'strength': 'strong',
                        'origin': 'Vietnam',
                        'name': 'Kopi Luwak',
                        'quantity': '16 fl oz'})

    elif method == 'WHEN':
        return jsonify({'status': 'stopped_pouring',
                        'content': 'milk'})


@app.route('/toggle_public', methods=['POST'])
def toggle_public():
    """Change the visibility of a recording."""

    recording_id = request.form.get('recording_id')

    if recording_belongs_to_user(recording_id):
        toggle_recording_visibility(recording_id)

        response = jsonify({"status": "success"})

    else:
        flash_message('Visibility can only be changed by recording author.',
                      ALERT_COLORS['red'])
        response = redirect('/')

    return response


@app.route('/update_account', methods=['POST'])
def update_account():
    """Update account info."""

    user = get_current_user()

    if user:
        form = request.form
        response = update_account_info(user, form)

    else:
        flash('You must be logged in to update your account information.',
              ALERT_COLORS['red'])
        response = redirect('/login')

    return response

if __name__ == '__main__':
    # set up javascript testing
    import sys
    if sys.argv[-1] == "jasmine":
        JS_TESTING_MODE = True

    app.debug = os.environ.get('DEBUG', False)
    connect_to_db(app, os.environ.get('DATABASE_URL'))
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
