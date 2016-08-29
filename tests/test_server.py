import json
import unittest

from model import connect_to_db, db, Recording, User
from server import app
from utils.test import (populate_test_db_keypresses,
                        populate_test_db_recordings,
                        populate_test_db_themes,
                        populate_test_db_users)


class TestIndex(unittest.TestCase):
    """Test that index (recording) page."""

    def setUp(self):
        """Set up app and fake client."""

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index(self):
        """Test that basic index page loads normally."""

        response = self.client.get('/',
                                   follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertIn('Play with Muse!', response.data)


class TestDeleteRecording(unittest.TestCase):
    """Test removing a recording via the web."""

    def setUp(self):
        """Set up app and fake client."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'super secret'
        self.client = app.test_client()

        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()
        populate_test_db_recordings()

    def test_delete_recording(self):
        """Test removing a single recording."""

        with app.test_request_context():
            num_before = len(Recording.query.all())

            self.client.post('/login',
                             data={
                                 "email": "angie@fake.com",
                                 "password": "pass"
                             })

            response = self.client.post('/delete',
                                        data={"recording_id": "1"},
                                        follow_redirects=True)

            num_after = len(Recording.query.all())

            self.assertEquals(200, response.status_code)
            self.assertIn('success', response.data)
            self.assertEquals(num_before, num_after + 1)

    def test_delete_recording_not_logged_in(self):
        """Test deleting when you aren't logged in."""

        num_before = len(Recording.query.all())

        response = self.client.post('/delete',
                                    data={"recording_id": "1"},
                                    follow_redirects=True)

        num_after = len(Recording.query.all())

        self.assertEquals(200, response.status_code)
        self.assertIn('Recording can only be deleted by recording author.',
                      response.data)
        self.assertEquals(num_before, num_after)

    def test_delete_no_recording_id(self):
        """Test what happens when no recording id is given."""

        response = self.client.post('/delete',
                                    data={},
                                    follow_redirects=True)

        self.assertIn('malformed request', response.data)

    def tearDown(self):
        """Reset db for next test."""

        db.session.close()
        db.drop_all()


class TestFetchRecording(unittest.TestCase):
    """Test route to get keypresses in a recording."""

    def setUp(self):
        """Set up app, db, and fake client."""

        app.config['TESTING'] = True
        self.client = app.test_client()

        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_themes()
        populate_test_db_users()
        populate_test_db_recordings()
        populate_test_db_keypresses()

    def test_existing_recording(self):
        """Test returned JSON for a recording that exists."""

        response = self.client.get('/fetch_recording/1',
                                   follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertIn('success', response.data)
        self.assertIn('key_pressed', response.data)

    def test_not_existing_recording(self):
        """Test returned JSON for a recording that does not exist."""

        response = self.client.get('/fetch_recording/2',
                                   follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertIn('failure', response.data)
        self.assertNotIn('key_pressed', response.data)

    def tearDown(self):
        """Reset db for next test."""

        db.session.close()
        db.drop_all()


class TestListen(unittest.TestCase):
    """Test what appears on the page when you listen to a recording."""

    def setUp(self):
        """Set up app and fake client."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'super secret'
        self.client = app.test_client()

        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()
        populate_test_db_recordings()

    def test_public_listen(self):
        """Test listening to a public recording."""

        response = self.client.get('/listen/1',
                                   follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertIn('svg', response.data)
        self.assertIn('data-id=1', response.data)

    def test_private_listen_logged_in(self):
        """Test listening to a private recording you created."""

        with app.test_request_context():
            self.client.post('/login',
                             data={
                                 "email": "angie2@fake.com",
                                 "password": "pass"
                             })

            response = self.client.get('/listen/2',
                                       follow_redirects=True)

            self.assertEquals(200, response.status_code)
            self.assertIn('svg', response.data)
            self.assertIn('data-id=2', response.data)

    def test_private_listen_not_logged_in(self):
        """Test listening to a private recording you did not create."""

        with app.test_request_context():
            response = self.client.get('/listen/2',
                                       follow_redirects=True)

            self.assertEquals(200, response.status_code)
            self.assertIn('It looks like that recording is private or does not exist.',
                          response.data)
            self.assertIn('Play with Muse!', response.data)

    def tearDown(self):
        """Reset db for next test."""

        db.session.close()
        db.drop_all()


class TestLogin(unittest.TestCase):
    """Test login page."""

    def setUp(self):
        """Set up app and fake client."""

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_login(self):
        """Test login page displays appropriately."""

        response = self.client.get('/login',
                                   follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertIn('Log in to Muse!', response.data)
        self.assertIn('login-form', response.data)


class TestLogout(unittest.TestCase):
    """Test logout endpoint."""

    def setUp(self):
        """Set up app and fake client."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'super secret'
        self.client = app.test_client()

        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()

    def test_logout_logged_in(self):
        """Logout when user is logged in."""

        self.client.post('/login',
                         data={
                             "email": "angie@fake.com",
                             "password": "pass"
                         })

        response = self.client.get('/logout',
                                   follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertIn('You were successfully logged out.', response.data)

    def test_logout_not_logged_in(self):
        """Logout when user is not logged in."""

        response = self.client.get('/logout',
                                   follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertIn('You were successfully logged out.', response.data)

    def tearDown(self):
        """Reset db for next test."""

        db.session.close()
        db.drop_all()


class TestLogView(unittest.TestCase):
    """Test that a View is logged in the db when someone watches a recording."""

    def setUp(self):
        """Set up app and fake client."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'super secret'
        self.client = app.test_client()

        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()
        populate_test_db_themes()
        populate_test_db_recordings()
        populate_test_db_keypresses()

    def test_fully_qualified_view(self):
        """Test logging a view when recording_id and ip_address provided."""

        response = self.client.post('/log_view', data={"recording_id": "1",
                                                       "ip_address": "0.0.0.0"})

        self.assertIn('success', response.data)

    def test_only_required_params(self):
        """Test logging a view when only recording_id provided."""

        response = self.client.post('/log_view', data={"recording_id": "1"})

        self.assertIn('success', response.data)

    def test_missing_required_params(self):
        """Test that a failure occurs when required information (recording_id) not provided"""

        response = self.client.post('/log_view', data={})

        self.assertIn('malformed request', response.data)

    def tearDown(self):
        """Reset db for next test."""

        db.session.close()
        db.drop_all()


class TestProfile(unittest.TestCase):
    """Test profile page."""

    def setUp(self):
        """Set up app, session key, and fake client."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'super secret'
        self.client = app.test_client()

        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_themes()
        populate_test_db_users()
        populate_test_db_recordings()
        populate_test_db_keypresses()

    def test_profile_logged_in(self):
        """Test profile page displays when logged in."""

        self.client.post('/login',
                         data={
                             "email": "angie@fake.com",
                             "password": "pass"
                         })

        response = self.client.get('/profile',
                                   follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertNotIn('Please log in to view your profile.', response.data)
        self.assertIn('s Profile', response.data)

    def test_profile_not_logged_in(self):
        """Test profile page displays when not logged in."""

        response = self.client.get('/profile',
                                   follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertIn('Please log in to view your profile.', response.data)
        self.assertNotIn('s Profile', response.data)

    def test_profile_not_in_db(self):
        """Test what happens when the logged in user is not in the db."""

        with app.test_request_context():
            self.client.post('/login',
                             data={
                                 "email": "angie@fake.com",
                                 "password": "pass"
                             })

            user = User.query.get(1)
            db.session.delete(user)
            db.session.commit()

            response = self.client.get('/profile',
                                       follow_redirects=True)

            self.assertEquals(200, response.status_code)
            self.assertIn('There was an error. Please log in and try again.', response.data)
            self.assertNotIn('s Profile', response.data)

    def tearDown(self):
        """Reset db for next test."""

        db.session.close()
        db.drop_all()


class TestRegister(unittest.TestCase):
    """Test registration endpoint."""

    def setUp(self):
        """Set up app and fake client."""

        app.config['TESTING'] = True
        self.client = app.test_client()

        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_themes()
        populate_test_db_users()
        populate_test_db_recordings()
        populate_test_db_keypresses()

    def test_registration_display(self):
        """Ensure registration form displays properly."""

        response = self.client.get('/register',
                                   follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertIn('Register with Muse!', response.data)
        self.assertIn('registration-form', response.data)

    def test_register_logged_in(self):
        """Test what happens when someone who is logged in tries to register."""

        self.client.post('/login',
                         data={
                             "email": "angie@fake.com",
                             "password": "pass"
                         })

        response = self.client.get('/register',
                                   follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertIn('Play with Muse!', response.data)
        self.assertNotIn('registration-form', response.data)

    def test_register_existing_user(self):
        """Test what happens when you try to register an existing user."""

        response = self.client.post('/register',
                                    data={
                                        "email": "angie@fake.com",
                                        "password": "password",
                                        "name": "Angie"
                                    },
                                    follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertIn('That user already exists. Please log in.', response.data)
        self.assertNotIn('Account created successfully.', response.data)

    def test_register_non_existing_user(self):
        """Test what happens when you try to register a non existing user."""

        response = self.client.post('/register',
                                    data={
                                        "email": "nobody@hasthis.email",
                                        "password": "password",
                                        "name": "Angie"
                                    },
                                    follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertNotIn('That user already exists. Please log in.', response.data)
        self.assertIn('Account created successfully.', response.data)

    def test_register_missing_params(self):
        """Test what happens when you try to register a user without necessary params."""

        response = self.client.post('/register',
                                    data={
                                        "email": "nobody@hasthis.email",
                                        "password": "password"
                                    },
                                    follow_redirects=True)

        self.assertEquals(400, response.status_code)
        self.assertIn('You are missing a field necessary for registration.', response.data)
        self.assertNotIn('Account created successfully.', response.data)

    def tearDown(self):
        """Reset db for next test."""

        db.session.close()
        db.drop_all()


class TestRenameRecording(unittest.TestCase):
    """Test what happens when we rename a recording."""

    def setUp(self):
        """Set up app and fake client."""

        app.config['TESTING'] = True
        self.client = app.test_client()

        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()
        populate_test_db_recordings()

    def test_rename_recording_logged_in(self):
        """Test renaming a recording when you are logged in."""

        with app.test_request_context():
            self.client.post('/login',
                             data={
                                 "email": "angie@fake.com",
                                 "password": "pass"
                             })

            id = '1'
            name = 'new name'

            response = self.client.post('/rename',
                                        data={"id": id,
                                              "title": name},
                                        follow_redirects=True)

            self.assertEquals(200, response.status_code)
            self.assertIn('success', response.data)
            self.assertIn(id, response.data)
            self.assertIn(name, response.data)

    def test_rename_recording_not_logged_in(self):
        """Test renaming a recording when you are not logged in."""

        id = '1'
        name = 'new name'

        response = self.client.post('/rename',
                                    data={"id": id,
                                          "title": name},
                                    follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertIn('Recording name can only be changed by recording author.',
                      response.data)

    def test_rename_recording_missing_params(self):
        """Test error returned when required param missing in request."""

        id = '1'

        response = self.client.post('/rename',
                                    data={"id": id},
                                    follow_redirects=True)

        self.assertIn('malformed request', response.data)

    def tearDown(self):
        """Reset db for next test."""

        db.session.close()
        db.drop_all()


class TestSaveRecording(unittest.TestCase):
    """Test save recording endpoint."""

    def setUp(self):
        """Set up app and fake client."""

        app.config['TESTING'] = True
        self.client = app.test_client()

        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()

        populate_test_db_users()
        populate_test_db_themes()

    def test_save_recording_logged_in(self):
        """Save recording while user is logged in."""

        self.client.post('/login',
                         data={
                             "email": "angie@fake.com",
                             "password": "pass"
                         })

        keypresses = json.dumps(
            [{"timestamp": 1471993671612,
              "key": "r",
              "theme": 1}]
        )

        response = self.client.post('/save_recording',
                                    data={"keypresses": keypresses},
                                    follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertIn('success', response.data)

    def test_save_recording_not_logged_in(self):
        """Save recording while user is not logged in."""

        response = self.client.post('/save_recording',
                                    data={"keypresses": None},
                                    follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertIn('login_required', response.data)

    def tearDown(self):
        """Reset db for next test."""

        db.session.close()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
