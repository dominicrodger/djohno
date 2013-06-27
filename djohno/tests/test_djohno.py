# -*- coding: utf-8 -*-
from contextlib import contextmanager
from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
import socket
from mock import Mock, patch
from smtplib import SMTPConnectError


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

    def test_djohno_frame_403s_without_login(self):
        url = reverse('djohno_frame')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_djohno_index_403s_without_login(self):
        url = reverse('djohno_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_djohno_403_403s_without_login(self):
        url = reverse('djohno_403')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_djohno_404_403s_without_login(self):
        url = reverse('djohno_404')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_djohno_500_403s_without_login(self):
        url = reverse('djohno_500')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_djohno_mail_403s_without_login(self):
        url = reverse('djohno_email')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_djohno_frame_with_login(self):
        with login_superuser(self.client):
            url = reverse('djohno_frame')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Djohno: Home')
            self.assertContains(response,
                                'src="%s"' % reverse('djohno_index'))

    def test_djohno_403_frame_with_login(self):
        with login_superuser(self.client):
            url = reverse('djohno_frame_403')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Djohno: 403 Check')
            self.assertContains(response,
                                'src="%s"' % reverse('djohno_403'))

    def test_djohno_404_frame_with_login(self):
        with login_superuser(self.client):
            url = reverse('djohno_frame_404')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Djohno: 404 Check')
            self.assertContains(response,
                                'src="%s"' % reverse('djohno_404'))

    def test_djohno_500_frame_with_login(self):
        with login_superuser(self.client):
            url = reverse('djohno_frame_500')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Djohno: 500 Check')
            self.assertContains(response,
                                'src="%s"' % reverse('djohno_500'))

    def test_djohno_email_frame_with_login(self):
        with login_superuser(self.client):
            url = reverse('djohno_frame_email')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Djohno: Email Check')
            self.assertContains(response,
                                'src="%s"' % reverse('djohno_email'))

    def test_djohno_index_with_login(self):
        with login_superuser(self.client):
            url = reverse('djohno_index')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_djohno_403_with_login(self):
        with login_superuser(self.client):
            url = reverse('djohno_403')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)
            self.assertTemplateUsed(response, '403.html')

    def test_djohno_404_with_login(self):
        with login_superuser(self.client):
            url = reverse('djohno_404')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)
            self.assertTemplateUsed(response, '404.html')

    def test_djohno_500_with_login(self):
        with login_superuser(self.client):
            url = reverse('djohno_500')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 500)
            self.assertTemplateUsed(response, '500.html')

    def test_mail_view(self):
        with login_superuser(self.client):
            url = reverse('djohno_email')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'djohno/email.html')
            self.assertEqual(len(mail.outbox), 1)
            sent = mail.outbox[0]
            self.assertEqual(sent.subject, 'djohno email test')
            self.assertEqual(len(sent.to), 1)
            self.assertEqual(sent.to[0], 'foo@example.com')
            self.assertContains(response, "successfully sent")
            self.assertContains(response, "foo@example.com")

    def test_mail_view_smtp_failure(self):
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
                self.assertContains(response, "failed to send")
                self.assertContains(response,
                                    "(1337, &#39;SMTP is too awesome&#39;)")

    def test_mail_view_socket_failure(self):
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
                self.assertContains(response, "failed to send")
                self.assertContains(response,
                                    "[Errno 1337] Sockets are too awesome")
