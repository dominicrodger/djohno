from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from email.utils import parseaddr


def is_pretty_from_address(input):
    name, email = parseaddr(input)

    if email == 'webmaster@localhost':
        # This is the default setting for DEFAULT_FROM_EMAIL, so if
        # this is the email we've got, you should probably override
        # DEFAULT_FROM_EMAIL in your settings file.
        raise ValidationError("Enter a valid value.")

    validate_email(email)

    if name:
        return True
    else:
        return False
