from model import Recording


def generate_keypress_pair(keypress, next_keypress):
    """Return a single keypress pair with relative timing."""

    this_key = keypress.key_pressed
    this_time = keypress.pressed_at

    next_key = next_keypress.key_pressed
    next_time = next_keypress.pressed_at

    pair_with_timing = {
        "this_key": this_key,
        "time_to_next": next_time - this_time,
        "next_key": next_key
    }

    return pair_with_timing


def get_keypresses_with_relative_timing(recording):
    """Return a list of key presses and relative timing pairs."""

    keypresses_with_relative_timing = []

    iter_keys = iter(recording.keypresses)
    keypress = next(iter_keys)

    for next_keypress in iter_keys:
        keypress_pair_with_timing = generate_keypress_pair(keypress, next_keypress)
        keypresses_with_relative_timing.append(keypress_pair_with_timing)
        keypress = next_keypress

    return keypresses_with_relative_timing


def get_recording_by_id(id):
    """Grab recording from db using recording id."""

    recording = None

    try:
        recording = Recording.query.get(id)

    except NoResultFound:
        pass

    return recording
