import json

from md5 import md5

from model import db, KeyPress, Recording


def delete_recording_from_db(id):
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


def get_recording_by_checksum(checksum):
    """Grab a recording from db using md5."""

    recording = None

    try:
        recording = db.session.query(Recording).filter(md5(id) == checksum).one()

    except NoResultFound:
        pass

    return recording


def get_recording_by_id(id):
    """Grab recording from db using recording id."""

    recording = None

    try:
        recording = Recording.query.get(id)

    except NoResultFound:
        pass

    return recording


def make_keypress_list(keypresses):
    """Create a JSON string containing keypress information."""

    keypress_list = []

    for keypress in keypresses:
        keypress_dict = {
            "key_pressed": keypress.key_pressed,
            "time_to_next_key": keypress.time_to_next_key
        }

        keypress_list.append(keypress_dict)

    return keypress_list


def rename_song(id, title):
    """Rename a song, given a new name and a recording id."""

    recording = get_recording_by_id(id)

    if recording:
        recording.name = title
        db.session.commit()
