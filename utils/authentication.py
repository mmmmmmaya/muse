from flask import redirect, session
from sqlalchemy.orm.exc import NoResultFound

from model import User
from utils.general import ALERT_COLORS, flash_message, get_user_by_email


def add_session_info(user_id):
    """Add user_id to session."""

    if user_id:
        session['user_id'] = user_id


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


def remove_session_info():
    """Remove user_id from session."""

    del session['user_id']


def verify_password(user, password):
    """Ensure user-entered password matches password in db."""

    if user.password == password:
        add_session_info(user.id)
        flash_message('You were successfully logged in.', ALERT_COLORS['green'])
        response = redirect('/')

    else:
        flash_message('Incorrect password.', ALERT_COLORS['red'])
        response = redirect('/login')

    return response
