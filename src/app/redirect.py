from urllib.parse import urlparse

from flask import url_for, request, redirect
from flask_wtf import FlaskForm
from wtforms import HiddenField

###
# This file contains a redirect form, the one we use for login. Its purpose is to redirect the user
# once he has logged in successfully to the hidden redirect value passed into the form.
###

def is_local_url(url):
    """
    Returns whether the given url is local, i.e. the scheme of the url and
    the network location part must be None.
    """
    try:
        url_info = urlparse(url)
    except ValueError:
        return False
    return not url_info.scheme and not url_info.netloc

def get_local_redirect():
    """
    Returns the redirect target of the current request if that target is local.
    """
    target = request.args.get('next')
    return target if is_local_url(target) else None


class RedirectForm(FlaskForm):
    """
    Represents a form which stores the current redirect target as a hidden
    field. When submitting the form, the application can than redirect to the
    intended target without passing the redirect target as request parameter.
    """
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        super(RedirectForm, self).__init__(*args, **kwargs)

        # Set the redirect target if not assigned
        if self.next.data is None:
            self.next.data = get_local_redirect()

    def redirect(self, endpoint='index', **values):
        """
        Redirects to the next form parameter if that url is local. Otherwise,
        redirects to the url associated with the given endpoint.
        """
        if is_local_url(self.next.data):
            return redirect(self.next.data)
        return redirect(url_for(endpoint, **values))
