from django.contrib.staticfiles.storage import StaticFilesStorage
from django.conf import settings


class YDcommonFileSystemStorage(StaticFilesStorage):

    def post_process(self, *args, **kwargs):
        if 'diet-images' in settings.INSTALLED_APPS:
            print "diet available"
