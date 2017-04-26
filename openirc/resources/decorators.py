from functools import wraps

from flask_login import current_user, logout_user

def err(msg):
    return {'status': 'err', 'message': msg, 'data': -1}, 403


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user or not current_user.is_authenticated:
            return err('You must be logged in to access this page')
        if current_user and not current_user.is_confirmed():
            logout_user()
            return err('Please verify your email first')
        return f(*args, **kwargs)
    return decorated_function
