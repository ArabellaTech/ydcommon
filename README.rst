=========================
YD Technology Common libs
=========================

.. image:: https://travis-ci.org/ArabellaTech/ydcommon.png?branch=master
   :target: http://travis-ci.org/ArabellaTech/ydcommon

.. image:: https://coveralls.io/repos/ArabellaTech/ydcommon/badge.png?branch=master
   :target: https://coveralls.io/r/ArabellaTech/ydcommon/


System Requirements
===================
 - Python 2.7+

Settings
========
- ``IGNORE_QUNIT_HTML_FILES`` ignore HTML qunits files
- ``JSHINT_FILES_FIND`` JS Hint search files grep. Default ``-name "*.js" | xargs grep -l '/\*jslint' | grep -v libs``
- ``STATICFILES_STORAGE = "ydcommon.file_system_storage.YDcommonFileSystemStorage"`` - adds additional compression for all images in staticfiles directories. IMPORTANT: for this to work you need to add 'image_diet' to your INSTALLED APPS
- ``image_diet`` added into installed apps - required by "ydcommon.file_system_storage.YDcommonFileSystemStorage"
- ``YDCOMMON_COMPRESS_STATIC_IMAGES`` - compress static images when true. Collectstatic takes very long with this, set False for local and dev. Defaults to False.


Image_diet addons
========================
Docs: https://github.com/samastur/image-diet

Image_diet requires following libs:

- jpegoptim
- jpegtran
- gifsicle
- optipng
- advpng
- pngcrush

At least some of those should be installed to take advantage of compression. On OSX those can be installed via brew, on linux via your distribution package management system. Important: on ubuntu advpng and jpegtran are not available in standard repositiories. Not available extensions should be disabled in settings.py:

`DIET_JPEGOPTIM = False`

You can check available options by:
::
    
    ./manage.py check_diet_tools

It will output configuration options to put in your settings.py file if any of compression tools is not available.

Views
=====
``QunitTestsView`` Qunit tests (stuff permission required), example entry in urls.py:
::

    url(r"^js-tests/(?P<path>.*)", 'ydcommon.views.qunit_view', name='quinit'),

Commands
========
Checking requirement for tests
::
    ./manage.py check_test_requirements

Running Qunit tests
::

    ./manage.py run_qunit

Running JS Hint
::

    ./manage.py jshint

Clear database - drop all tables
::

    ./manage.py clear_database

Dump database
::
    ./manage.py dump_database
