Steps for Preparing a Release
=============================

1. Increment the version number in ``__init__.py``
2. Update the release notes in ``README.rst`` and
   ``docs/release_notes.rst``
3. Update the version in ``docs/conf.py``
4. Create a git tag (format ``X.Y.Z``)
5. Run ``tox``
6. ``git push``
7. ``python setup.py sdist upload``
