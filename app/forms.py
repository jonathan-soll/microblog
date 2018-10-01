"""
Declare different forms we will use to have users navigate our web application.
The forms inherit from the FlaskForm class and define their own unique attributes.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    """
    Form used to allow users to login to the website. This form is used in the
    login() function in routes.py and passed to login.html to be displayed on the
    login page.
    """
    username    = StringField('Username', validators=[DataRequired()])      # [DataRequired()] ensures not blank
    password    = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit      = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username    = StringField('Username', validators=[DataRequired()])
    email       = StringField('Email', validators=[DataRequired(), Email()])
    password    = PasswordField('Password', validators=[DataRequired()])
    password2   = PasswordField(
                    'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit      = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
