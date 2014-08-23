# coding=utf-8
"""Test for user model module."""
__author__ = 'akbar'

# from unittest import TestCase
from flask.ext.testing import TestCase as FlaskTestCase
from flask.ext.migrate import downgrade, upgrade

from users import APP
from users.database import db
from users.models import (
    add_user,
    edit_user,
    delete_user,
    get_user,
    get_user_by_email,
    get_all_users,
    )


class TestUser(FlaskTestCase):
    """Test User Model."""

    def create_app(self):
        app = APP
        app.config['TESTING'] = True
        return app

    #noinspection PyPep8Naming
    def setUp(self):
        self.user_to_add = dict(
            name='Akbar',
            email='test@gmail.com',
            website='http://www.ac.com',
            email_updates=True,
            latitude=12.32,
            longitude=-13.03,
            social_account=dict(twitter="johndoe"),
            )

    @classmethod
    def setUpClass(cls):
        with APP.test_request_context():
            upgrade(revision="head")

    #noinspection PyPep8Naming
    def tearDown(self):
        """Destructor."""
        db.session.remove()

    @classmethod
    def tearDownClass(cls):
        with APP.test_request_context():
            downgrade(revision="base")

    def test_add_user(self):
        """Test for add user function."""
        number_of_users_before = len(get_all_users())
        guid = add_user(**self.user_to_add)
        self.assertIsNotNone(guid)
        number_of_users_after = len(get_all_users())
        self.assertEqual(number_of_users_before + 1, number_of_users_after)

    def test_edit_user(self):
        """Test for edit user function."""
        guid = add_user(**self.user_to_add)
        edited_data = dict(
            name='Akbar Gumbira',
            email='gumbira@gmail.com',
            website='http://www.akbargumbira.com',
            email_updates=True,
            latitude=-6.32,
            longitude=102.03)
        guid = edit_user(guid, **edited_data)
        user = get_user(guid)
        for key in edited_data:
            if key != 'email_updates':
                self.assertEqual(edited_data[key], getattr(user, key))
        self.assertEqual(user.email_updates, 1)

    def test_delete_user(self):
        """Test for delete user function."""
        guid = add_user(**self.user_to_add)
        self.assertIsNotNone(guid)
        delete_user(guid)
        user = get_user(guid)
        self.assertEqual(user, None)

    def test_get_user(self):
        """Test for getting user function."""
        guid = add_user(**self.user_to_add)
        self.assertIsNotNone(guid)
        user = get_user(None)
        assert user is None
        user = get_user(guid)
        self.assertEqual('Akbar', user.name)

    def test_get_user_by_email(self):
        """Test for getting user function."""
        guid = add_user(**self.user_to_add)
        self.assertIsNotNone(guid)
        user = get_user_by_email(self.user_to_add['email'])
        self.assertEqual('Akbar', user.name)
