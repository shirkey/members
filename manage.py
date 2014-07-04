from flask.ext.script import Manager

from users import APP

if __name__ == "__main__":
    manager = Manager(APP)
    manager.run()
