# flake8: noqa

# The "no cover" lines below are to avoid noise in the coverage
# reports - two of the below lines will always be skipped (depending
# on whether you're running Python 2.x or Python 3.x).

import sys


if sys.version_info >= (3,):
    from urllib.error import HTTPError, URLError  # pragma: no cover
    import urllib.request as urllib2  # pragma: no cover
else:
    from urllib2 import HTTPError, URLError  # pragma: no cover
    import urllib2  # pragma: no cover
