from django.contrib import admin
try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

admin.autodiscover()


urlpatterns = patterns('',
                       url(r"^js-tests/(?P<path>.*)",
                           'ydcommon.views.qunit_view',
                           name='qunit'),
                       )
