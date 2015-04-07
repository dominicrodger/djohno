Installation
============

djohno is available for install from PyPI::

    pip install djohno

Once it's in your virtualenv, add it to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'djohno',
    )

.. note::

   It's important to make sure ``djohno`` is listed after all other
   apps which have templates you care about, since djohno includes
   some templates that aren't scoped to a ``djohno`` subdirectory
   (namely, ``403.html``, ``404.html``, ``500.html``). You should have
   other apps (or perhaps templates in ``TEMPLATE_DIRS``) which
   provide those templates, so ensure those apps are listed **before**
   ``djohno``. If you're using templates for ``403.html`` et al in
   ``TEMPLATE_DIRS``, make sure
   ``'django.template.loaders.filesystem.Loader'`` is listed before
   ``'django.template.loaders.app_directories.Loader'`` in your
   ``TEMPLATE_DIRS`` setting.

Once you've added ``djohno`` to your ``INSTALLED_APPS``, add djohno to
your ``urls.py``::

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

Supported Python and Django versions
------------------------------------

Currently, djohno supports Django 1.4, 1.5, 1.6 and 1.7. Djohno
follows Django's lead in the versions of Python it supports
(i.e. with Django 1.5 and above, djohno will support Python 3).
