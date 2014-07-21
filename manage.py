from flask.ext.script import Manager
from flask.ext.migrate import MigrateCommand

from users import APP

if __name__ == "__main__":
    manager = Manager(APP)
    manager.add_command("db", MigrateCommand)
    manager.run()
