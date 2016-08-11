import unittest

from flask import session

from model import connect_to_db, db
from server import app
from utils.authentication import (add_session_info, attempt_login,
                                  remove_session_info, verify_password)
from tests.test_utils import populate_test_db_users


class TestAddSessionInfo(unittest.TestCase):
    """Test adding info to session."""

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'super secret'

    def test_add_session_info_user_id(self):
        """Test adding session info when user_id has a value."""

        with app.test_request_context():
                add_session_info(35)
                self.assertIn('user_id', session)
                self.assertEquals(session['user_id'], 35)

    def test_add_session_info_no_user_id(self):
        """Test what happens when no user_id is passed (hopefully nothing)."""

        with app.test_request_context():
            add_session_info(None)
            self.assertNotIn('user_id', session)


class TestAttemptLogin(unittest.TestCase):
    """Test an attempt to log user into site."""

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'super secret'

        self.client = app.test_client()

        # setup test db
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()
        populate_test_db_users()

    def test_login_valid_user_valid_password(self):
        """Test a valid user/password pair."""

        with app.test_request_context():
            username = 'angie@fake.com'
            password = 'pass'

            response = attempt_login(username, password)

            self.assertEquals('/', response.location)
            self.assertEquals(302, response.status_code)
            self.assertEquals(1, session['user_id'])

    def test_login_valid_user_invalid_password(self):
        """Test login for an existing user with an incorrect password."""

        pass

    def test_login_invalid_user(self):
        """Test login for a user that does not exist."""

        pass

    def tearDown(self):
        """Clear db for next test."""

        db.session.close()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
