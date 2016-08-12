import json

from model import Recording


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
