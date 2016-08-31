import unittest

from flask import session

from model import connect_to_db, db, User
from server import app
from utils.authentication import (add_session_info, attempt_login,
                                  remove_session_info, verify_password)
from utils.test import populate_test_db_users


class TestAddSessionInfo(unittest.TestCase):
    """Test adding info to session."""

    def setUp(self):
        """Set up app and session key."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'super secret'

    def test_add_session_info_user(self):
        """Test adding session info when user has a value."""

        with app.test_request_context():
            user = User(id=1,
                        name='name',
                        email='angie@fake.com',
                        password='pass')
            add_session_info(user)

            self.assertIn('user', session)

            session_user = session['user']
            self.assertEquals(session_user['id'], 1)
            self.assertEquals(session_user['name'], 'name')

    def test_add_session_info_no_user(self):
        """Test what happens when no user is passed (hopefully nothing)."""

        with app.test_request_context():
            add_session_info(None)
            self.assertNotIn('user', session)


class TestAttemptLogin(unittest.TestCase):
    """Test an attempt to log user into site."""

    def setUp(self):
        """Set up app, session key, and db."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'super secret'

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
            self.assertEquals(1, session['user']['id'])

    def test_login_valid_user_invalid_password(self):
        """Test login for an existing user with an incorrect password."""

        with app.test_request_context():
            username = 'angie@fake.com'
            password = 'wrong password'

            response = attempt_login(username, password)

            self.assertEquals('/login', response.location)
            self.assertEquals(302, response.status_code)
            self.assertNotIn('user', session)

    def test_login_invalid_user(self):
        """Test login for a user that does not exist."""

        with app.test_request_context():
            username = 'not_in@db.com'
            password = 'doesnt matter'

            response = attempt_login(username, password)

            self.assertEquals(302, response.status_code)
            self.assertEquals('/register', response.location)
            self.assertNotIn('user', session)

    def tearDown(self):
        """Clear db for next test."""

        db.session.close()
        db.drop_all()


class TestRemoveSessionInfo(unittest.TestCase):
    """Test that user is removed from session."""

    def setUp(self):
        """Set up app and session key."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'super secret'

    def test_remove_no_user_in_session(self):
        """Test removal when we start without any user in session."""

        with app.test_request_context():
            remove_session_info()

            self.assertNotIn('user', session)

    def test_remove_user_is_none(self):
        """Test removal when user in session, but value is None."""

        with app.test_request_context():
            session['user'] = None
            self.assertIn('user', session)

            remove_session_info()
            self.assertNotIn('user', session)

    def test_remove_user_in_session(self):
        """Test removal when we start with a user in session."""

        with app.test_request_context():
            user = {
                'id': 1,
                'name': 'name'
            }

            session['user'] = user
            self.assertIn('user', session)

            remove_session_info()
            self.assertNotIn('user', session)

if __name__ == '__main__':
    unittest.main()
