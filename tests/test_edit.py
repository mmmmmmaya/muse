import unittest

from model import connect_to_db, db, Recording
from server import app
from utils.playback import get_recording_by_id
from utils.edit import (delete_recording_by_id, delete_keypresses_by_recording_id,
                        rename_recording, toggle_recording_visibility)
from utils.test import (populate_test_db_keypresses, populate_test_db_recordings,
                        populate_test_db_themes, populate_test_db_users)


class TestDeleteRecordingById(unittest.TestCase):
    """Remove a recording from the db, given a recording_id."""

    def setUp(self):
        """Set up app and db."""

        app.config['TESTING'] = True

        # setup test db
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()
        populate_test_db_recordings()

    def test_delete_existing_recording(self):
        """Delete an existing recording from the db."""

        delete_recording_by_id(1)
        recording = get_recording_by_id(1)

        self.assertEquals(recording, None)
        self.assertNotIsInstance(recording, Recording)

    def test_delete_non_existing_recording(self):
        """Delete a recording from the db that doesn't exist."""

        delete_recording_by_id(3)
        recording = get_recording_by_id(3)

        self.assertEquals(recording, None)

    def tearDown(self):
        """Clear db for next test."""

        db.session.close()
        db.drop_all()


class TestDeleteKeyPressesByRecordingId(unittest.TestCase):
    """Remove keypresses from the db, given a recording_id."""

    def setUp(self):
        """Set up app and db."""

        app.config['TESTING'] = True

        # setup test db
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()
        populate_test_db_themes()
        populate_test_db_recordings()
        populate_test_db_keypresses()

    def test_delete_existing_keypresses(self):
        """Delete existing keypresses from the db."""

        delete_keypresses_by_recording_id(1)
        recording = get_recording_by_id(1)
        keypresses = recording.keypresses

        self.assertEquals(len(keypresses), 0)

    def test_delete_non_existing_keypresses(self):
        """Delete keypresses from the db where the recording doesn't exist."""

        delete_keypresses_by_recording_id(3)

    def tearDown(self):
        """Clear db for next test."""

        db.session.close()
        db.drop_all()


class TestRenameRecording(unittest.TestCase):
    """Rename recording in db, given a recording_id and new name."""

    def setUp(self):
        """Set up app and db."""

        app.config['TESTING'] = True

        # setup test db
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()
        populate_test_db_recordings()

    def test_rename_existing_recording(self):
        """Rename existing recording in the db."""

        new_name = 'new name'
        rename_recording(1, new_name)

        recording = get_recording_by_id(1)
        all_recs_with_new_name = db.session.query(Recording).filter_by(name=new_name).all()

        self.assertEquals(recording.name, new_name)
        self.assertEquals(len(all_recs_with_new_name), 1)

    def test_rename_non_existing_recording(self):
        """Rename a recording from the db that doesn't exist."""

        new_name = 'new name'
        rename_recording(3, new_name)

        recording = get_recording_by_id(3)
        all_recs_with_new_name = db.session.query(Recording).filter_by(name=new_name).all()

        self.assertEquals(recording, None)
        self.assertEquals(len(all_recs_with_new_name), 0)

    def tearDown(self):
        """Clear db for next test."""

        db.session.close()
        db.drop_all()


class TestToggleRecordingVisibility(unittest.TestCase):
    """Change a recording's visibility."""

    def setUp(self):
        """Set up app and db."""

        app.config['TESTING'] = True

        # setup test db
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()
        populate_test_db_recordings()

    def test_public_to_private(self):
        """Test making a public recording private."""

        recording = Recording.query.get(1)
        self.assertEquals(True, recording.public)

        toggle_recording_visibility(1)
        recording = Recording.query.get(1)

        self.assertEquals(False, recording.public)

    def test_private_to_public(self):
        """Test making a private recording public."""

        recording = Recording.query.get(2)
        self.assertEquals(False, recording.public)

        toggle_recording_visibility(2)
        recording = Recording.query.get(2)

        self.assertEquals(True, recording.public)

    def test_no_recording(self):
        """Test what happens when there is no recording to update."""

        num_recordings = len(Recording.query.all())

        toggle_recording_visibility(3)
        recording = Recording.query.get(3)

        num_recordings_after = len(Recording.query.all())

        self.assertEquals(recording, None)
        self.assertEquals(num_recordings, num_recordings_after)

    def tearDown(self):
        """Clear db for next test."""

        db.session.close()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
