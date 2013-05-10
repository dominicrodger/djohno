from django.conf.urls import patterns, url

from .views import (
    index_view,
    test_400,
    test_403,
    test_404,
    test_500,
    test_email
)

urlpatterns = patterns(
    '',
    url(r'^$', index_view),
    url(r'^400/$', test_400),
    url(r'^403/$', test_403),
    url(r'^404/$', test_404),
    url(r'^500/$', test_500),
    url(r'^email/$', test_email),
)
