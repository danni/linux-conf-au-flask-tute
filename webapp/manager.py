"""
Webapp manager
"""

from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager, Server as ServerCommand

from . import app
from .collectstatic import CollectBower


class Server(ServerCommand):
    def handle(self, *args, **kwargs):
        app.running = True

        super(Server, self).handle(*args, **kwargs)

        print "Shutting down"
        app.running = False


manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server)
manager.add_command('collectstatic', CollectBower)
