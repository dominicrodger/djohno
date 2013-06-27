from django.conf.urls import (
    handler403,
    handler404,
    handler500
)
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.utils.importlib import import_module
from django.views.generic import View
import socket
from smtplib import SMTPException


def _imported_symbol(import_path):
    """Resolve a dotted path into a symbol, and return that.

    For example...

    >>> _imported_symbol('django.db.models.Model')
    <class 'django.db.models.base.Model'>

    Raise ImportError if there's no such module, AttributeError if no
    such symbol.

    """
    module_name, symbol_name = import_path.rsplit('.', 1)
    module = import_module(module_name)
    return getattr(module, symbol_name)


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


class IndexView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return render(request, 'djohno/index.html')
index_view = IndexView.as_view()


class BaseExceptionView(View):
    response_func = None

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return _imported_symbol(self.response_func)(request)


class Test403View(BaseExceptionView):
    response_func = handler403
test_403 = Test403View.as_view()


class Test404View(BaseExceptionView):
    response_func = handler404
test_404 = Test404View.as_view()


class Test500View(BaseExceptionView):
    response_func = handler500
test_500 = Test500View.as_view()


class TestEmailView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied

        error = None

        try:
            send_mail('djohno email test',
                      'Here is the message.',
                      'from@example.com',
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
                       'sent_successfully': sent_successfully,
                       'error': error})
test_email = TestEmailView.as_view()
