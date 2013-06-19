from django.conf.urls import patterns, include, url
from django.views.defaults import (
    permission_denied,
    page_not_found,
    server_error
)

urlpatterns = patterns(
    '',
    url(r'^403/$', permission_denied, name='regular_403'),
    url(r'^404/$', page_not_found, name='regular_404'),
    url(r'^500/$', server_error, name='regular_500'),
    url(r'^djohno/', include('djohno.urls')),
)
