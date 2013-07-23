from django.core.urlresolvers import reverse
from djohno.views import DjohnoTestException
from .utils import (
    login_superuser,
    DjohnoBaseViewTests
)


class DjohnoViewTests(DjohnoBaseViewTests):
    def test_djohno_frame_with_login(self):
        """
        Tests to ensure loading the djohno frame view is successful,
        and renders a few specific strings.
        """
        with login_superuser(self.client):
            url = reverse('djohno_frame')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Djohno: Home')
            self.assertContains(response,
                                'src="%s"' % reverse('djohno_index'))

    def test_djohno_403_frame_with_login(self):
        """
        Tests to ensure loading the djohno framed 403 view is
        successful, and renders a few specific strings.
        """
        with login_superuser(self.client):
            url = reverse('djohno_frame_403')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Djohno: 403 Check')
            self.assertContains(response,
                                'src="%s"' % reverse('djohno_403'))

    def test_djohno_404_frame_with_login(self):
        """
        Tests to ensure loading the djohno framed 404 view is
        successful, and renders a few specific strings.
        """
        with login_superuser(self.client):
            url = reverse('djohno_frame_404')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Djohno: 404 Check')
            self.assertContains(response,
                                'src="%s"' % reverse('djohno_404'))

    def test_djohno_500_frame_with_login(self):
        """
        Tests to ensure loading the djohno framed 500 view is
        successful, and renders a few specific strings.
        """
        with login_superuser(self.client):
            url = reverse('djohno_frame_500')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Djohno: 500 Check')
            self.assertContains(response,
                                'src="%s"' % reverse('djohno_500'))

    def test_djohno_index_with_login(self):
        """
        Tests to ensure loading the djohno index view is successful.
        """
        with login_superuser(self.client):
            url = reverse('djohno_index')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_djohno_403_with_login(self):
        """
        Tests to ensure loading the djohno 403 test view results in a
        403, and uses the expected template (this test may break if
        you've overriden handler403 with a function that doesn't
        render 403.html).
        """
        with login_superuser(self.client):
            url = reverse('djohno_403')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)
            self.assertTemplateUsed(response, '403.html')

    def test_djohno_404_with_login(self):
        """
        Tests to ensure loading the djohno 404 test view results in a
        404, and uses the expected template (this test may break if
        you've overriden handler404 with a function that doesn't
        render 404.html).
        """
        with login_superuser(self.client):
            url = reverse('djohno_404')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)
            self.assertTemplateUsed(response, '404.html')

    def test_djohno_500_with_login(self):
        """
        Tests to ensure loading the djohno 500 test view raises an
        exception.
        """
        with login_superuser(self.client):
            url = reverse('djohno_500')
            with self.assertRaises(DjohnoTestException):
                self.client.get(url)

    def test_djohno_server_error_handler(self):
        """
        Tests to ensure our handler500 works correctly.
        """
        url = reverse('server_error_handler')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 500)
        self.assertTrue('STATIC_URL' in response.context)
