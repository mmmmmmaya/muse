from flask import redirect

from model import db, User
from utils.authentication import add_session_info, hash_password, password_matches
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


def update_account_info(user, form):
    """Update information stored about a user in the db."""

    if 'password' in form:
        response = update_password(user, form)

    else:
        response = update_user_details(user, form)

    return response


def update_password(user, form):
    """Update the password stored in db."""

    old_password = form.get('old-password', '')

    if password_matches(user, old_password):
        user.password = hash_password(form['password'])
        db.session.commit()

        flash_message('Password successfully updated.',
                      ALERT_COLORS['green'])
        response = redirect('/account')

    else:
        flash_message('Incorrect current password.',
                      ALERT_COLORS['red'])
        response = redirect('/account')

    return response


def update_user_details(user, form):
    """Update name, email, etc on user account."""

    if get_user_by_email(form.get('email')):
        flash_message('An account with that email address already exists.',
                      ALERT_COLORS['red'])

    else:
        user.name = form.get('name', user.name)
        user.email = form.get('email', user.email)
        user.zipcode = form.get('zipcode', user.zipcode)
        user.country = form.get('country', user.country)

        flash_message('Account successfully updated.',
                      ALERT_COLORS['green'])

        db.session.commit()

    return redirect('/account')


def user_already_exists(email):
    """Checks to make sure new registration does not conflict with
    an existing user.
    """

    exists = False

    user = get_user_by_email(email)

    if user:
        exists = True

    return exists
