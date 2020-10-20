from functools import wraps
from blog import db
from flask import g,flash,redirect,url_for,request,session
from blog.user.models import User

def login_required(f):
    @wraps(f)
    def decorator_function(*args, **kwargs):
        if g.user is None:
            flash('You need to be signed in for this page.', "warning")
            return redirect(url_for('users.login', next=request.path))
        return f(*args, **kwargs)
    return decorator_function


def login_management(f):
    @wraps(f)
    def decorator_function(*args, **kwargs):
        if 'user_id' in session:
            flash("You have already in login.", "danger")
            return redirect(url_for("users.profile", next=request.path))
        return f(*args, **kwargs)
    return decorator_function
