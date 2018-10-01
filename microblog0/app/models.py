"""
Implement SQLAlchemy objects for the tables in the application database;

The classes inherit from db.Model which is a base class for all Flask-SQLAlchemy
data models. The variables after the class definition are the fields in the table.

The __repr__ method defines how the objects of the class are printed.

All db.Model classes have a query attribute that is the entry point to run
database queries.

To deploy to the app...
    1. run `flask db migrate -m "write message here"`
    2. run `flask db upgrade`
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin
from hashlib import md5

@login.user_loader              # registers the function with Flask-Login
def load_user(id):
    """
    Load a user (User object) into memory. This user is stored in a variable
    called current_user that is used in the login() function in the routes
    module.
    """
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    """
    Data for the users of the application.

    The 'UserMixin' arg is contains generic implementations for Flask-Login and
    instantiates the following properties of the user:
        1. is_authenticated: True if user has valid credentials, False otherwise
        2. is_active: True if account if active, False otherwise
        3. is_anonymous: False for regular users, True for special, anonymous users
        4. get_id(): method that returns a unique identifier as a string

    The two password methods are used to hash a password and then check if a
    given password matches the hash.

    PRIMARY_KEY = 'id', one per user
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index = True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """
        Return the URL of the user's avatar image, scaled to the size passed
        into the 'size' argument
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
                    digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    """
    Data for the blog posts

    PRIMARY_KEY = 'id', one per blog post
    FOREIGN_KEY = 'user_id', relates the the 'id' in the User table
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
