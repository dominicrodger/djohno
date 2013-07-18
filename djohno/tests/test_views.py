from contextlib import contextmanager
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
import djohno
from djohno.views import DjohnoTestException
import socket
from mock import Mock, patch
from smtplib import SMTPConnectError


@contextmanager
def login_superuser(client):
    client.login(username='admin', password='password')
    yield
    client.logout()


class DjohnoViewTests(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin',
                                      'foo@example.com',
                                      'password')

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

    def test_djohno_mail_403s_without_login(self):
        """
        Tests to ensure loading the framed djohno email test view
        without authenticating results in a 403.
        """
        url = reverse('djohno_email')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

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

    def test_djohno_email_frame_with_login(self):
        """
        Tests to ensure loading the djohno framed email test view is
        successful, and renders a few specific strings.
        """
        with login_superuser(self.client):
            url = reverse('djohno_frame_email')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Djohno: Email Check')
            self.assertContains(response,
                                'src="%s"' % reverse('djohno_email'))

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

    @override_settings(DEFAULT_FROM_EMAIL='Foobar <foo@bar.com>')
    def test_mail_view_complex_from_address(self):
        """
        Ensure the mail view correctly sends emails, and sends the
        expected text (we have a "pretty" from address).
        """
        with login_superuser(self.client):
            url = reverse('djohno_email')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'djohno/email.html')
            self.assertEqual(len(mail.outbox), 1)
            sent = mail.outbox[0]
            self.assertEqual(sent.subject, 'djohno email test')
            self.assertTrue(sent.body.find('Congratulations') != -1)
            self.assertEqual(sent.body.find('It\'s probably a good'), -1)
            self.assertEqual(sent.body.find('\n\n\n'), -1)
            self.assertEqual(len(sent.to), 1)
            self.assertEqual(sent.to[0], 'foo@example.com')
            self.assertContains(response, "successfully sent")
            self.assertContains(response, "foo@example.com")
            self.assertContains(response, "Foobar &lt;foo@bar.com&gt;")

    @override_settings(DEFAULT_FROM_EMAIL='simple@bar.com')
    def test_mail_view_simple_from_address(self):
        """
        Ensure the mail view correctly sends emails, and sends the
        expected text (we don't have a "pretty" from address, so it
        should tell us about that).
        """
        with login_superuser(self.client):
            url = reverse('djohno_email')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'djohno/email.html')
            self.assertEqual(len(mail.outbox), 1)
            sent = mail.outbox[0]
            self.assertEqual(sent.subject, 'djohno email test')
            self.assertTrue(sent.body.find('Congratulations') != -1)
            self.assertNotEqual(sent.body.find('It\'s probably a good'), -1)
            self.assertEqual(sent.body.find('\n\n\n'), -1)
            self.assertEqual(len(sent.to), 1)
            self.assertEqual(sent.to[0], 'foo@example.com')
            self.assertContains(response, "successfully sent")
            self.assertContains(response, "foo@example.com")
            self.assertContains(response, "simple@bar.com")

    @override_settings(DEFAULT_FROM_EMAIL='notanemail')
    def test_mail_view_invalid_from_address(self):
        """
        Ensure the mail view correctly detects invalid from emails.
        """
        with login_superuser(self.client):
            url = reverse('djohno_email')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'djohno/bad_email.html')
            self.assertTemplateUsed(response,
                                    'djohno/_bad_email_invalid.html')
            self.assertEqual(len(mail.outbox), 0)
            self.assertContains(response, "no email was sent")
            self.assertContains(response, "notanemail")

    @override_settings(DEFAULT_FROM_EMAIL='webmaster@localhost')
    def test_mail_view_default_from_address(self):
        """
        Ensure the mail view correctly detects the DEFAULT_FROM_EMAIL
        settings not being overriden.
        """
        with login_superuser(self.client):
            url = reverse('djohno_email')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'djohno/bad_email.html')
            self.assertTemplateUsed(response,
                                    'djohno/_bad_email_default.html')
            self.assertEqual(len(mail.outbox), 0)
            self.assertContains(response, "Your Name")
            self.assertContains(response, "you@example.com")

    def test_mail_view_smtp_failure(self):
        """
        Ensure the mail view correctly handles SMTP failures.
        """

        def fake_send_mail(subject, message,
                           from_email, recipient_list,
                           fail_silently=False,
                           auth_user=None, auth_password=None,
                           connection=None):
            raise SMTPConnectError(1337, "SMTP is too awesome")

        with login_superuser(self.client):
            url = reverse('djohno_email')
            with patch('djohno.views.send_mail',
                       Mock(side_effect=fake_send_mail)):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'djohno/email.html')
                self.assertEqual(len(mail.outbox), 0)
                self.assertContains(response, "failed to send")
                self.assertContains(response,
                                    "(1337, &#39;SMTP is too awesome&#39;)")

    def test_mail_view_socket_failure(self):
        """
        Ensure the mail view correctly handles socket failures
        (probably fairly unlikely except in local development
        scenarios, when you are without an internet connection).
        """

        def fake_send_mail(subject, message,
                           from_email, recipient_list,
                           fail_silently=False,
                           auth_user=None, auth_password=None,
                           connection=None):
            raise socket.error(1337, 'Sockets are too awesome')

        with login_superuser(self.client):
            url = reverse('djohno_email')
            with patch('djohno.views.send_mail',
                       Mock(side_effect=fake_send_mail)):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'djohno/email.html')
                self.assertEqual(len(mail.outbox), 0)
                self.assertContains(response, "failed to send")
                self.assertContains(response,
                                    "[Errno 1337] Sockets are too awesome")

    def test_djohno_version_frame_with_login(self):
        """
        Tests to ensure loading the djohno framed app versions view is
        successful, and renders a few specific strings.
        """
        with login_superuser(self.client):
            url = reverse('djohno_frame_versions')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Djohno: Versions')
            self.assertContains(response,
                                'src="%s"' % reverse('djohno_versions'))

    def test_djohno_versions_with_login(self):
        """
        Tests to ensure loading the djohno versions view is
        successful.
        """
        with login_superuser(self.client):
            url = reverse('djohno_versions')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response,
                                '<td>Djohno</td>',
                                html=True)
            self.assertContains(response,
                                '<td>%s</td>' % djohno.__version__,
                                html=True)
            self.assertContains(response,
                                '<td>Django</td>',
                                html=True)
            self.assertContains(response,
                                '<tr class="version">',
                                count=4)

    def test_djohno_server_error_handler(self):
        """
        Tests to ensure our handler500 works correctly.
        """
        url = reverse('server_error_handler')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 500)
        self.assertTrue('STATIC_URL' in response.context)
