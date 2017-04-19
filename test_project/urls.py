from django.conf.urls import url
from django.contrib import admin

from ydcommon.views import qunit_view

admin.autodiscover()


urlpatterns = [
   url(r"^js-tests/(?P<path>.*)", qunit_view, name='qunit'),
]
