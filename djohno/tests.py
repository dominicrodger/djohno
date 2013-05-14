from django.test import TestCase
from django.core.urlresolvers import reverse


class SimpleTest(TestCase):
    def test_index(self):
        url = reverse('djohno_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_400(self):
        url = reverse('djohno_400')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_403(self):
        url = reverse('djohno_403')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_404(self):
        url = reverse('djohno_404')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_405(self):
        url = reverse('djohno_405')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
        headers = dict(response.items())
        self.assertEqual(headers['Allow'], 'GET')

    def test_500(self):
        url = reverse('djohno_500')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 500)
