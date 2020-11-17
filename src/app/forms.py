from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import InputRequired, Optional

from app.redirect import RedirectForm

###
# This file contains the two forms that we use in our application.
# One for login and one for searching the record of our expenses
###

try:
    from html import escape
except ImportError:
    from cgi import escape


class LoginForm(RedirectForm):
    """
    Represents a login form with fields:
        * username (a string)
        * password (a password)
        * remember_me (a boolean)
    """

    username = StringField(
        'Username:',
        validators=[InputRequired()]
    )
    password = PasswordField(
        'Password:',
        validators=[InputRequired()]
    )
    remember_me = BooleanField(
        'Remember me:',
        default=False
    )


class SearchExpenseForm(FlaskForm):
    """
    Represents a list of record for the corresponding user with the field:
        * search_string (a string, query on the record description)
    """
    def __init__(self, prefix='search_task', *args, **kwargs):
        super(SearchExpenseForm, self).__init__(prefix=prefix, *args, **kwargs)

    search_string = StringField(
        'Expense description:',
        validators=[Optional()]
    )


