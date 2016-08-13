import unittest

from flask import session

from model import connect_to_db, db
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
        self.assertIn('record-button', response.data)


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
        self.client = app.test_client()

    def test_logout(self):
        """General logout case."""

        response = self.client.get('/logout',
                                   follow_redirects=True)

        self.assertEquals(200, response.status_code)


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
        self.assertIn('record-button', response.data)
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
                                        "email": "angie2@fake.com",
                                        "password": "password",
                                        "name": "Angie"
                                    },
                                    follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertNotIn('That user already exists. Please log in.', response.data)
        self.assertIn('Account created successfully.', response.data)

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

    def test_save_recording_logged_in(self):
        """Save recording while user is logged in."""

        self.client.post('/login',
                         data={
                             "email": "angie@fake.com",
                             "password": "pass"
                         })

        response = self.client.post('/save_recording',
                                    data={"recording": "[]"},
                                    follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertIn('saved', response.data)

    def test_save_recording_not_logged_in(self):
        """Save recording while user is not logged in."""

        response = self.client.post('/save_recording',
                                    data={"recording": "[]"},
                                    follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertIn('login_required', response.data)

if __name__ == '__main__':
    unittest.main()
