from django.conf.urls import patterns, include, url
from djohno.views import server_error


urlpatterns = patterns(
    '',
    url(r'^djohno/', include('djohno.urls')),
    url(r'^500/', server_error, name='server_error_handler'),
)
