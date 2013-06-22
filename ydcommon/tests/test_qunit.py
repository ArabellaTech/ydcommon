import mock
import sys

from django.test import TestCase
from django.core.management import call_command

BUILTIN_MODULE = '__builtin__'
CMD = 'ydcommon.management.commands.run_qunit.commands.getstatusoutput'
if sys.version_info > (3, 0):
    BUILTIN_MODULE = 'builtins'

if sys.version_info > (2, 7):
    CMD = 'ydcommon.management.commands.run_qunit.subprocess.check_output'


class RunQunitTest(TestCase):

    @mock.patch(CMD)
    @mock.patch(BUILTIN_MODULE + ".open")
    def test_run(self, mock_open, mock_status):
        call_command('run_qunit')
        self.assertTrue('example.html' in mock_status.call_args[0][0])
