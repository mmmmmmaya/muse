from Crypto.Hash import SHA256
from flask import redirect, session
from sqlalchemy.orm.exc import NoResultFound

from model import User
from utils.general import ALERT_COLORS, flash_message, get_user_by_email


def add_session_info(user):
    """Add user info to session."""

    if user:
        session['user'] = {
            'id': user.id,
            'name': user.name
        }


def attempt_login(email, password):
    """Try to log the user in.

    Returns Flask response.
    """

    user = get_user_by_email(email)

    if user:
        response = verify_password(user, password)

    else:
        flash_message('No registered user found. Please register.',
                      ALERT_COLORS['blue'])
        response = redirect('/register')

    return response


def hash_password(password):
    """Take a password and return its hashed version."""

    hashed_password = SHA256.new()
    hashed_password.update(password)

    return hashed_password.hexdigest()


def remove_session_info():
    """Remove user info from session."""

    if 'user' in session:
        del session['user']


def verify_password(user, password):
    """Ensure user-entered password matches password in db."""

    hashed_password = hash_password(password)

    if user.password == hashed_password:
        add_session_info(user)
        flash_message('You were successfully logged in.', ALERT_COLORS['green'])
        response = redirect('/')

    else:
        flash_message('Incorrect password.', ALERT_COLORS['red'])
        response = redirect('/login')

    return response
