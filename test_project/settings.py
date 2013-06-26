import os

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
