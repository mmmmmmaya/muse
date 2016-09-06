import unittest

from flask import session

from model import connect_to_db, db, Recording, View
from server import app
from utils.authentication import add_session_info
from utils.playback import (add_view_to_db, get_popular_recordings, get_recording_by_id,
                            make_keypress_list, recording_belongs_to_user,
                            recording_is_public)
from utils.test import (populate_test_db_recordings, populate_test_db_users,
                        populate_test_db_views)


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


class TestGetPopularRecordings(unittest.TestCase):
    """Test that recordings are returned in the proper order."""

    def setUp(self):
        """Set up app and db."""

        app.config['TESTING'] = True

        # setup test db
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()

    def test_no_recordings(self):
        """Test what is returned when no recordings in db."""

        recordings = get_popular_recordings()

        self.assertEquals(len(recordings), 0)
        self.assertIsInstance(recordings, list)

    def test_mixed_public_private_recordings(self):
        """Test that only public recordings returned when both exist in db."""

        for i in range(5):
            populate_test_db_recordings()
            populate_test_db_views(i + 1)  # even numbered recordings are private

        recordings = get_popular_recordings()

        self.assertEquals(len(recordings), 3)  # views only exist on recordings 1-5
        for recording in recordings:           # but 2 and 4 are private
            self.assertEquals(recording.public, True)

    def test_public_ordered(self):
        """Test that a max of 10 recordings are returned in desc order by number of views."""

        for i in range(30):
            populate_test_db_recordings()

            for j in range(i):
                populate_test_db_views(recording_id=i + 1)

        recordings = get_popular_recordings()
        prev_num_views = None

        for recording in recordings:
            num_views = len(recording.views)

            if prev_num_views:
                self.assertTrue(prev_num_views > num_views)

            prev_num_views = num_views

            self.assertEquals(recording.public, True)

        self.assertEquals(len(recordings), 10)

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


if __name__ == '__main__':
    unittest.main()
