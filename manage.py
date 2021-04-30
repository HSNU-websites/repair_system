import unittest

from flask_script import Manager

from app import create_app

app = create_app("production")
manager = Manager(app)


@manager.command
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    manager.run()
