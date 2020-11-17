import os

from flask import Flask, g, request
from flask_login import current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
static_dir = os.path.join(os.path.dirname(__file__), 'static')

flaskapp = Flask("SQL injection demo", template_folder=template_dir, static_folder=static_dir)
flaskapp.config.from_object('config')

# Flask-SQLAlchemy for database connections
db = SQLAlchemy(flaskapp)

# Flask-Login for user session handling
lm = LoginManager()
lm.init_app(flaskapp)
lm.login_view = 'login'
lm.login_message = 'Please login.'

# Avoid circular imports
import app.models

@lm.user_loader
def user_loader(id):
    """
    The callback for reloading a user from the session.
    """
    return models.User.query.get(int(id))


@flaskapp.before_request
def before_request():
    """
    This function is run before each request.
    """
    g.user = current_user


@flaskapp.after_request
def after_request(resp):
    """
    This function is run after each request.
    """
    if 'themeId' in request.args:
        theme_id = request.args.get('themeId')
    elif 'themeId' in request.cookies:
        theme_id = request.cookies.get('themeId')
    else:
        theme_id = '0'

    cookie = bytes(theme_id, 'ascii')
    resp.set_cookie('themeId', cookie)
    resp.cache_control.max_age = 1
    return resp

# Import the views/app to start
import app.views
