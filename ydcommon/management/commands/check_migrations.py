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

    def handle(self, *args, **options):
        cmd = "./manage.py makemigrations %s --check --dry-run"
        for app in settings.PROJECT_APPS:
            # Skip main app name, e.g., demo.accounts => accounts
            submodule = app[app.find('.') + 1:]
            code, result = False, False
            if sys.version_info > (2, 7):
                try:
                    result = subprocess.check_call(cmd % submodule,
                                                   stderr=subprocess.STDOUT,
                                                   shell=True)
                except subprocess.CalledProcessError as e:
                    code = e.returncode
                    result = e.output
            else:
                code, result = commands.getstatusoutput(cmd % submodule)

            if code != 0:
                raise Exception('Missing migration')
