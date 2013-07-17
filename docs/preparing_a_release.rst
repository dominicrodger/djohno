Steps for Preparing a Release
=============================

1. Increment the version number in ``__init__.py``
2. Update the release notes in ``README.rst`` and
   ``docs/release_notes.rst``
3. Create a git tag (format ``X.Y.Z``)
4. Run ``tox``
5. ``git push``
6. ``python setup.py sdist upload``
