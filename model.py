from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """User account."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(10))
    country = db.Column(db.String(2))

    recordings = db.relationship('Recording')

    def __repr__(self):
        """String representation of User."""

        return '<User id: %s, email:%s>' % (self.id, self.email)


class Theme(db.Model):
    """The theme of each sound set."""

    __tablename__ = 'themes'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        """String representation of Theme."""

        return '<Theme id: %s, name: %s>' % (self.id, self.name)


class Recording(db.Model):
    """A single song recording."""

    __tablename__ = 'recordings'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    public = db.Column(db.Boolean, nullable=False, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user = db.relationship('User')
    views = db.relationship('View')
    keypresses = db.relationship('KeyPress', order_by='KeyPress.id')

    def __repr__(self):
        """String representation of Recording."""

        return '<Recording id: %s>' % (self.id)


class KeyPress(db.Model):
    """A single keypress within a song recording."""

    __tablename__ = 'keypresses'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recording_id = db.Column(db.Integer, db.ForeignKey('recordings.id'))
    key_pressed = db.Column(db.String(1), nullable=False)
    pressed_at = db.Column(db.BigInteger, nullable=False)
    theme = db.Column(db.Integer, db.ForeignKey('themes.id'))

    recording = db.relationship('Recording')

    def __repr__(self):
        """String representation of KeyPress."""

        return '<KeyPress id: %s, key: %s, recording_id: %s>' % (self.id,
                                                                 self.key_pressed,
                                                                 self.recording_id)


class View(db.Model):
    """Every time someone loads a particular song's link in a browser."""

    __tablename__ = 'views'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recording_id = db.Column(db.Integer, db.ForeignKey('recordings.id'))
    ip_address = db.Column(db.String(15))
    viewed_at = db.Column(db.DateTime, default=datetime.now())

    recording = db.relationship('Recording')

    def __repr__(self):
        """String representation of View."""

        return '<View id: %s>' % (self.id)


# These help connect us to the database.
def connect_to_db(app, uri='postgresql:///muse'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_ECHO'] = True

    db.app = app
    db.init_app(app)
    print "Connected to DB."


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
