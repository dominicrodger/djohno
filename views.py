from django.views.generic import TemplateView, View
from django.http.response import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError
)


class IndexView(TemplateView):
    template_name = 'djohno/index.html'
index_view = IndexView.as_view()


class BaseExceptionView(View):
    response_class = None

    def get(self, request, *args, **kwargs):
        if self.response_class is None:
            pass
        return self.response_class()


class Test400View(BaseExceptionView):
    response_class = HttpResponseBadRequest
test_400 = Test400View.as_view()


class Test403View(BaseExceptionView):
    response_class = HttpResponseForbidden
test_403 = Test403View.as_view()


class Test404View(BaseExceptionView):
    response_class = HttpResponseNotFound
test_404 = Test404View.as_view()


class Test500View(BaseExceptionView):
    response_class = HttpResponseServerError
test_500 = Test500View.as_view()


class TestEmailView(View):
    pass
test_email = TestEmailView.as_view()
