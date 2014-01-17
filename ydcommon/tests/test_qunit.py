import mock
import sys

from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth.models import User

BUILTIN_MODULE = '__builtin__'
CMD = 'ydcommon.management.commands.run_qunit.commands.getstatusoutput'
CMD_VALUE = (0, """X
<!--
 Tests completed in 289 milliseconds.
16 tests of 16 passed, 0 failed.
-->X""")
if sys.version_info > (3, 0):
    BUILTIN_MODULE = 'builtins'

if sys.version_info > (2, 7):
    CMD = 'ydcommon.management.commands.run_qunit.subprocess.check_output'
    CMD_VALUE = ("""X
<!--
 Tests completed in 289 milliseconds.
16 tests of 16 passed, 0 failed.
-->X""")


class QunitTests(TestCase):

    @mock.patch(CMD)
    @mock.patch(BUILTIN_MODULE + ".open")
    def test_command(self, mock_open, mock_status):
        mock_status.return_value = CMD_VALUE
        call_command('run_qunit')
        self.assertTrue('example.html' in mock_status.call_args[0][0])

    def test_view(self):
        User.objects.create_superuser('foo', 'foo@foo.com' 'me', 'pass')

        self.client.login(username='foo', password='pass')
        response = self.client.get('/js-tests/')
        self.assertContains(response, '/js-tests/example')

        self.client.get('/js-tests/example')
        self.assertEqual(response.status_code, 200)
