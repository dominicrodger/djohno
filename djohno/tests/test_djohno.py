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

    def test_djohno_index_403s_without_login(self):
        url = reverse('djohno_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertTemplateNotUsed(response, 'djohno/_djohno_dose.html')

    def test_djohno_403_403s_without_login(self):
        url = reverse('djohno_403')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertTemplateNotUsed(response, 'djohno/_djohno_dose.html')

    def test_djohno_404_403s_without_login(self):
        url = reverse('djohno_404')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertTemplateNotUsed(response, 'djohno/_djohno_dose.html')

    def test_djohno_500_403s_without_login(self):
        url = reverse('djohno_500')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertTemplateNotUsed(response, 'djohno/_djohno_dose.html')

    def test_djohno_mail_403s_without_login(self):
        url = reverse('djohno_email')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        self.assertTemplateNotUsed(response, 'djohno/_djohno_dose.html')

    def test_djohno_index_with_login(self):
        with login_superuser(self.client):
            url = reverse('djohno_index')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'djohno/_djohno_dose.html')

    def test_djohno_403_with_login(self):
        with login_superuser(self.client):
            url = reverse('djohno_403')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)
            self.assertTemplateUsed(response, '403.html')
            self.assertTemplateUsed(response, 'djohno/_djohno_dose.html')

    def test_djohno_404_with_login(self):
        with login_superuser(self.client):
            url = reverse('djohno_404')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)
            self.assertTemplateUsed(response, '404.html')
            self.assertTemplateUsed(response, 'djohno/_djohno_dose.html')

    def test_djohno_500_with_login(self):
        with login_superuser(self.client):
            url = reverse('djohno_500')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 500)
            self.assertTemplateUsed(response, '500.html')
            self.assertTemplateUsed(response, 'djohno/_djohno_dose.html')

    def test_mail_view(self):
        with login_superuser(self.client):
            url = reverse('djohno_email')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'djohno/email.html')
            self.assertTemplateUsed(response, 'djohno/_djohno_dose.html')
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
                self.assertTemplateUsed(response, 'djohno/_djohno_dose.html')
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
                self.assertTemplateUsed(response, 'djohno/_djohno_dose.html')
                self.assertContains(response, "failed to send")
                self.assertContains(response,
                                    "[Errno 1337] Sockets are too awesome")

    def test_redirects_in_middleware_work(self):
        response = self.client.get('/403')
        self.assertEqual(response.status_code, 301)

    def test_200_with_login_does_not_show_djohno(self):
        with login_superuser(self.client):
            url = reverse('regular_200')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateNotUsed(response, 'djohno/_djohno_dose.html')
            self.assertContains(response, '☃')

    def test_regular_403_with_login_does_not_show_djohno(self):
        with login_superuser(self.client):
            url = reverse('regular_403')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)
            self.assertTemplateUsed(response, '403.html')
            self.assertTemplateNotUsed(response, 'djohno/_djohno_dose.html')

    def test_regular_404_with_login_does_not_show_djohno(self):
        with login_superuser(self.client):
            url = reverse('regular_404')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)
            self.assertTemplateUsed(response, '404.html')
            self.assertTemplateNotUsed(response, 'djohno/_djohno_dose.html')

    def test_regular_500_with_login_does_not_show_djohno(self):
        with login_superuser(self.client):
            url = reverse('regular_500')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 500)
            self.assertTemplateUsed(response, '500.html')
            self.assertTemplateNotUsed(response, 'djohno/_djohno_dose.html')
