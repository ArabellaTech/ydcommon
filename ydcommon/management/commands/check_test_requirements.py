from __future__ import print_function

import sys

from django.core.management.base import NoArgsCommand

try:
    import subprocess
    import commands
except ImportError:
    pass


class Command(NoArgsCommand):
    help = 'Check test requirements'
    errors = []

    def check_req(self, name, cmd):
        print('Checking ' + name)
        if sys.version_info > (2, 7):
            try:
                result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
                code = 0
            except subprocess.CalledProcessError as e:
                result = e.output
                code = 1
        else:
            code, result = commands.getstatusoutput(cmd)
        if code != 0:
            self.errors.append('jshint')
        return code, result

    def handle_noargs(self, **options):
        self.check_req('jshint', 'jshint -v')
        code, result = self.check_req('phantomjs', 'phantomjs -v')
        if code == 0:
            versions = result.split('.')
            if int(versions[0]) < 1 or int(versions[1]) < 9:
                self.errors.append('phantomjs')

        if self.errors:
            print('Missing: ' + ', '.join(self.errors))
            exit(1)
        else:
            print('OK')
