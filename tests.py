from django.test import TestCase


class SimpleTest(TestCase):
    def test_index(self):
        response = self.client.get('/djohno/')
        self.assertEqual(response.status_code, 200)

    def test_400(self):
        response = self.client.get('/djohno/400/')
        self.assertEqual(response.status_code, 400)

    def test_403(self):
        response = self.client.get('/djohno/403/')
        self.assertEqual(response.status_code, 403)

    def test_404(self):
        response = self.client.get('/djohno/404/')
        self.assertEqual(response.status_code, 404)

    def test_500(self):
        response = self.client.get('/djohno/500/')
        self.assertEqual(response.status_code, 500)
