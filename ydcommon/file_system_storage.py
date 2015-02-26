import os
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.conf import settings


class YDCommonFileSystemStorage(StaticFilesStorage):

    def post_process(self, files, *args, **kwargs):
        results = []
        compress_images = getattr(settings, 'YDCOMMON_COMPRESS_STATIC_IMAGES', False)
        if compress_images:
            if 'image_diet' not in settings.INSTALLED_APPS:
                raise NotImplementedError("You need to install image_diet to use YDCOMMON_COMPRESS_STATIC_IMAGES")

            from image_diet import squeeze
            for f in files:
                processed_file = squeeze(os.path.join(settings.STATIC_ROOT, f))
                results.append([f, processed_file, True if processed_file is not None else False])
        return results
