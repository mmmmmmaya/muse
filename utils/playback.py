import json

from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

from model import db, Recording, View
from utils.general import get_current_user


def add_view_to_db(recording_id, ip_address):
    """Add a new recording View to the db."""

    view = View(recording_id=recording_id,
                ip_address=ip_address)

    db.session.add(view)
    db.session.commit()


def get_recording_by_id(id):
    """Grab recording from db using recording id."""

    return Recording.query.get(id)


def get_popular_recordings():
    """Get the top 10 most-viewed recordings."""

    view_count = func.count(View.id).label('view_count')

    recordings = db.session.query(Recording, view_count) \
                           .join(View) \
                           .group_by(Recording.id) \
                           .order_by('view_count DESC') \
                           .limit(10) \
                           .all()
    popular_recordings = [recording[0] for recording in recordings]

    return popular_recordings


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


def recording_belongs_to_user(recording_id):
    """Determines whether the accessed recording belongs to the authenticated user."""

    belongs_to_user = False

    user = get_current_user()
    recording = get_recording_by_id(recording_id)

    if recording and user:
        if recording.user_id == user.id:
            belongs_to_user = True

    return belongs_to_user


def recording_is_public(recording_id):
    """Determines whether a given recording is publicly viewable."""

    is_public = False
    recording = get_recording_by_id(recording_id)

    if recording:
        is_public = recording.public

    return is_public
