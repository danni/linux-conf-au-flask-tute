"""
app and db are available in the test scope
"""


def test_index(app):
    """Test I can get the index page"""

    rv = app.get('/')

    print rv.data

    assert rv.data == "Hello"
