from django.contrib.auth.models import User
from django.test import TestCase


class DjohnoBaseViewTests(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin',
                                      'foo@example.com',
                                      'password')
        self.client.login(username='admin', password='password')

    def tearDown(self):
        self.client.logout()
