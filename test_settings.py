import os

DATABASE_ENGINE = 'sqlite3'

INSTALLED_APPS = (
    'ydcommon',
)
DATABASES = {
    'default': {
        'NAME': ':memory:',
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

project = lambda: os.path.dirname(os.path.realpath(__file__))
location = lambda x: os.path.join(str(project()), str(x))

TEMPLATE_DIRS = (
    location("test_project/templates"),
)

STATIC_ROOT = location("test_project/static")
