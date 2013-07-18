from django.conf import settings
from django.core.exceptions import (
    PermissionDenied,
    ValidationError
)
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import View, TemplateView
from djohno.utils import (
    is_pretty_from_address,
    get_app_versions
)
import socket
from smtplib import SMTPException
import sys


class BaseFrameView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return render(request, 'djohno/frame.html',
                      {'frame_url': self.frame_url,
                       'title': self.title})


class FrameView(BaseFrameView):
    title = 'Djohno: Home'
    frame_url = reverse_lazy('djohno_index')
frame_view = FrameView.as_view()


class Frame403View(BaseFrameView):
    title = 'Djohno: 403 Check'
    frame_url = reverse_lazy('djohno_403')
frame_403_view = Frame403View.as_view()


class Frame404View(BaseFrameView):
    title = 'Djohno: 404 Check'
    frame_url = reverse_lazy('djohno_404')
frame_404_view = Frame404View.as_view()


class Frame500View(BaseFrameView):
    title = 'Djohno: 500 Check'
    frame_url = reverse_lazy('djohno_500')
frame_500_view = Frame500View.as_view()


class FrameEmailView(BaseFrameView):
    title = 'Djohno: Email Check'
    frame_url = reverse_lazy('djohno_email')
frame_email_view = FrameEmailView.as_view()


class FrameVersionsView(BaseFrameView):
    title = 'Djohno: Versions'
    frame_url = reverse_lazy('djohno_versions')
frame_versions_view = FrameVersionsView.as_view()


class IndexView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return render(request, 'djohno/index.html')
index_view = IndexView.as_view()


class BaseExceptionView(View):
    exception = None

    def _get_exception(self):
        raise self.exception('Intentionally raised exception to test error '
                             'handling.')

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        self._get_exception()


class Test403View(BaseExceptionView):
    exception = PermissionDenied
test_403 = Test403View.as_view()


class Test404View(BaseExceptionView):
    exception = Http404
test_404 = Test404View.as_view()


class DjohnoTestException(Exception):
    pass


class Test500View(BaseExceptionView):
    exception = DjohnoTestException
test_500 = Test500View.as_view()


class TestEmailView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied

        from_address = settings.DEFAULT_FROM_EMAIL
        try:
            is_pretty = is_pretty_from_address(from_address)
        except ValidationError as e:
            return render(request, 'djohno/bad_email.html',
                          {'from_email': from_address})

        message = render_to_string('djohno/email_body.txt',
                                   {'pretty_from': is_pretty})

        error = None

        try:
            send_mail('djohno email test',
                      message,
                      from_address,
                      [request.user.email, ],
                      fail_silently=False)
            sent_successfully = True
        except SMTPException as e:
            sent_successfully = False
            error = e
        except socket.error as e:
            sent_successfully = False
            error = e

        return render(request, 'djohno/email.html',
                      {'email': request.user.email,
                       'from_email': from_address,
                       'sent_successfully': sent_successfully,
                       'error': error})
test_email = TestEmailView.as_view()


class VersionsView(TemplateView):
    template_name = 'djohno/versions.html'

    def get_context_data(self, **kwargs):
        return {'sys': '%d.%d.%d' % sys.version_info[:3],
                'versions': get_app_versions(),
                'path': sys.path}
versions = VersionsView.as_view()
