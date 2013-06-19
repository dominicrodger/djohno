from contextlib import contextmanager
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


@contextmanager
def login_superuser(client):
    client.login(username='admin', password='password')
    yield
    client.logout()


class SimpleTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin',
                                      'foo@example.com',
                                      'password')

    def test_index_403s_without_login(self):
        url = reverse('djohno_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertTemplateNotUsed(response, 'djohno/_djohno_dose.html')

    def test_403_403s_without_login(self):
        url = reverse('djohno_403')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertTemplateNotUsed(response, 'djohno/_djohno_dose.html')

    def test_404_403s_without_login(self):
        url = reverse('djohno_404')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertTemplateNotUsed(response, 'djohno/_djohno_dose.html')

    def test_500_403s_without_login(self):
        url = reverse('djohno_500')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertTemplateNotUsed(response, 'djohno/_djohno_dose.html')

    def test_index_with_login(self):
        with login_superuser(self.client):
            url = reverse('djohno_index')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'djohno/_djohno_dose.html')

    def test_403_with_login(self):
        with login_superuser(self.client):
            url = reverse('djohno_403')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)
            self.assertTemplateUsed(response, '403.html')
            self.assertTemplateUsed(response, 'djohno/_djohno_dose.html')

    def test_404_with_login(self):
        with login_superuser(self.client):
            url = reverse('djohno_404')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)
            self.assertTemplateUsed(response, '404.html')
            self.assertTemplateUsed(response, 'djohno/_djohno_dose.html')

    def test_500_with_login(self):
        with login_superuser(self.client):
            url = reverse('djohno_500')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 500)
            self.assertTemplateUsed(response, '500.html')
            self.assertTemplateUsed(response, 'djohno/_djohno_dose.html')
