import os
import django

DATABASE_ENGINE = 'sqlite3'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
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
    location("templates"),
)

STATIC_ROOT = location("static")

STATICFILES_DIRS = [
    location("static"),
]

SECRET_KEY = 'fake'

ROOT_URLCONF = 'test_project.urls'

if django.VERSION >= (1, 8):
    TEST_RUNNER = 'django.test.runner.DiscoverRunner'
else:
    TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
