from django.conf.urls import patterns, url

from .views import (
    index_view,
    test_400,
    test_403,
    test_404,
    test_405,
    test_500,
    test_email
)

urlpatterns = patterns(
    '',
    url(r'^$', index_view, name='djohno_index'),
    url(r'^400/$', test_400, name='djohno_400'),
    url(r'^403/$', test_403, name='djohno_403'),
    url(r'^404/$', test_404, name='djohno_404'),
    url(r'^405/$', test_405, name='djohno_405'),
    url(r'^500/$', test_500, name='djohno_500'),
    url(r'^email/$', test_email, name='djohno_email'),
)
