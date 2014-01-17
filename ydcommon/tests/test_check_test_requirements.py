import mock
import sys

from django.test import TestCase
from django.core.management import call_command

BUILTIN_MODULE = '__builtin__'
CMD = 'ydcommon.management.commands.check_test_requirements.commands.getstatusoutput'
CMD_VALUE = (0, '1.9.2')
CMD_VALUE_WRONG = (0, '1.8.2')
if sys.version_info > (3, 0):
    BUILTIN_MODULE = 'builtins'

if sys.version_info > (2, 7):
    CMD = 'ydcommon.management.commands.check_test_requirements.subprocess.check_output'
    CMD_VALUE = ('1.9.2')
    CMD_VALUE_WRONG = ('1.8.2')


class CheckTestRequirementsTests(TestCase):

    @mock.patch(CMD)
    def test_command(self, mock_status):
        mock_status.return_value = CMD_VALUE
        call_command('check_test_requirements')
        self.assertTrue('jshint -v' in mock_status.call_args_list[0][0])
        self.assertTrue('phantomjs -v' in mock_status.call_args_list[1][0])

    @mock.patch(CMD)
    def test_wrong_phantomjs(self, mock_status):
        mock_status.return_value = CMD_VALUE_WRONG
        with self.assertRaises(SystemExit):
            call_command('check_test_requirements')
