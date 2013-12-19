"""
WSGI webapp using Flask
"""

from flask import Flask, redirect, render_template, url_for


app = Flask(__name__)


@app.route('/')
def index():
    """Homepage"""

    return "Hello, linux.conf.au"


@app.route('/a-redirect')
def a_redirect():
    """Redirect the user"""

    return redirect(url_for('a_template'))


@app.route('/a-template')
def a_template():
    """Render a template"""

    return render_template('template.html')


if __name__ == '__main__':
    app.run(debug=True)
