"""
Flask-Script to collect static
"""

import json
import os
import shutil
import subprocess

from flask import current_app
from flask.ext.script import Command


class CollectBower(Command):
    """Collects static files for Bower"""

    def run(self):
        paths = json.loads(subprocess.check_output([
            'bower', 'list', '--paths'
        ]))

        folder = os.path.join(current_app.static_folder, 'bower')

        try:
            shutil.rmtree(folder)
        except OSError:
            pass

        os.makedirs(folder)

        for item in paths.values():
            print "Installed {item}".format(item=item)
            shutil.copy(item, folder)
