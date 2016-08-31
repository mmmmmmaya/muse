from flask import redirect

from model import db, User
from utils.authentication import add_session_info, hash_password
from utils.general import ALERT_COLORS, flash_message, get_user_by_email


def add_user_to_db(name, email, password, zipcode, country):
    """Create a new user and add to db.

    Returns id of new user.
    """

    hashed_password = hash_password(password)

    new_user = User(name=name,
                    email=email,
                    password=hashed_password,
                    zipcode=zipcode,
                    country=country)

    db.session.add(new_user)
    db.session.commit()

    return new_user


def all_fields_filled(name, email, password):
    """Check to see if the following (required) fields have values."""

    filled = False

    if name and email and password:
        filled = True

    return filled


def register_user(name, email, password, zipcode, country):
    """Add new user to the database."""

    if user_already_exists(email):
        flash_message('That user already exists. Please log in.',
                      ALERT_COLORS['yellow'])
        response = redirect('/login')

    else:
        user = add_user_to_db(name, email, password, zipcode, country)
        add_session_info(user)
        flash_message('Account created successfully.',
                      ALERT_COLORS['green'])
        response = redirect('/')

    return response


def user_already_exists(email):
    """Checks to make sure new registration does not conflict with
    an existing user.
    """

    exists = False

    user = get_user_by_email(email)

    if user:
        exists = True

    return exists
