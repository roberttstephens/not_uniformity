import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

ADMINS = frozenset(['roberttstephens@gmail.com'])
SECRET_KEY = 'SecretKey'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
#SQLALCHEMY_DATABASE_URI = 'postgresql://uniformity_test:uniformity_test@db1/uniformity_test'
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2

CSRF_ENABLED = True
CSRF_SESSION_KEY = "something_impossible"


