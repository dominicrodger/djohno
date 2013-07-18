from django.core.exceptions import ValidationError
from django.test import TestCase
import djohno
from djohno.utils import (
    is_pretty_from_address,
    get_app_versions
)


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
        versions = get_app_versions()
        self.assertEqual(versions['Djohno']['installed'], djohno.__version__)
        self.assertEqual(versions['Baz']['installed'], '0.4.2')
        self.assertEqual(versions['Moo']['installed'], '0.42')
