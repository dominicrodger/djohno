Welcome to djohno's documentation!
==================================

djohno is a reusable Django app for ensuring your error views and
templates work properly. djohno adds views which intentionally trigger
HTTP 403, HTTP 404 and HTTP 500 responses. There's also a view for
ensuring your site email facilities are set up correctly.

All djohno views are restricted to users with superuser access.

``djohno`` also adds default ``403.html``, ``404.html`` and
``500.html`` templates, which you should override.

Installation
------------

djohno is available for install from PyPI::

    pip install djohno

Once it's in your virtualenv, add it to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'djohno',
    )

Add djohno to your ``urls.py``::

    urlpatterns = patterns(
        '',
        ...
        url(r'^djohno/', include('djohno.urls')),
    )

Finally, you'll need to deploy djohno's static files, with::

    python manage.py collectstatic

Usage
-----

Once installed, simply visit ``djohno/`` in your browser, and try the
links to the 403, 404, 500 and mail integration pages.
