import os
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.conf import settings


class YDcommonFileSystemStorage(StaticFilesStorage):

    def post_process(self, files, *args, **kwargs):
        # print files
        results = []
        compress_images = getattr(settings, 'YDCOMMON_COMPRESS_STATIC_IMAGES', False)
        if 'image_diet' in settings.INSTALLED_APPS and compress_images:
            from image_diet import squeeze
            for f in files:
                processed_file = squeeze(os.path.join(settings.STATIC_ROOT, f))
                results.append([f, processed_file, True if processed_file is not None else False])
        return results
