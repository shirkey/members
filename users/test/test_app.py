# coding=utf-8
"""Tests for the application web urls.
:copyright: (c) 2013 by Tim Sutton
:license: GPLv3, see LICENSE for more details.
"""
import os
import json

from flask_testing import TestCase
from flask_migrate import downgrade, upgrade

from users import LOGGER
from users.views import APP as app
from users.database import db
from users.models import add_user, get_user

import collections


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)


class AppTestCase(TestCase):
    """Test the application."""

    @classmethod
    def setUpClass(cls):
        """
        Run migrations
        """
        with app.test_request_context():
            upgrade(revision="head")

    @classmethod
    def tearDownClass(cls):
        with app.test_request_context():
            downgrade(revision="base")

    def create_app(self):
        """Passthrough app instance"""
        return app

    def setUp(self):
        """unittest setup"""
        app.config.from_pyfile(os.path.join(app.root_path, 'test/test_config.py'))
        self.client = app.test_client()
        # db.create_all()
        self.correct_user_data = dict(
            name='Akbar',
            email='test@gmail.com',
            website='http://www.ac.com',
            email_updates=True,
            latitude=12.32,
            longitude=-13.03,
            social_account=dict(
                twitter="johndoe"
            ),
        )

        self.wrong_user_data = dict(
            name='',
            email='testgmaicom',
            website='http://www.ac.com',
            email_updates=True,
            latitude=12.32,
            longitude=-13.03,
            social_account=dict(
                twitter="johndoe",
            )
        )

        self.edited_user_data = dict(
            name='Akbar Gumbira',
            email='test@gmail.com',
            website='http://www.ac.com',
            email_updates=True,
            latitude=12.32,
            longitude=-13.03,
            social_account=dict(
                twitter="mrsmith",
            )
        )

    def tearDown(self):
        """Destructor."""
        db.session.remove()

    def test_url_root_get(self):
        """GET /"""
        result = self.client.get('/', follow_redirects=True)
        self.assert200(result, message="URL / GET failed.")

    def test_url_root_post(self):
        """POST /"""
        result = self.client.post('/', data=dict(), follow_redirects=True)
        self.assert405(result, message="URL / POST should not be allowed.")

    def test_url_users_data_get(self):
        """GET /users.json"""
        result = self.client.get(
            '/users.json',
            follow_redirects=True)
        self.assert200(result, message="URL /users.json GET failed.")

    def test_url_users_data_get(self):
        """POST /users.json"""
        result = self.client.get(
            '/users.json',
            data=dict(),
            follow_redirects=True)
        self.assert200(result, message="URL /users.json POST failed.")

    def test_users_data_correct(self):
        """Test the users json response works."""
        data = self.correct_user_data
        data["social_account"] = {
            "twitter": data.pop("twitter", ""),
        }
        guid = add_user(**data)
        if guid is not None:
            result = self.client.post(
                '/users.json',
                follow_redirects=True)
            self.assertIn(self.correct_user_data['name'], result.data, 'Correct data not found')

    def test_add_user_duplicate(self):
        url = '/add_user'
        user_data = {
            'name': 'Bounce_Effect_Bob',
            'email': 'noduplicates@gmail.com',
            'website': 'http://www.noduplicates.com',
            'email_updates': True,
            'latitude': 12.32,
            'longitude': -13.03,
            'twitter': 'bouncing'
        }
        result = self.client.post(
            url,
            data=user_data,
            follow_redirects=True)
        self.assertEquals(result.status_code, 200, 'Expected HTTP status code 200/OK')

        result = self.client.post(
            url,
            data=user_data,
            follow_redirects=True)
        self.assertEquals(result.status_code, 409, 'Expected HTTP status code 409/Conflict')

    def test_add_user_success(self):
        """Test the user added json response works."""
        url = '/add_user'
        data = flatten(self.correct_user_data)
        result = self.client.post(
            url,
            data=data,
            follow_redirects=True)
        self.assertEquals(result.status_code, 200, 'Expected HTTP status code 200/OK')
        data = result.json
        self.assertIn(
            self.correct_user_data['name'],
            data,
            'expected add_user success')

    def test_add_user_error(self):
        url = '/add_user'
        data = flatten(self.wrong_user_data)
        result = self.client.post(
            url,
            data=data,
            follow_redirects=True,
        )

        self.assertEquals(result.status_code, 400, 'Expected HTTP status code 400/Bad Request')
        # self.assertEquals(result.json['type'], u'Error', "Expected add_user error")

    def test_edit_user_view(self):
        """Test the edit_user_view function.
        """
        data = self.wrong_user_data
        guid = add_user(**data)
        url = '/edit/%s' % guid
        result = self.client.get(
            url,
            data=flatten(data),
            follow_redirects=True)
        self.assertEquals(result.status_code, 200, 'Expected HTTP status code 200/OK')
#        self.assertEquals(result.json['name'], 'Akbar Gumbira', "Expected name to change")

    def test_edit_user_controller(self):
        """Test the edit_user_view function.
        """
        url = '/edit_user'
        data = self.correct_user_data
        guid = add_user(**data)
        edited_data = self.edited_user_data
        edited_data['guid'] = guid
        result = self.client.post(
            url,
            data=flatten(edited_data),
            follow_redirects=True)
        self.assertEquals(result.status_code, 200, 'Expected HTTP status code 200/OK')
        self.assertEquals('Akbar Gumbira', result.json['name'], 'Expected edit_user success')

    def test_delete_user_view(self):
        """Test the delete_user_view function.
        """
        data = self.correct_user_data
        guid = add_user(**data)
        url = '/delete/%s' % guid
        try:
            self.client.post(
                url,
                data=dict(),
                follow_redirects=True)
            user = get_user(guid)
            self.assertIsNone(user)

        except Exception, e:
            LOGGER.exception('Basic front page load failed.')
            raise e

    def test_download_view(self):
        """Test the download_view function."""
        url = '/download'
        try:
            return self.client.get(url, data=dict(), follow_redirects=True)
        except Exception, e:
            LOGGER.exception('Basic front page load failed.')
            raise e

    def test_reminder_view(self):
        """Test the download_view function."""
        data = self.correct_user_data
        url = '/reminder'

        # Test OK
        guid = add_user(**data)
        if guid is not None:
            email = data['email']
            try:
                result = self.client.post(
                    url, data=dict(email=email), follow_redirects=True)
                self.assertTrue('Success' in result.data)
            except Exception, e:
                LOGGER.exception('Basic front page load failed.')
                raise e

        # Test Error
        try:
            result = self.client.post(
                url,
                data=dict(
                    email='notok@email.com'),
                follow_redirects=True)
            self.assertTrue('Error' in result.data)
        except Exception, e:
            LOGGER.exception('Basic front page load failed.')
            raise e
