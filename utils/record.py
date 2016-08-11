from flask import session

from model import db, KeyPress, Recording


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


def add_recording_to_db():
    """Create new Recording and add to db.

    Returns the id of the new recording.
    """

    user_id = session['user_id']
    new_recording = Recording(user_id=user_id)

    db.session.add(new_recording)
    db.session.commit()

    return new_recording.id
