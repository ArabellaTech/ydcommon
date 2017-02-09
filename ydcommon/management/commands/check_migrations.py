import sys
from django.conf import settings
from django.core.management.base import BaseCommand


try:
    import subprocess
    import commands
except ImportError:
    pass


class Command(BaseCommand):
    help = 'Render JSHint'

    def add_arguments(self, parser):
        parser.add_argument('-x', '--xml-output', action='store_true',
                            default=False,
                            dest='xml_output',
                            help='Render as XML')

    def handle(self, *args, **options):
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
