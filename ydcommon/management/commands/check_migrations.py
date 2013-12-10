import sys
from django.conf import settings
from django.core.management.base import NoArgsCommand
from optparse import make_option


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
    )
    help = 'Render JSHint'

    def handle_noargs(self, xml_output, **options):
        cmd = "./manage.py schemamigration %s --auto"
        for app in settings.PROJECT_APPS:
            code, result = False, False
            if sys.version_info > (2, 7):
                try:
                    result = subprocess.check_call(cmd % app,
                                                   stderr=subprocess.STDOUT,
                                                   shell=True)
                except subprocess.CalledProcessError as e:
                    code = e.returncode
                    result = e.output
            else:
                code, result = commands.getstatusoutput(cmd % app)

            if code != 1:
                raise Exception('Missing migration')
