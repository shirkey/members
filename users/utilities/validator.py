# coding=utf-8
"""Form Validator Function."""

from validate_email import validate_email


def is_required_valid(req_input):
    """Validate input that required.

    :param req_input: input that neeeds to be validated
    :type req_input: str
    """
    result = False

    if isinstance(req_input, basestring):
        if len(str(req_input).strip()) != 0:
            result = True
    if isinstance(req_input, (int, long, float, complex)):
        if req_input != 0:
            result = True
    return result



def is_email_address_valid(email):
    """Validate the email address.

    :param email: email input
    :type email: str
    This function uses library from: https://pypi.python
    .org/pypi/validate_email
    It can check if the host has SMTP Server and the email
    does exist. Due to issue here: https://github
    .com/SyrusAkbary/validate_email/issues/4 and sometimes it takes long time
    to  check SMTP Server, this feature is not used.
    """
    is_valid_email = validate_email(email)
    return is_valid_email


def is_boolean(param_input):
    """Check if param_input string is boolean 'type'.

    :param param_input: input that need to be checked
    :type param_input: str
    """
    if param_input.lower() not in ['true', 'false']:
        return False
    return True


def validate_user_data(data):
    REQUIRED_USER_FIELDS = ['name', 'email', 'latitude', 'longitude']

    message = dict()

    # Validate data

    for field in REQUIRED_USER_FIELDS:
        if not is_required_valid(data[field]):
            message[field] = '%s is a required field' % field
    if not is_email_address_valid(data['email']):
        message['email'] = 'Email address is not valid'
    if not data['email_updates']:
        message['email_updates'] = 'Notification must be checked'

    return message
