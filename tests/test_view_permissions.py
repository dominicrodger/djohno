from django.core.urlresolvers import reverse
from django.test import TestCase


class DjohnoViewPermissionTests(TestCase):
    def test_djohno_frame_403s_without_login(self):
        """
        Tests to ensure loading the root djohno view without
        authenticating results in a 403.
        """
        url = reverse('djohno_frame')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_djohno_index_403s_without_login(self):
        """
        Tests to ensure loading the framed djohno view without
        authenticating results in a 403.
        """
        url = reverse('djohno_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_djohno_403_403s_without_login(self):
        """
        Tests to ensure loading the framed djohno 403 test view
        without authenticating results in a 403.
        """
        url = reverse('djohno_403')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_djohno_404_403s_without_login(self):
        """
        Tests to ensure loading the framed djohno 404 test view
        without authenticating results in a 403.
        """
        url = reverse('djohno_404')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_djohno_500_403s_without_login(self):
        """
        Tests to ensure loading the framed djohno 500 test view
        without authenticating results in a 403.
        """
        url = reverse('djohno_500')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_djohno_idempotent_mail_403s_without_login(self):
        """
        Tests to ensure loading the framed djohno email test view
        without authenticating results in a 403.
        """
        url = reverse('djohno_email')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_djohno_mail_send_403s_without_login(self):
        """
        Tests to ensure loading the framed djohno email sending test view
        without authenticating results in a 403.
        """
        url = reverse('djohno_email')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
