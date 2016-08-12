import unittest

from model import connect_to_db, db
from server import app
from tests.test_utils import (populate_test_db_keypresses,
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
        self.assertIn('this_key', response.data)

    def test_not_existing_recording(self):
        """Test returned JSON for a recording that does not exist."""

        response = self.client.get('/fetch_recording/2',
                                   follow_redirects=True)

        self.assertEquals(200, response.status_code)
        self.assertIn('failure', response.data)
        self.assertNotIn('this_key', response.data)

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

    def test_profile_logged_in(self):
        """Test profile page displays when logged in."""

        pass

    def test_profile_not_logged_in(self):
        """Test profile page displays when not logged in."""

        pass


class TestRegister(unittest.TestCase):
    """Test registration endpoint."""

    def setUp(self):
        """Set up app and fake client."""

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_registration display(self):
        """Ensure registration form displays properly."""

        pass

    def test_register_existing_user(self):
        """Test what happens when you try to register an existing user."""

        pass

    def test_register_non_existing_user(self):
        """Test what happens when you try to register a non existing user."""

        pass


class TestSaveRecording(unittest.TestCase):
    """Test save recording endpoint."""

    def setUp(self):
        """Set up app and fake client."""

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_save_recording_logged_in(self):
        """Save recording while user is logged in."""

        pass

    def test_save_recording_not_logged_in(self):
        """Save recording while user is not logged in."""

        pass

if __name__ == '__main__':
    unittest.main()
