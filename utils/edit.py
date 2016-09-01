from model import db, KeyPress, View
from utils.playback import get_recording_by_id


def delete_recording_by_id(recording_id):
    """Remove a recording from the db, given an id."""

    recording = get_recording_by_id(recording_id)

    if recording:
        delete_keypresses_by_recording_id(recording_id)
        delete_views_by_recording_id(recording_id)
        db.session.delete(recording)
        db.session.commit()


def delete_keypresses_by_recording_id(recording_id):
    """Delete all keypresses associated with a given recording."""

    keypresses = KeyPress.query.filter_by(recording_id=recording_id).all()

    for keypress in keypresses:
        db.session.delete(keypress)

    db.session.commit()


def delete_views_by_recording_id(recording_id):
    """Delete all views associated with a given recording."""

    views = View.query.filter_by(recording_id=recording_id).all()

    for view in views:
        db.session.delete(view)

    db.session.commit()


def rename_recording(id, title):
    """Rename a recording, given a new name and a recording id."""

    recording = get_recording_by_id(id)

    if recording:
        recording.name = title
        db.session.commit()


def toggle_recording_visibility(recording_id):
    """Change recording from public to private or vice versa."""

    recording = get_recording_by_id(recording_id)

    if recording:
        recording.public = not recording.public
        db.session.commit()
