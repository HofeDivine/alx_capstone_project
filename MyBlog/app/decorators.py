# decorators.py

from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

def custom_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('routes.userlogin'))  # Redirect to login page
        return func(*args, **kwargs)
    return decorated_view
