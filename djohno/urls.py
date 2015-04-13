from django.conf.urls import patterns, url

from .views import (
    frame_view,
    frame_403_view,
    frame_404_view,
    frame_500_view,
    frame_email_view,
    index_view,
    test_403,
    test_404,
    test_500,
    test_email
)

urlpatterns = patterns(
    '',
    url(r'^$', frame_view, name='djohno_frame'),
    url(r'^403/$', frame_403_view, name='djohno_frame_403'),
    url(r'^404/$', frame_404_view, name='djohno_frame_404'),
    url(r'^500/$', frame_500_view, name='djohno_frame_500'),
    url(r'^email/$', frame_email_view, name='djohno_frame_email'),
    url(r'^framed/index/$', index_view, name='djohno_index'),
    url(r'^framed/403/$', test_403, name='djohno_403'),
    url(r'^framed/404/$', test_404, name='djohno_404'),
    url(r'^framed/500/$', test_500, name='djohno_500'),
    url(r'^framed/email/$', test_email, name='djohno_email'),
)
