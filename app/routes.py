"""
Functions (Routes) that define app behavior when navigated to certain pages of the app;
Each route...
    - Has one or more corresponding relative urls defined by the @app.route() method;
    - Returns the result of the render_template method which renders the content of an
        html file (first argument) and passes in any additional parameters to the html file
        which are handled in the HTML file via the Jinja2 template engine
"""

from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime

@app.before_request     # run this function before a view function is invoked
def before_request():
    """
    This function is called before any other view function is called; Check if
    the current_user is logged in, if so, set the last_seen field to the current
    time.
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required     # can only be viewed if user is logged in
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Renders the HTML in 'templates/login.html' and upon submit...
        - Checks if the user is logged in, if so, redirects to the index page
        - Checks for a valid username/password combo, handles if combo is invalid
        - If username/password combo is valid, directs the user to the index page
            or the page they tried to access before logging in.
    """
    if current_user.is_authenticated:       # Redirect the user to the index page if the user is already logged in
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():                                           # FALSE if form submitted via GET, TRUE if form submitted via POST (submit button)
        user = User.query.filter_by(username=form.username.data).first()   # Assign the user that just logged in to 'user' variable
        if user is None or not user.check_password(form.password.data):     # check the password
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)                    # comes from Flask-Login, register the user as logged in, future pages will identify this user as `current_user`
        next_page = request.args.get('next')                                # get the next page to go to after logging in, if any
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Renders the HTML in 'templates/register.html' and upon submit...
    - Checks if the user is logged in, if so, redirects to the index page
    - Creates a user object from the data in the form. The RegistrationForm
        includes validator methods to ensure unique username and email.
    - Commits the new user to the database.
    - Redirects the client to the login page.
    """
    if current_user.is_authenticated:       # Redirect the user to the index page if the user is already logged in
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
        email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required     # can only be viewed if user is logged in
def user(username):
    user = User.query.filter_by(username=username).first_or_404()   # raise an exception if user not in db
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Renders the HTML in 'templates/edit_profile.html' and checks for a submission
    (POST) or a GET request. A get request occurs when the browser requests the
    form, such as when navigating to the link.
    If submission of form via a POST request...
        - Updates the username and about_me fields in the db with the data in the
            form
    Else if form is spawned via a GET request...
        - Pre-populate the form fields with the data that is already in the db for
            the current user (current_user)

    """
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
