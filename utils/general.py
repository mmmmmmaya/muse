from flask import flash, session
from markupsafe import Markup
from sqlalchemy.orm.exc import NoResultFound

from model import User

ALERT_COLORS = {
    'red': 'danger',
    'yellow': 'warning',
    'green': 'success',
    'blue': 'info',
}


def flash_message(msg, alert_type):
    """Add a stylized flash message to the browser session."""

    if msg:
        html = """
            <div class="alert alert-%s alert-dismissible" role="alert">
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
                    %s
            </div>
            """ % (alert_type, msg)

        markup_msg = Markup(html)
        flash(markup_msg)


def get_current_user():
    """Returns the User that is currently logged into the site."""

    user = None

    if 'user_id' in session:
        try:
            user = User.query.get(session['user_id'])

        except NoResultFound:
            pass

    return user


def get_user_by_email(email):
    """Return a single User based on the email address."""

    try:
        return User.query.filter_by(email=email).one()

    except NoResultFound:
        return None


def is_logged_in():
    """Determines whether someone is logged into the site.

    Returns boolean.
    """

    logged_in = False

    # if 'user_id' in session and session['user_id'] is not None
    if session.get('user_id', None):
        logged_in = True

    return logged_in
