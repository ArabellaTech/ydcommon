from django.contrib.staticfiles.storage import StaticFilesStorage
from django.conf import settings
from django.core.management import call_command


class YDcommonFileSystemStorage(StaticFilesStorage):

    def post_process(self, *args, **kwargs):
        if 'diet-images' in settings.INSTALLED_APPS:
            print "diet available"
            call_command('diet_images', settings.STATIC_ROOT)
