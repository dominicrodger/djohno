from django.core import mail
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
import socket
from mock import Mock, patch
from smtplib import SMTPConnectError
from tests.utils import DjohnoBaseViewTests


class DjohnoMailViewTests(DjohnoBaseViewTests):
    def test_djohno_email_frame_with_login(self):
        """
        Tests to ensure loading the djohno framed email test view is
        successful, and renders a few specific strings.
        """
        url = reverse('djohno_frame_email')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Djohno: Email Check')
        self.assertContains(response,
                            'src="%s"' % reverse('djohno_email'))

    @override_settings(DEFAULT_FROM_EMAIL='Foobar <foo@bar.com>')
    def test_mail_view_complex_from_address(self):
        """
        Ensure the mail view correctly sends emails, and sends the
        expected text (we have a "pretty" from address).
        """
        url = reverse('djohno_email')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djohno/email_sent.html')
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

    @override_settings(DEFAULT_FROM_EMAIL='Foobar <foo@bar.com>')
    def test_idempotent_mail_view_complex_from_address(self):
        """
        Ensure the idempotent mail view correctly parses emails.
        """
        url = reverse('djohno_email')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djohno/email.html')
        self.assertEqual(len(mail.outbox), 0)
        self.assertContains(response, "foo@example.com")
        self.assertContains(response, "Foobar &lt;foo@bar.com&gt;")

    @override_settings(DEFAULT_FROM_EMAIL='simple@bar.com')
    def test_mail_view_simple_from_address(self):
        """
        Ensure the mail view correctly sends emails, and sends the
        expected text (we don't have a "pretty" from address, so it
        should tell us about that).
        """
        url = reverse('djohno_email')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djohno/email_sent.html')
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
        url = reverse('djohno_email')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'djohno/bad_email.html')
        self.assertTemplateUsed(response,
                                'djohno/_bad_email_invalid.html')
        self.assertEqual(len(mail.outbox), 0)
        self.assertContains(response, "notanemail")

    @override_settings(DEFAULT_FROM_EMAIL='webmaster@localhost')
    def test_mail_view_default_from_address(self):
        """
        Ensure the mail view correctly detects the DEFAULT_FROM_EMAIL
        settings not being overriden.
        """
        url = reverse('djohno_email')
        response = self.client.post(url)
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

        url = reverse('djohno_email')
        with patch('djohno.views.send_mail',
                   Mock(side_effect=fake_send_mail)):
            response = self.client.post(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'djohno/email_sent.html')
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

        url = reverse('djohno_email')
        with patch('djohno.views.send_mail',
                   Mock(side_effect=fake_send_mail)):
            response = self.client.post(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'djohno/email_sent.html')
            self.assertEqual(len(mail.outbox), 0)
            self.assertContains(response, "failed to send")
            self.assertContains(response,
                                "[Errno 1337] Sockets are too awesome")
