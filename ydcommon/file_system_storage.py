import os
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.conf import settings


class YDcommonFileSystemStorage(StaticFilesStorage):

    def post_process(self, files, *args, **kwargs):
        # print files
        results = []
        if 'image_diet' in settings.INSTALLED_APPS and settings.YDCOMMON_COMPRESS_IMAGES:
            from image_diet import squeeze
            for f in files:
                processed_file = squeeze(os.path.join(settings.STATIC_ROOT, f))
                results.append([f, processed_file, True if processed_file is not None else False])
        return results
