from django.conf import settings
IGNORE_QUNIT_HTML_FILES = getattr(settings,
                                  'IGNORE_QUNIT_HTML_FILES', ['index', 'base'])
