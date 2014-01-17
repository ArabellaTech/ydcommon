=========================
YD Technology Common libs
=========================

.. image:: https://travis-ci.org/YD-Technology/ydcommon.png?branch=master
   :target: http://travis-ci.org/YD-Technology/ydcommon

.. image:: https://coveralls.io/repos/YD-Technology/ydcommon/badge.png?branch=master
   :target: https://coveralls.io/r/YD-Technology/ydcommon/

.. image:: https://d2weczhvl823v0.cloudfront.net/YD-Technology/ydcommon/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

Settings
========
``IGNORE_QUNIT_HTML_FILES`` ignore HTML qunits files
``JSHINT_FILES_FIND`` JS Hint search files grep. Default ``-name "*.js" | xargs grep -l '/\*jslint' | grep -v libs``

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
