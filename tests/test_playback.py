import unittest

from flask import session

from model import connect_to_db, db, Recording, View
from server import app
from utils.authentication import add_session_info
from utils.playback import (add_view_to_db, delete_recording_by_id,
                            delete_keypresses_by_recording_id, get_recording_by_id,
                            make_keypress_list, recording_belongs_to_user,
                            recording_is_public, rename_recording,
                            toggle_recording_visibility)
from utils.test import (populate_test_db_keypresses, populate_test_db_recordings,
                        populate_test_db_themes, populate_test_db_users)


class TestAddViewToDb(unittest.TestCase):
    """Test adding a view to the db."""

    def setUp(self):
        """Set up app and db."""

        app.config['TESTING'] = True

        # setup test db
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()
        populate_test_db_recordings()

    def test_adding_recording_id_and_ip_address(self):
        """Test a fully qualified View entry."""

        recording_id = 1
        ip_address = '127.0.0.1'

        add_view_to_db(recording_id=recording_id,
                       ip_address=ip_address)

        db_view = View.query.get(1)
        all_views = View.query.all()

        self.assertEquals(recording_id, db_view.recording_id)
        self.assertEquals(ip_address, db_view.ip_address)
        self.assertEquals(1, len(all_views))

    def test_adding_recording_id(self):
        """Test adding a view that does not have an associated IP address."""

        recording_id = 1
        ip_address = None

        add_view_to_db(recording_id=recording_id,
                       ip_address=ip_address)

        db_view = View.query.get(1)
        all_views = View.query.all()

        self.assertEquals(recording_id, db_view.recording_id)
        self.assertEquals(ip_address, db_view.ip_address)
        self.assertEquals(db_view.ip_address, None)
        self.assertEquals(1, len(all_views))

    def tearDown(self):
        """Clear db for next test."""

        db.session.close()
        db.drop_all()


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

        recording = get_recording_by_id(1)

        self.assertNotEquals(recording, None)
        self.assertIsInstance(recording, Recording)
        self.assertEquals(recording.id, 1)

    def test_get_non_existing_recording(self):
        """Get a recording from the db that doesn't exist."""

        recording = get_recording_by_id(3)

        self.assertEquals(recording, None)

    def tearDown(self):
        """Clear db for next test."""

        db.session.close()
        db.drop_all()


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


class TestRecordingBelongsToUser(unittest.TestCase):
    """Test that we can accurately verify if a recording belongs to a user."""

    def setUp(self):
        """Set up app and db."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'super secret'

        # setup test db
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()
        populate_test_db_recordings()

    def test_belongs_to_user(self):
        """Test a recording that belongs to the user."""

        with app.test_request_context():
            user = {
                'id': 1,
                'name': 'Angie'
            }

            session['user'] = user
            belongs_to_user = recording_belongs_to_user(1)
            self.assertEquals(True, belongs_to_user)

    def test_does_not_belong_to_user(self):
        """Test a recording that does not belong to the user."""

        with app.test_request_context():
            user = {
                'id': 1,
                'name': 'Angie'
            }

            session['user'] = user
            belongs_to_user = recording_belongs_to_user(2)
            self.assertEquals(False, belongs_to_user)

    def test_recording_does_not_exist(self):
        """Test what happens when a recording does not exist."""

        with app.test_request_context():
            user = {
                'id': 1,
                'name': 'Angie'
            }

            session['user'] = user
            belongs_to_user = recording_belongs_to_user(3)
            self.assertEquals(False, belongs_to_user)

    def tearDown(self):
        """Clear db for next test."""

        db.session.close()
        db.drop_all()


class TestRecordingIsPublic(unittest.TestCase):
    """Test whether or not a given recording is public."""

    def setUp(self):
        """Set up app and db."""

        app.config['TESTING'] = True

        # setup test db
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()
        populate_test_db_recordings()

    def test_public(self):
        """Test a public recording."""

        is_public = recording_is_public(1)
        self.assertEquals(True, is_public)

    def test_private(self):
        """Test a private recording."""

        is_public = recording_is_public(2)
        self.assertEquals(False, is_public)

    def test_no_recording(self):
        """Test what happens when the recording does not exist."""

        is_public = recording_is_public(3)
        self.assertEquals(False, is_public)

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
