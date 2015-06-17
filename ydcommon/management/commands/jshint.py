import sys
from django.conf import settings
from django.core.management.base import NoArgsCommand
from optparse import make_option

from ydcommon.settings import JSHINT_FILES_FIND

try:
    import subprocess
    import commands
except ImportError:
    pass


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('-x', '--xml-output', action='store_true',
                    default=False,
                    dest='xml_output',
                    help='Render as XML'),
        make_option('-d', '--dir', action='store',
                    default=None,
                    dest='search_dir',
                    help='Search files in directory'),
    )
    help = 'Render JSHint'

    def handle_noargs(self, xml_output, search_dir=None, **options):
        files = []
        if search_dir is not None:
            search_dir = [search_dir]
        else:
            search_dir = settings.STATICFILES_DIRS
        for path in search_dir:
            cmd = "find %s %s" % (path, JSHINT_FILES_FIND)
            if sys.version_info > (2, 7):
                try:
                    result = subprocess.check_output(cmd,
                                                     stderr=subprocess.STDOUT,
                                                     shell=True)
                except subprocess.CalledProcessError:
                    return
            else:
                code, result = commands.getstatusoutput(cmd)
            for f in result.split('\n'):
                if f.strip():
                    files.append(f.strip())

            if xml_output:
                cmd = 'jshint --reporter=checkstyle %s' % (' '.join(files))
            else:
                cmd = 'jshint --show-non-errors %s' % (' '.join(files))
            if sys.version_info > (2, 7):
                try:
                    result = subprocess.check_output(cmd,
                                                     stderr=subprocess.STDOUT,
                                                     shell=True)
                    code = 0
                except subprocess.CalledProcessError as e:
                    result = e.output
                    code = e.returncode
            else:
                code, result = commands.getstatusoutput(cmd)
            if result:
                sys.stdout.write(result)
            if not xml_output:
                message = 'OK' if code == 0 else 'Error'
                sys.stdout.write('%s! (Checked files: %d)' % (message, len(files)))
