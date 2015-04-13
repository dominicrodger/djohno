Welcome to djohno's documentation!
==================================

djohno is a reusable Django app for ensuring your error views and
templates work properly. djohno adds views which intentionally trigger
HTTP 403, HTTP 404 and HTTP 500 responses. There are also views for
ensuring your site email facilities are set up correctly.

All djohno views are restricted to users with superuser access.

``djohno`` also adds default ``403.html``, ``404.html`` and
``500.html`` templates, which you should override.

Contents
--------

.. toctree::
   :maxdepth: 2

   installation
   screenshots
   release_notes
   preparing_a_release
