Release Notes
*************

.. contents:: Table of Contents
   :local:

0.1.5 (Release date TBC)
========================

* Added images to documentation and README to show what djohno looks
  like.
* Make layout responsive.
* Make mail sending optional (and require a POST).

0.1.4 (19th July 2013)
======================

* Also include ``sys.path`` in the versions page.
* Add margin to the table of app versions.
* Added a favicon for the djohno views.
* Added a convenient ``handler500`` method which includes
  ``STATIC_URL``, and include information on how to configure your
  project to use it in the default ``500.html`` template.
* Attempt to identify what the latest version number for apps is in
  the versions page, and highlight apps that are out of date.

0.1.3 (17th July 2013)
======================

* Change the 500 view to just raise an exception
  ``djohno.views.DjohnoTestException``, so that we actually activate
  the error logging stuff correctly.

0.1.2 (15th July 2013)
======================

* Test re-organising (separated view tests and utility tests), added
  test descriptions.
* Better styles for buttons (based on Flat UI, from
  http://designmodo.github.io/Flat-UI/).
* Added a "versions" view to see versions of apps in
  ``INSTALLED_APPS`` (similar to, and based on, the versions panel in
  Django Debug Toolbar).

0.1.1 (29th June 2013)
======================

* Fix the email address the test email is sent from, add checking that
  it's a valid email address, and encourage users to set
  `DEFAULT_FROM_EMAIL` to a friendly address (`Your Name
  <you@yourcompany.com>`);
* Ensure setup.py has a short and a long description;
* Improved documentation.

0.1.0 (27th June 2013)
======================

* Initial release
