import mock
import sys

from django.test import TestCase
from django.core.management import call_command

BUILTIN_MODULE = '__builtin__'
CMD = 'ydcommon.management.commands.run_qunit.commands.getstatusoutput'
CMD_VALUE = (0, 'X')
if sys.version_info > (3, 0):
    BUILTIN_MODULE = 'builtins'

if sys.version_info > (2, 7):
    import subprocess
    CMD = 'ydcommon.management.commands.run_qunit.subprocess.check_output'
    CMD_VALUE = ('X')


class JSHintTests(TestCase):

    @mock.patch(CMD)
    @mock.patch(BUILTIN_MODULE + ".open")
    def test_command(self, mock_open, mock_status):
        mock_status.return_value = CMD_VALUE
        call_command('jshint')
        self.assertTrue('--show-non-errors' in mock_status.call_args[0][0])

        call_command('jshint', xml_output=True)
        self.assertTrue('--reporter=checkstyle' in mock_status.call_args[0][0])

        if sys.version_info > (2, 7):
            mock_status.side_effect = subprocess.CalledProcessError('x', 'x', 'x')
        call_command('jshint', xml_output=True)
