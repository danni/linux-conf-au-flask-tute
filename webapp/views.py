"""
Views for our web app
"""

from flask import (Response,
                   flash,
                   get_flashed_messages,
                   json,
                   message_flashed,
                   redirect,
                   render_template,
                   request,
                   stream_with_context,
                   url_for)

from . import app, db
from .models import User, UserForm


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


@app.route('/events')
def get_events():
    """Returns the events"""

    return render_template('events.html')


@app.route('/events/stream')
def get_events_stream():
    """Returns an event-stream"""

    queue = Queue()
    running = True

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

        while app.running:
            try:
                item = queue.get(timeout=1)

                yield format_messages([item])
                queue.task_done()  # eat the queue item
            except Empty:
                pass

    return Response(generate(), mimetype='text/event-stream')
