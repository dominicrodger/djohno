from django.conf import settings
from django.core.validators import validate_email
from email.utils import parseaddr
from pkgtools.pypi import PyPIJson
import sys

if sys.version_info >= (3,):
    from urllib.error import HTTPError, URLError
    import urllib.request as urllib2
else:
    from urllib2 import HTTPError, URLError
    import urllib2


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

        latest_version = get_pypi_version(app)

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
