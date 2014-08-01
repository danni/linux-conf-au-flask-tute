"""
WSGI webapp using Flask
"""

import os

from Queue import Queue, Empty

from flask import Flask
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = os.environ.get('OPENSHIFT_SECRET_TOKEN',
                                'THIS IS REALLY SECRET')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_DEFAULT_URL']

try:
    app.static_folder = os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi')
except KeyError:
    pass

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import webapp.views
