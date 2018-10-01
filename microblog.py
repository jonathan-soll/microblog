"""
Defines the app; Imports the app and it's corresponding database; Defines the
flask shell context via the make_shell_context() function
"""

from app import app, db
from app.models import User, Post

@app.shell_context_processor         # registers the function as a shell context function
def make_shell_context():
    """
    Defines a dictionary in which each item is a variable that is made available
    after running the flask shell instead of having to import them
    """
    return {'db': db, 'User': User, 'Post': Post}
