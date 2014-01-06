"""
WSGI webapp using Flask
"""

from Queue import Queue

from flask import (Flask,
                   Response,
                   flash,
                   get_flashed_messages,
                   message_flashed,
                   redirect,
                   render_template,
                   request,
                   stream_with_context,
                   url_for)
from flask import json
from flask.ext.wtf import Form
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy

from wtforms import validators
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

UserForm = model_form(User, base_class=Form, field_args={
    'email': {
        'validators': [validators.Email()],
    },
})


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

        flash("User {email} registered".format(email=obj.email))

        return redirect(url_for('register'))

    return render_template('template.html',
                           form=form,
                           users=User.query.all())


@app.route('/events/stream')
def get_events():
    """Returns an event-stream"""

    queue = Queue()

    @message_flashed.connect_via(app)
    def store_flashed_message(sender, message, category, **kwargs):
        """
        Add a flashed message to the queue
        """

        queue.put(message)

    def format_messages(messages):
        return 'data: ' + json.dumps(messages) + '\n\n'

    @stream_with_context
    def generate():
        """
        Yield JSON-encoded events
        """

        yield format_messages(get_flashed_messages())

        while True:
            yield format_messages([queue.get()])
            queue.task_done()  # eat the queue item

    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    manager.run()
