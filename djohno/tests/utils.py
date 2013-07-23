from contextlib import contextmanager
from django.contrib.auth.models import User
from django.test import TestCase


@contextmanager
def login_superuser(client):
    client.login(username='admin', password='password')
    yield
    client.logout()


class DjohnoBaseViewTests(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin',
                                      'foo@example.com',
                                      'password')
