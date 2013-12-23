"""
WSGI webapp using Flask
"""

from flask import Flask
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'THIS IS REALLY SECRET'

manager = Manager(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    """Homepage"""

    return "Hello, linux.conf.au"


if __name__ == '__main__':
    manager.run()
