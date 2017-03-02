from django.conf import settings


def get_template_dirs():
    try:
        dirs = settings.TEMPLATES[0]['DIRS']
    except (AttributeError, IndexError, KeyError):
        dirs = getattr(settings, 'TEMPLATE_DIRS', [])

    return list(dirs)
