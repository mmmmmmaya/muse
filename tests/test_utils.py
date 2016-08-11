from model import db, User


def populate_test_db_users():
    """Create user data in fake db for testing."""

    fake_user = User(name='Angie',
                     email='angie@fake.com',
                     password='pass')

    db.session.add(fake_user)
    db.session.commit()
