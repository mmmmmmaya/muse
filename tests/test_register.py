import unittest

from model import connect_to_db, db, User
from server import app
from utils.register import (add_user_to_db, all_fields_filled,
                            register_user, user_already_exists)
from utils.test import populate_test_db_users


class TestAddUserToDb(unittest.TestCase):
    """Test adding a User to the db."""

    def setUp(self):
        """Set up app, session key, and db."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'super secret'

        # setup test db
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()
        populate_test_db_users()

    def test_fully_qualified_user(self):
        """Test when all fields are supplied."""

        add_user_to_db(name='Angie',
                       email='angie@fake.com',
                       password='pass',
                       zipcode='99999',
                       country='US')

        user = User.query.get(1)

        self.assertNotEquals(user, None)
        self.assertIsInstance(user, User)
        self.assertEquals(user.name, 'Angie')

    def test_only_required_fields(self):
        """Test all required fields supplied but optional fields empty."""

        add_user_to_db(name='Angie',
                       email='angie@fake.com',
                       password='pass',
                       zipcode=None,
                       country=None)

        user = User.query.get(1)

        self.assertNotEquals(user, None)
        self.assertIsInstance(user, User)
        self.assertEquals(user.name, 'Angie')

    def tearDown(self):
        """Clear db for next test."""

        db.session.close()
        db.drop_all()


class TestAllFieldsFilled(unittest.TestCase):
    """Test to make sure all necessary fields are full."""

    def test_missing_name(self):
        """Test what happens if name is None."""

        name = None
        name2 = ''
        email = 'some@email.com'
        password = 'password'

        filled = all_fields_filled(name, email, password)
        filled2 = all_fields_filled(name2, email, password)

        self.assertEquals(filled, False)
        self.assertEquals(filled2, False)

    def test_missing_email(self):
        """Test what happens if email is None."""

        name = 'Angie'
        email = None
        email2 = ''
        password = 'password'

        filled = all_fields_filled(name, email, password)
        filled2 = all_fields_filled(name, email2, password)

        self.assertEquals(filled, False)
        self.assertEquals(filled2, False)

    def test_missing_password(self):
        """Test what happens if password is None."""

        name = 'Angie'
        email = 'some@email.com'
        password = None
        password2 = ''

        filled = all_fields_filled(name, email, password)
        filled2 = all_fields_filled(name, email, password2)

        self.assertEquals(filled, False)
        self.assertEquals(filled2, False)

    def test_all_filled(self):
        """Test when all fields full."""

        name = 'Angie'
        email = 'some@email.com'
        password = 'password'

        filled = all_fields_filled(name, email, password)

        self.assertEquals(filled, True)


class TestRegisterUser(unittest.TestCase):
    """Test that registration works properly."""

    def setUp(self):
        """Set up app, session key, and db."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'super secret'

        # setup test db
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()
        populate_test_db_users()

    def test_register_existing_user(self):
        """Test what happens when trying to register a user that already exists."""

        count_before = len(User.query.all())

        with app.test_request_context():
            response = register_user(name='Angie',
                                     email='angie@fake.com',
                                     password='pass',
                                     zipcode='99999',
                                     country='US')

        count_after = len(User.query.all())
        count_difference = count_after - count_before

        self.assertEquals(302, response.status_code)
        self.assertEquals('/login', response.location)
        self.assertEquals(count_difference, 0)

    def test_register_not_existing_user(self):
        """Test what happens when trying to register a user that does
        not already exist."""

        count_before = len(User.query.all())

        with app.test_request_context():
            response = register_user(name='Angie',
                                     email='nobody@hasthis.email',
                                     password='pass',
                                     zipcode='99999',
                                     country='US')

        count_after = len(User.query.all())
        count_difference = count_after - count_before

        self.assertEquals(302, response.status_code)
        self.assertEquals('/', response.location)
        self.assertEquals(count_difference, 1)

    def tearDown(self):
        """Clear db for next test."""

        db.session.close()
        db.drop_all()


class TestUserAlreadyExists(unittest.TestCase):
    """Test adding a User to the db."""

    def setUp(self):
        """Set up app, session key, and db."""

        app.config['TESTING'] = True

    def test_user_already_exists(self):
        """Test what happens when you query with an email that is in the db."""

        exists = user_already_exists('angie@fake.com')

        self.assertEquals(exists, True)

    def test_user_does_not_already_exist(self):
        """Test what happens when you query with an email that is not in the db."""

        exists = user_already_exists('nobody@hasthis.email')

        self.assertEquals(exists, False)

    def tearDown(self):
        """Clear db for next test."""

        db.session.close()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
