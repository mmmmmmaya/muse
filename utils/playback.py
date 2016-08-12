from model import Recording


def get_recording_by_id(id):
    """Grab recording from db using recording id."""

    recording = None

    try:
        recording = Recording.query.get(id)

    except NoResultFound:
        pass

    return recording
