******
djohno
******

djohno is a tiny app for checking over your error pages, and email
integration - to stop me doing evil things post-production to ensure
I've set up Sentry and my error pages by randomly breaking parts of my
site by editing code live.

Documentation is available at https://djohno.readthedocs.org.

Tests are run on Travis with every push - see
https://travis-ci.org/dominicrodger/djohno.

Release Notes
=============

0.1.3 (17th July 2013)
----------------------

* Change the 500 view to just raise an exception
  ``djohno.views.DjohnoTestException``, so that we actually activate
  the error logging stuff correctly.

0.1.2 (15th July 2013)
----------------------

* Test re-organising (separated view tests and utility tests), added
  test descriptions.
* Better styles for buttons (based on Flat UI, from
  http://designmodo.github.io/Flat-UI/).
* Added a "versions" view to see versions of apps in
  ``INSTALLED_APPS`` (similar to, and based on, the versions panel in
  Django Debug Toolbar).

0.1.1 (29th June 2013)
----------------------

* Fix the email address the test email is sent from, add checking that
  it's a valid email address, and encourage users to set
  `DEFAULT_FROM_EMAIL` to a friendly address (`Your Name
  <you@yourcompany.com>`);
* Ensure setup.py has a short and a long description;
* Improved documentation.

0.1.0 (27th June 2013)
----------------------

* Initial release
