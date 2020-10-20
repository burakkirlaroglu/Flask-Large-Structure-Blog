import os
from datetime import timedelta
_basedir = os.path.abspath(os.path.dirname(__file__))


DEBUG = True

SECRET_KEY = "somethingimpossibletoguess"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'large_blog.db')
DATABASE_CONNECT_OPTIONS = {}

# PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
# SESSION_REFRESH_EACH_REQUEST = True

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY = "somethingimpossibletoguess"


MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'yourmail@gmail.com'
MAIL_PASSWORD = 'YourPassword.'
