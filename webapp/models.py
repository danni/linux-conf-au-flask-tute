"""
Models and forms for our webapp
"""

from flask.ext.wtf import Form

from wtforms import validators
from wtforms.ext.sqlalchemy.orm import model_form

from . import db


class User(db.Model):
    """A user"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)

UserForm = model_form(User, base_class=Form, field_args={
    'email': {
        'validators': [validators.Email()],
    },
})
