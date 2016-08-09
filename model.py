from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


class User(db.Model):
    """User account."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(10))
    country = db.Column(db.String(2))


class Theme(db.Model):
    """The theme of each sound set."""

    __tablename__ = 'themes'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(25), nullable=False)


class Recording(db.Model):
    """A single song recording."""

    __tablename__ = 'recordings'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    public = db.Column(db.Boolean, nullable=False, default=True)
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    content = db.Column(db.Text, nullable=False)


class View(db.Model):
    """Every time someone loads a particular song's link in a browser."""

    __tablename__ = 'views'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recording_id = db.Column(db.Integer, db.ForeignKey('recordings.id'))
    ip_address = db.Column(db.String(15))
    viewed_at = db.Column(db.DateTime, default=datetime.now())
