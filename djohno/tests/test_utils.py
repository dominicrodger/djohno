from django.core.exceptions import ValidationError
from django.test import TestCase
from djohno.utils import is_pretty_from_address


class DjohnoUtilTest(TestCase):
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
