from django.contrib import admin
from django.conf.urls import patterns, url

admin.autodiscover()


urlpatterns = patterns('',
                       url(r"^js-tests/(?P<path>.*)",
                           'ydcommon.views.qunit_view'
                           ),
                       )
