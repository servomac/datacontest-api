from flask_script import Manager, Server
from flask_script.commands import Clean, ShowUrls

from datacontest.app import create_app


app = create_app()
manager = Manager(app)

manager.add_command('run', Server())
manager.add_command('urls', ShowUrls())
manager.add_command('clean', Clean())

if __name__ == '__main__':
    manager.run()
