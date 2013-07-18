from django.conf import settings
from django.core.validators import validate_email
from email.utils import parseaddr
import sys


def is_pretty_from_address(input):
    name, email = parseaddr(input)
    validate_email(email)

    if name:
        return True
    else:
        return False


def _get_installed_version_from_app(app):
    if hasattr(app, 'get_version'):
        if callable(app.get_version):
            return app.get_version()
        return app.get_version

    if hasattr(app, 'VERSION'):
        return app.VERSION

    if hasattr(app, '__version__'):
        return app.__version__

    return None


def get_app_versions():
    versions = {}

    for app in list(settings.INSTALLED_APPS) + ['django']:
        __import__(app)
        app = sys.modules[app]

        version = _get_installed_version_from_app(app)

        if version is None:
            continue

        if isinstance(version, (list, tuple)):
            version = '.'.join(str(o) for o in version)

        name = app.__name__.split('.')[-1].replace('_', ' ').capitalize()

        versions[name] = {}
        versions[name]['installed'] = version

    return versions
