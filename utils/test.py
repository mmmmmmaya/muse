import random
import time

from Crypto.Hash import SHA256

from model import db, KeyPress, Recording, Theme, User, View
from utils.authentication import hash_password


def populate_test_db_keypresses():
    """Add keypress data in fake db for testing."""

    for num in range(6):
        time_to_next_key = random.randint(0, 5000)
        fake_keypress = KeyPress(recording_id=1,
                                 key_pressed='a',
                                 time_to_next_key=time_to_next_key,
                                 theme=1)

        db.session.add(fake_keypress)

    db.session.commit()


def populate_test_db_recordings():
    """Add recording data in fake db for testing."""

    fake_recording = Recording(user_id=1)
    fake_recording2 = Recording(user_id=2,
                                public=False)

    db.session.add(fake_recording)
    db.session.add(fake_recording2)
    db.session.commit()


def populate_test_db_themes():
    """Create theme data in fake db for testing."""

    fake_theme = Theme(name='fake_theme')

    db.session.add(fake_theme)
    db.session.commit()


def populate_test_db_users():
    """Create user data in fake db for testing."""

    hashed_password = hash_password('pass')

    fake_user = User(name='Angie',
                     email='angie@fake.com',
                     password=hashed_password)

    fake_user2 = User(name='Angie2',
                      email='angie2@fake.com',
                      password=hashed_password)

    db.session.add(fake_user)
    db.session.add(fake_user2)
    db.session.commit()


def populate_test_db_views(recording_id=1):
    """Add view data in fake db for testing."""

    fake_view = View(recording_id=recording_id)

    db.session.add(fake_view)
    db.session.commit()
