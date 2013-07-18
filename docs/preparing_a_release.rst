Steps for Preparing a Release
=============================

1. Increment the version number in ``__init__.py``.
2. Update the release notes in ``docs/release_notes.rst``.
3. Update the version in ``docs/conf.py``.
4. Ensure the release notes in the documentation have the current date
   as the release date.
5. Create a git tag (format ``X.Y.Z``).
6. Run ``tox``.
7. ``git push``
8. ``python setup.py sdist upload``
