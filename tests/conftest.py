"""
Global fixtures for tests
"""

import pytest

from webapp import (app as flask_app,
                    db as flask_db)


@pytest.fixture(scope='session')
def db():
    """Set up the database"""

    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

    flask_db.create_all()

    return flask_db


@pytest.fixture(scope='session')
def app(db):
    """Set up the Flask test client"""

    return flask_app.test_client()
