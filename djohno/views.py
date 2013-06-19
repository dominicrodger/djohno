from django.conf.urls import (
    handler403,
    handler404,
    handler500
)
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.utils.importlib import import_module
from django.views.generic import View


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
    pass
test_email = TestEmailView.as_view()
