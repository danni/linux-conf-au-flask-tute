"""
WSGI webapp using Flask
"""

from flask import Flask, render_template
from flask.ext.wtf import Form

from wtforms import TextField, validators


app = Flask(__name__)


@app.route('/')
def index():
    """Homepage"""

    return "Hello, linux.conf.au"


class RegoForm(Form):
    """A simple rego form"""

    email = TextField('Email', validators=(validators.DataRequired(),
                                           validators.Email()))


@app.route('/register', methods=('GET', 'POST'))
def get_register():
    """Handle the registration form"""

    form = RegoForm()

    if form.validate_on_submit():
        return "Success"

    return render_template('template.html', form=form)

if __name__ == '__main__':
    app.secret_key = 'THIS IS REALLY SECRET'
    app.run(debug=True)
