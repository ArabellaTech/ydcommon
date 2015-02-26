from django.conf import settings

IGNORE_QUNIT_HTML_FILES = getattr(settings,
                                  'IGNORE_QUNIT_HTML_FILES', ['index', 'base'])

JSHINT_FILES_FIND = getattr(settings,
                            'JSHINT_FILES_FIND',
                            '-name "*.js" | xargs grep -l "/*jslint" | grep -v libs')
