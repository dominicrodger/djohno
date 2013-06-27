from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url(r'^djohno/', include('djohno.urls')),
)
