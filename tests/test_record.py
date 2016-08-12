import unittest

from datetime import datetime
from flask import session

from model import connect_to_db, db, KeyPress, Recording
from server import app
from utils.record import (add_keypress_to_db_session, add_recording_to_db,
                          generate_keypress, process_raw_keypresses)
from utils.test import (populate_test_db_recordings,
                        populate_test_db_themes, populate_test_db_users)


class TestAddKeyPressToDbSession(unittest.TestCase):
    """Test adding Keypress objects to db."""

    def setUp(self):
        """Set up app and db."""

        app.config['TESTING'] = True

        # setup test db
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()
        populate_test_db_recordings()
        populate_test_db_themes()

    def test_fully_qualified_keypress(self):
        """Add a keypress that contains all possible pieces of information."""

        new_keypress = KeyPress(recording_id=1,
                                key_pressed='a',
                                time_to_next_key=500,
                                theme=1)

        add_keypress_to_db_session(new_keypress)
        db.session.commit()

        keypress = KeyPress.query.one()

        self.assertNotEquals(keypress, None)
        self.assertIsInstance(keypress, KeyPress)
        self.assertEquals(keypress.key_pressed, 'a')

    def test_only_required_fields(self):
        """Add a keypress that does not have a time_to_next value."""

        new_keypress = KeyPress(recording_id=1,
                                key_pressed='a',
                                theme=1)

        add_keypress_to_db_session(new_keypress)
        db.session.commit()

        keypress = KeyPress.query.one()

        self.assertNotEquals(keypress, None)
        self.assertIsInstance(keypress, KeyPress)
        self.assertEquals(keypress.key_pressed, 'a')
        self.assertEquals(keypress.time_to_next_key, None)

    def tearDown(self):
        """Clear db for next test."""

        db.session.close()
        db.drop_all()


class TestAddRecordingToDb(unittest.TestCase):
    """Test adding Recording objects to db."""

    def setUp(self):
        """Set up app and db."""

        app.config['TESTING'] = True

        # setup test db
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()
        populate_test_db_themes()

    def test_add_recording(self):
        """Add a recording that contains all possible pieces of information."""

        with app.test_request_context():
            session['user_id'] = 1
            add_recording_to_db()

            recording = Recording.query.one()

            self.assertNotEquals(recording, None)
            self.assertIsInstance(recording, Recording)
            self.assertEquals(recording.user_id, 1)
            self.assertEquals(recording.public, True)

    def tearDown(self):
        """Clear db for next test."""

        db.session.close()
        db.drop_all()


class TestGenerateKeypress(unittest.TestCase):
    """Make a single Keypress object from two sequential pieces of keypress data."""

    def test_two_keypresses(self):
        """Test that a KeyPress object is made from 2 pieces of keypress data."""

        recording_id = 1
        keypress = {
            'key': 'a',
            'timestamp': 12345,
            'theme': 1
        }
        next_keypress = {
            'key': 'b',
            'timestamp': 12945,
            'theme': 1
        }

        new_keypress = generate_keypress(recording_id, keypress, next_keypress)

        self.assertNotEquals(new_keypress, None)
        self.assertIsInstance(new_keypress, KeyPress)
        self.assertEquals(new_keypress.time_to_next_key, 600)

    def test_one_keypress(self):
        """Test that a KeyPress object is made from 1 piece of keypress data and a None."""

        recording_id = 1
        keypress = {
            'key': 'a',
            'timestamp': 12345,
            'theme': 1
        }
        next_keypress = None

        new_keypress = generate_keypress(recording_id, keypress, next_keypress)

        self.assertNotEquals(new_keypress, None)
        self.assertIsInstance(new_keypress, KeyPress)
        self.assertEquals(new_keypress.key_pressed, 'a')
        self.assertEquals(new_keypress.time_to_next_key, None)


class TestProcessRawKeypresses(unittest.TestCase):
    """Make a list of KeyPress objects from a list of keypress data pieces."""

    def setUp(self):
        """Set up app and db."""

        app.config['TESTING'] = True

        # setup test db
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()
        populate_test_db_themes()
        populate_test_db_recordings()

    def test_empty_list(self):
        """Test what happens when processing a list with no keypresses in it."""

        raw_keypress_list = []

        process_raw_keypresses(raw_keypress_list, recording_id=1)
        keypresses = Recording.query.get('1').keypresses

        self.assertIsInstance(keypresses, list)
        self.assertEquals(len(keypresses), 0)

    def test_one_item_in_list(self):
        """Test what happens when processing a list with one keypress in it."""

        raw_keypress_list = [
            {'key': 'a',
             'timestamp': 12345,
             'theme': 1}
        ]

        process_raw_keypresses(raw_keypress_list, recording_id=1)
        keypresses = Recording.query.get('1').keypresses

        self.assertIsInstance(keypresses, list)
        self.assertEquals(len(keypresses), 1)

    def test_multi_items_in_list(self):
        """Test what happens when processing a list with many keypresses."""

        raw_keypress_list = [
            {'key': 'a',
             'timestamp': 12345,
             'theme': 1},
            {'key': 'b',
             'timestamp': 12445,
             'theme': 1},
            {'key': 'c',
             'timestamp': 12545,
             'theme': 1},
            {'key': 'd',
             'timestamp': 12645,
             'theme': 1},
            {'key': 'e',
             'timestamp': 12745,
             'theme': 1}
        ]

        process_raw_keypresses(raw_keypress_list, recording_id=1)
        keypresses = Recording.query.get('1').keypresses

        self.assertIsInstance(keypresses, list)
        self.assertEquals(len(keypresses), 5)

    def tearDown(self):
        """Clear db for next test."""

        db.session.close()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
