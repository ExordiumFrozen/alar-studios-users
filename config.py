import os
basedir = os.path.abspath(os.path.dirname(__file__))

TITLE = 'Alar Studio User Management'

CSRF_ENABLED = True
SECRET_KEY = 'nthvbyfnjh'

# database settings
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'mysql://task1_exordium:task1_exordium@localhost/task1_exordium'

USERS_PER_PAGE = 5
