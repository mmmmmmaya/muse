import json

from md5 import md5
from sqlalchemy.orm.exc import NoResultFound

from model import db, KeyPress, Recording, View


def add_view_to_db(recording_id, ip_address):
    """Add a new recording View to the db."""

    view = View(recording_id=recording_id,
                ip_address=ip_address)

    db.session.add(view)
    db.session.commit()


def delete_recording_by_id(id):
    """Remove a recording from the db, given an id."""

    recording = get_recording_by_id(id)

    if recording:
        delete_keypresses_by_recording_id(id)
        db.session.delete(recording)
        db.session.commit()


def delete_keypresses_by_recording_id(id):
    """Delete all keypressess associated with a given recording."""

    keypresses = KeyPress.query.filter_by(recording_id=id).all()

    for keypress in keypresses:
        db.session.delete(keypress)

    db.session.commit()


def get_recording_by_id(id):
    """Grab recording from db using recording id."""

    return Recording.query.get(id)


def make_keypress_list(keypresses):
    """Create a JSON string containing keypress information."""

    keypress_list = []

    for keypress in keypresses:
        keypress_dict = {
            "key_pressed": keypress.key_pressed,
            "time_to_next_key": keypress.time_to_next_key,
            "theme": keypress.theme
        }

        keypress_list.append(keypress_dict)

    return keypress_list


def rename_recording(id, title):
    """Rename a recording, given a new name and a recording id."""

    recording = get_recording_by_id(id)

    if recording:
        recording.name = title
        db.session.commit()
