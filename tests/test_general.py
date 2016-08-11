import unittest

from flask import session

from model import connect_to_db, db, User
from server import app
from tests.test_utils import populate_test_db_users
from utils.general import (flash_message, get_current_user,
                           get_user_by_email, is_logged_in)


class TestFlashMessage(unittest.TestCase):
    """Test various applications of marked up flash messages."""

    def setUp(self):
        """Set up app and browser."""

        app.config['TESTING'] = True

    def test_empty_message(self):
        """Test flashing a message with no text."""

        message = ''
        alert_type = 'success'

        flash_message(message, alert_type)

        with app.test_request_context():
            self.assertNotIn('_flashes', session)

    def test_message_with_content(self):
        """Test flashing a message with text."""

        with app.test_request_context():
            message = 'message'
            alert_type = 'success'

            flash_message(message, alert_type)
            flashed_message = session['_flashes'][0]

            self.assertEquals(message, flashed_message[0])
            self.assertIn(alert_type, flashed_message[1])


class TestGetCurrentUser(unittest.TestCase):
    """Test the app's ability to get the logged in user."""

    def setUp(self):
        """Set up app, session key, and db."""

        app.config['TESTING'] = True

        # set up db
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()
        populate_test_db_users()

    def test_no_user(self):
        """Test what happens when no user is logged in."""

        with app.test_request_context():
            user = get_current_user()

            self.assertEquals(user, None)

    def test_invalid_user(self):
        """Test what happens when we try to get a user that is not in the db."""

        with app.test_request_context():
            # log in
            session['user_id'] = 1

            # somehow, user is removed from db
            db_user = User.query.get(1)
            db.session.delete(db_user)
            db.session.commit()

            user = get_current_user()

            self.assertIn('user_id', session)
            self.assertEquals(1, session['user_id'])
            self.assertEquals(user, None)

    def test_user_logged_in(self):
        """Test what happens when someone is logged in."""

        with app.test_request_context():
            # log in
            session['user_id'] = 1

            user = get_current_user()

            self.assertNotEquals(user, None)
            self.assertIsInstance(user, User)
            self.assertEquals(user.name, 'Angie')

    def tearDown(self):
        """Reset db for next test."""

        db.session.close()
        db.drop_all()


class TestGetUserByEmail(unittest.TestCase):
    """Test our ability to get a User given an email."""

    def setUp(self):
        """Set up app, session key, and db."""

        app.config['TESTING'] = True

        # set up db
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()
        populate_test_db_users()

    def test_no_email(self):
        """Test what happens when no email is passed in."""

        user = get_user_by_email(None)

        self.assertEquals(user, None)

    def test_invalid_email(self):
        """Test what happens when no user in db has this email."""

        user = get_user_by_email('nobody@hasthis.email')

        self.assertEquals(user, None)

    def test_valid_email(self):
        """Test what happens when a user in the db has this email."""

        user = get_user_by_email('angie@fake.com')

        self.assertNotEquals(user, None)
        self.assertIsInstance(user, User)
        self.assertEquals(user.name, 'Angie')

    def tearDown(self):
        """Reset db for next test."""

        db.session.close()
        db.drop_all()


class TestIsLoggedIn(unittest.TestCase):
    """Test our ability to determine if someone is logged in."""

    def setUp(self):
        """Set up app, session key, and db."""

        app.config['TESTING'] = True

    def test_logged_in(self):
        """Test what happens when someone is logged in."""

        with app.test_request_context():
            session['user_id'] = 1
            logged_in = is_logged_in()

            self.assertEquals(logged_in, True)

    def test_not_logged_in(self):
        """Test what happens when someone is not logged in."""

        with app.test_request_context():
            logged_in = is_logged_in()

            self.assertEquals(logged_in, False)

    def test_user_in_session_is_null(self):
        """Test what happen if session is in wonky state (user_id=None)."""

        with app.test_request_context():
            session['user_id'] = None
            logged_in = is_logged_in()

            self.assertEquals(logged_in, False)

if __name__ == '__main__':
    unittest.main()
