from django.core.exceptions import ValidationError
from django.test import TestCase
import djohno
from djohno.six import URLError
from djohno.utils import (
    is_pretty_from_address,
    get_app_versions,
    get_pypi_version
)
import httpretty
from httpretty import httprettified
from mock import Mock, patch


class DjohnoUtilTests(TestCase):
    def test_is_pretty_from_address_fails_on_bare_address(self):
        """
        Ensure normal email addresses aren't parsed as being "pretty".
        """
        self.assertFalse(is_pretty_from_address('foo@bar.com'))

    def test_is_pretty_from_succeeds_on_pretty_address(self):
        """
        Ensure pretty addresses (e.g. Foo <foo@bar.com>) are parsed as
        being "pretty".
        """
        self.assertTrue(is_pretty_from_address('Foo <foo@bar.com>'))

    def test_is_pretty_from_raises_validation_error_on_bad_input(self):
        """
        Ensure invalid email addresses (e.g. "hello") raise
        ValidationError if given invalid inputs.
        """
        with self.assertRaises(ValidationError):
            self.assertTrue(is_pretty_from_address('hello'))

    def test_get_installed_app_versions(self):
        """
        Ensure we can correctly get the version of a few simple apps
        (Baz and Moo are bundled in djohno.test, and set up in
        test_settings.py).
        """
        def fake_get_pypi(app):
            if app == 'djohno':
                return djohno.__version__

            if app == 'djohno.tests.baz':
                return '4.2'
            return None

        with patch('djohno.utils.get_pypi_version',
                   Mock(side_effect=fake_get_pypi)):
            versions = get_app_versions()
            self.assertEqual(versions['Djohno']['installed'],
                             djohno.__version__)
            self.assertEqual(versions['Djohno']['latest'], djohno.__version__)
            self.assertEqual(versions['Baz']['installed'], '0.4.2')
            self.assertEqual(versions['Baz']['latest'], '4.2')
            self.assertEqual(versions['Moo']['installed'], '0.42')
            self.assertEqual(versions['Moo']['latest'], None)

    @httprettified
    def test_get_pypi_version_bad_package(self):
        """
        Ensure we fail as expected to get the version of a
        non-existent package from PyPI.
        """
        httpretty.register_uri(
            httpretty.GET,
            "http://pypi.python.org/simple/Django",
            status=404)

        self.assertEqual(get_pypi_version('Django'), None)

    def test_get_pypi_version_timeout(self):
        """
        Ensure we fail as expected to get the version of a
        package when PyPI is being unresponsive.
        """
        def fake_real_name(pkg):
            raise URLError("Request timed out")

        with patch('pkgtools.pypi.real_name',
                   Mock(side_effect=fake_real_name)):
            self.assertEqual(get_pypi_version('Django'), None)

    @httprettified
    def test_get_pypi_version_good_package(self):
        """
        Ensure we can get the latest version of a package from PyPI.
        """
        httpretty.register_uri(
            httpretty.GET,
            "http://pypi.python.org/simple/djohno",
            status=301,
            location="http://pypi.python.org/simple/djohno/")

        httpretty.register_uri(
            httpretty.GET,
            "http://pypi.python.org/simple/djohno/")

        httpretty.register_uri(
            httpretty.GET,
            "http://pypi.python.org/pypi/djohno/json",
            body="""
            {
              "info": {
                "package_url": "http://pypi.python.org/pypi/djohno",
                "author": "Dominic Rodger",
                "version": "0.1.3"
              }
            }
            """)

        self.assertEqual(get_pypi_version('djohno'), "0.1.3")
