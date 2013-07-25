from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from djohno.six import (
    HTTPError,
    URLError,
    urllib2
)
from email.utils import parseaddr
from pkgtools.pypi import PyPIJson
import sys


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

        latest_version = get_pypi_version(app.__name__)

        versions[name] = {}
        versions[name]['installed'] = version
        versions[name]['latest'] = latest_version

        if latest_version is None:
            status = 'unknown'
        elif latest_version == version:
            status = 'fresh'
        else:
            status = 'stale'

        versions[name]['status'] = status

    return versions


def _patched_request(url, timeout=None):
    r = urllib2.Request(url)
    return urllib2.urlopen(r, timeout=timeout).read().decode("utf-8")


def get_pypi_version(app):
    try:
        api = PyPIJson(app)
        api.retrieve(req_func=_patched_request)
        return api.version
    except HTTPError:
        # Probably got a 404
        return None
    except URLError:
        # Probably not connected to the internet
        return None
