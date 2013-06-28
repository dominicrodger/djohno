from django.core.validators import validate_email
from email.utils import parseaddr


def is_pretty_from_address(input):
    name, email = parseaddr(input)
    validate_email(email)

    if name:
        return True
    else:
        return False
