=========================
YD Technology Common libs
=========================

.. image:: https://travis-ci.org/YD-Technology/ydcommon.png?branch=master
   :target: http://travis-ci.org/YD-Technology/ydcommon

.. image:: https://coveralls.io/repos/YD-Technology/ydcommon/badge.png?branch=master
   :target: https://coveralls.io/r/YD-Technology/ydcommon/

Settings
========
``IGNORE_QUNIT_HTML_FILES`` ignore HTML qunits files

Views
=====
``QunitTestsView`` Qunit tests (stuff permission required), example entry in urls.py:
::

    url(r"^js-tests/(?P<path>.*)", 'ydcommon.views.qunit_view'),

Commands
========
Running Qunit tests
::

    ./manage.py run_qunit
