import unittest

from model import connect_to_db, db, Recording
from server import app
from utils.test import populate_test_db_recordings, populate_test_db_users


class TestGetRecordingById(unittest.TestCase):
    """Get a recording from the db, by id."""

    def setUp(self):
        """Set up app and db."""

        app.config['TESTING'] = True

        # setup test db
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()
        populate_test_db_recordings()

    def test_get_existing_recording(self):
        """Get an existing recording from the db."""

        print Recording.query.all()
        recording = Recording.query.get('1')

        self.assertNotEquals(recording, None)
        self.assertIsInstance(recording, Recording)
        self.assertEquals(recording.id, 1)

    def test_get_non_existing_recording(self):
        """Get a recording from the db that doesn't exist."""

        recording = Recording.query.get('2')

        self.assertEquals(recording, None)

    def tearDown(self):
        """Clear db for next test."""

        db.session.close()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
