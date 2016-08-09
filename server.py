import json

from flask import Flask, jsonify, render_template, request
from model import connect_to_db, db, KeyPress, Recording

app = Flask(__name__)


@app.route('/')
def index():
    """Show main music-making page to user."""

    return render_template('index.html')


@app.route('/api/save_recording', methods=['POST'])
def save_recording():
    """Save recording data to the database."""

    recording_str = request.form.get('recording', None)
    recording = json.loads(recording_str)

    if recording:
        recording_id = add_recording_to_db()

        for keypress in recording:
            add_keypress_to_db_session(recording_id, keypress)

        db.session.commit()

    return jsonify({'response': 'OK'})


def add_recording_to_db():
    """Create new Recording and add to db.

    Returns the id of the new recording.
    """

    # TODO use my sample user until I get user accounts set up
    user_id = 1  # session['user_id']
    new_recording = Recording(user_id=user_id)

    db.session.add(new_recording)
    db.session.commit()

    return new_recording.id


def add_keypress_to_db_session(recording_id, keypress):
    """Create new KeyPress and add to db."""

    key_pressed = keypress.get('key')
    pressed_at = keypress.get('timestamp')
    theme = keypress.get('theme')

    new_keypress = KeyPress(recording_id=recording_id,
                            key_pressed=key_pressed,
                            pressed_at=pressed_at,
                            theme=theme)

    db.session.add(new_keypress)


if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    app.run(host='0.0.0.0')
