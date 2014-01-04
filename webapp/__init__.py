"""
WSGI webapp using Flask
"""

from flask import Flask, request, render_template, redirect, url_for
from flask.ext.wtf import Form
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy

from wtforms.ext.sqlalchemy.orm import model_form


app = Flask(__name__)
app.secret_key = 'THIS IS REALLY SECRET'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../app.db'

manager = Manager(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    """A user"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)

UserForm = model_form(User, base_class=Form)


@app.route('/')
def index():
    """Homepage"""

    return "Hello, linux.conf.au"


@app.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new user"""

    obj = User()
    form = UserForm(request.form, obj)

    if form.validate_on_submit():
        form.populate_obj(obj)
        db.session.add(obj)
        db.session.commit()

        return redirect(url_for('register'))

    return render_template('template.html',
                           form=form,
                           users=User.query.all())


if __name__ == '__main__':
    manager.run()
