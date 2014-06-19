# coding=utf-8
"""This is the main package for the application.
:copyright: (c) 2013 by Tim Sutton
:license: GPLv3, see LICENSE for more details.
"""

import os
import logging

from flask import Flask
from flask_mail import Mail

from users.config import (
    PROJECT_NAME,
    PUBLIC_URL,
    PROJECT_FAVICON_FILE,
    MAIL_CONFIG,
    SQLITE_DB_PATH,
    USER_ICONS)


def add_handler_once(logger, handler):
    """A helper to add a handler to a logger, ensuring there are no duplicates.

    :param logger: The logger instance.
    :type logger: logging.logger

    :param handler: Hander instance to be added. It will not be
        added if an instance of that Handler subclass already exists.
    :type handler: logging.Handler

    :returns: True if the logging handler was added
    :rtype bool: bool
    """
    class_name = handler.__class__.__name__
    for logger_handler in logger.handlers:
        if logger_handler.__class__.__name__ == class_name:
            return False

    logger.addHandler(handler)
    return True


def setup_logger():
    """Set up our logger with sentry support.
    """
    logger = logging.getLogger('user_map')
    logger.setLevel(logging.DEBUG)
    handler_level = logging.DEBUG
    # create formatter that will be added to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    temp_dir = '/tmp'
    # so e.g. jenkins can override log dir.
    if 'USER_MAP_LOGFILE' in os.environ:
        file_name = os.environ['USER_MAP_LOGFILE']
    else:
        file_name = os.path.join(temp_dir, 'user-map.log')
    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(handler_level)
    # create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)

    #Set formatters
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # add the handlers to the logger
    add_handler_once(logger, file_handler)
    add_handler_once(logger, console_handler)

setup_logger()
LOGGER = logging.getLogger('user_map')

APP = Flask(__name__)

# Load configuration
APP.config['PROJECT_NAME'] = PROJECT_NAME
APP.config['PUBLIC_URL'] = PUBLIC_URL
APP.config['PROJECT_FAVICON_FILE'] = PROJECT_FAVICON_FILE
APP.config.update(MAIL_CONFIG)
mail = Mail(APP)
APP.config['DATABASE'] = SQLITE_DB_PATH
APP.config['USER_ICONS'] = USER_ICONS
# Don't import actual view methods themselves - see:
# http://flask.pocoo.org/docs/patterns/packages/#larger-applications
# Also views must be imported AFTER app is created above.
# noinspection PyUnresolvedReferences
import users.views
