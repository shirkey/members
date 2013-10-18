# coding=utf-8
"""Tests for the application web urls.
:copyright: (c) 2013 by Tim Sutton
:license: GPLv3, see LICENSE for more details.
"""
import os

from users.views import APP
from users.test.logged_unittest import LoggedTestCase
from users import LOGGER
from users.utilities.db_handler import get_conn


class AppTestCase(LoggedTestCase):
    """Test the application."""
    def setUp(self):
        """Constructor."""
        self.db_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            os.pardir,
            'test_users.db'))
        APP.config['DATABASE'] = self.db_path
        APP.config['TESTING'] = True
        self.app = APP.test_client()

    def tearDown(self):
        """Destructor."""
        pass

    def test_home(self):
        """Test the home page works."""
        try:
            return self.app.post('/', data=dict(), follow_redirects=True)
        except Exception, e:
            LOGGER.exception('Basic front page load failed.')
            raise e

    def test_users_view(self):
        """Test the users json response works."""
        conn = get_conn(self.db_path)
        sql = ('INSERT INTO user VALUES("Akbar", "akbargum@gmail.com", '
               '"true", "true", "2013-10-16", "75.672197", "-42.187500");')
        conn.execute(sql)
        conn.commit()
        conn.close()

        try:
            result = self.app.get(
                '/users.json', data=dict(), follow_redirects=True)
            #pylint: ignore-msg=E1103
            self.assertTrue('Akbar' in result.data)
        except Exception, e:
            LOGGER.exception('Basic front page load failed.')
            raise e

    def test_add_user_view(self):
        """Test the user added json response works."""
        try:
            result = self.app.post(
                '/add_user', data=dict(
                    name='Akbar',
                    email='akbargumbira@gmail.com',
                    role='true',
                    notification='true',
                    latitude='12',
                    longitude='31'
                ), follow_redirects=True)
            #pylint: ignore-msg=E1103
            self.assertTrue('Akbar' in result.data)
        except Exception, e:
            LOGGER.exception('Page load failed.')
            raise e

        try:
            result = self.app.post(
                '/add_user', data=dict(
                    name='Akbar',
                    email='akbargumbiragmail.com',
                    role='true',
                    notification='true',
                    latitude='12',
                    longitude='31'
                ), follow_redirects=True)
            #pylint: ignore-msg=E1103
            self.assertTrue('Error' in result.data)
        except Exception, e:
            LOGGER.exception('Page load failed.')
            raise e
