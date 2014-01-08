"""
WSGI webapp using Flask
"""

import os

from Queue import Queue, Empty

from flask import Flask
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.secret_key = 'THIS IS REALLY SECRET'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL',
                   'sqlite:///../app.db')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import webapp.views
