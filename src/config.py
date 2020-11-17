import os

# Just a standard config file for Flask application

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE_URI = os.path.join(basedir, 'app.db')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True
DATE_FORMAT = '%Y-%m-%d'

SECRET_KEY = '<insert-a-secret-key-here>'