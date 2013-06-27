from django.conf.urls import patterns, url

from .views import (
    frame_view,
    index_view,
    test_403,
    test_404,
    test_500,
    test_email
)

urlpatterns = patterns(
    '',
    url(r'^$', frame_view, name='djohno_frame'),
    url(r'^index/$', index_view, name='djohno_index'),
    url(r'^403/$', test_403, name='djohno_403'),
    url(r'^404/$', test_404, name='djohno_404'),
    url(r'^500/$', test_500, name='djohno_500'),
    url(r'^email/$', test_email, name='djohno_email'),
)
