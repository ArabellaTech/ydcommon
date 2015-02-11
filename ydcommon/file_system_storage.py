import os
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.conf import settings


class YDcommonFileSystemStorage(StaticFilesStorage):

    def post_process(self, files, *args, **kwargs):
        # print files
        results = []
        print '1'
        if 'image_diet' in settings.INSTALLED_APPS:
            print 2
            from image_diet import squeeze
            for f in files:
                processed_file = squeeze(os.path.join(settings.STATIC_ROOT, f))
                results.append([f, processed_file, True if processed_file is not None else False])
        return results
