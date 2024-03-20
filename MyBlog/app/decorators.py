# decorators.py

from functools import wraps
from flask import redirect, url_for
from flask_login import current_user
import re


def custom_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('routes.userlogin'))  # Redirect to login page
        return func(*args, **kwargs)
    return decorated_view
def strip_html_tags(text):
    """Remove HTML tags from the given text."""
    return re.sub('<[^<]+?>', '', text)