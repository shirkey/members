# coding=utf-8
"""Helper methods."""
from threading import Thread

from flask import jsonify
from werkzeug.exceptions import HTTPException
from flask_mail import Message
from users import mail, APP


def make_json_error(ex):
    """Return errors as json.

    See http://flask.pocoo.org/snippets/83/

    :param ex: An exception.
    :return:  HttpResponse
    """
    response = jsonify(message=str(ex))
    response.status_code = (
        ex.code
        if isinstance(ex, HTTPException)
        else 500)
    return response


def send_mail(sender, recipients, subject, text_body, html_body):
    """To send a single email from sender to receiver synchronously

    :param sender: Sender of the email.
    :type sender: str
    :param recipients: Recipients email address.
    :type recipients: list
    :param subject: Subject of the email.
    :type subject: str
    :param text_body: Text of the body.
    :type text_body: str
    :param html_body: HTML of the body.
    :type html_body: str
    """
    # Get mail server configuration
    message = Message(subject=subject, sender=sender, recipients=recipients)
    message.body = text_body
    message.html = html_body
    with APP.app_context():

        mail.send(message)


def send_async_mail(sender, recipients, subject, text_body, html_body):
    """To send email asynchronously

     :param sender: Sender of the email.
    :type sender: str
    :param recipients: Recipients email address.
    :type recipients: list
    :param subject: Subject of the email.
    :type subject: str
    :param text_body: Text of the body.
    :type text_body: str
    :param html_body: HTML of the body.
    :type html_body: str
    :return sender_thread: The thread for sending the email.
    :rtype: Thread
    """
    sender_thread = Thread(
        target=send_mail,
        args=[sender, recipients, subject, text_body, html_body]
    )
    sender_thread.start()
    return sender_thread

def parse_user_data(req):
    USER_FIELDS = ['name', 'email', 'latitude', 'longitude', 'website']
    SOCIAL_ACCOUNT_TYPES = ['twitter']

    data = dict()

    # Parse data
    for val in USER_FIELDS:
        data[val] = str(req.get(val, '')).strip()

    if 'http://' not in req['website']:
        data['website'] = 'http://%s' % req['website']
    data['email_updates'] = True if req['email_updates'].lower() == 'true' else False

    for float_val in ['longitude', 'latitude']:
        try:
            data[float_val] = float(data[float_val])
        except ValueError:
            print "%s must be a number" % float_val

    social_account_data = data['social_account'] = dict()
    for sa in SOCIAL_ACCOUNT_TYPES:
        social_account_data[sa] = str(req.get(sa, '')).strip() or str(req.get('social_account_%s' % sa, '')).strip()

    return data