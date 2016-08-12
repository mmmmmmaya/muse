from flask import session

from model import db, KeyPress, Recording


def add_keypress_to_db_session(keypress):
    """Add new KeyPress to db.

    Returns the id of the new KeyPress.
    """

    db.session.add(keypress)


def add_recording_to_db():
    """Create new Recording and add to db.

    Returns the id of the new Recording.
    """

    user_id = session['user_id']
    new_recording = Recording(user_id=user_id)

    db.session.add(new_recording)
    db.session.commit()

    return new_recording.id


def generate_keypress(recording_id, keypress, next_keypress):
    """Return a single keypress pair with relative timing."""

    key_pressed = keypress.get('key')
    time = keypress.get('timestamp')
    time_to_next_key = None

    if next_keypress:
        next_time = next_keypress.get('timestamp')
        time_to_next_key = next_time - time

    theme = keypress.get('theme')

    new_keypress = KeyPress(recording_id=recording_id,
                            key_pressed=key_pressed,
                            time_to_next_key=time_to_next_key,
                            theme=theme)

    return new_keypress


def process_raw_keypresses(raw_keypress_list, recording_id):
    """Convert raw data into KeyPresses and add to db."""

    raw_keypress_list += [None]

    iter_keys = iter(raw_keypress_list)
    keypress = next(iter_keys)

    for next_keypress in iter_keys:
        new_keypress = generate_keypress(recording_id,
                                         keypress,
                                         next_keypress)
        add_keypress_to_db_session(new_keypress)

    db.session.commit()
