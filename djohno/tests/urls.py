from django.conf.urls import patterns, include, url
from django.http import HttpResponse
from django.views.decorators.gzip import gzip_page
from django.views.defaults import (
    permission_denied,
    page_not_found,
    server_error
)


@gzip_page
def simple_view(request):
    return HttpResponse(
        'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed '
        'do eiusmod tempor incididunt ut labore et dolore magna '
        'aliqua. Ut enim ad minim veniam, quis nostrud exercitation '
        'ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis '
        'aute irure dolor in reprehenderit in voluptate velit esse '
        'cillum dolore eu fugiat nulla pariatur. Excepteur sint '
        'occaecat cupidatat non proident, sunt in culpa qui officia '
        'deserunt mollit anim id est laborum.</body>'
    )


urlpatterns = patterns(
    '',
    url(r'^200/$', simple_view, name='regular_200'),
    url(r'^403/$', permission_denied, name='regular_403'),
    url(r'^404/$', page_not_found, name='regular_404'),
    url(r'^500/$', server_error, name='regular_500'),
    url(r'^djohno/', include('djohno.urls')),
)
