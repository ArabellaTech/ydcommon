import os
import sys
from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpRequest
from optparse import make_option

from ydcommon.settings import IGNORE_QUNIT_HTML_FILES

try:
    import subprocess
    import commands
except ImportError:
    pass


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('-l', '--without-local-paths', action='store_false',
                    default=True,
                    dest='local_paths',
                    help='Render with changing js path to local'),
    )
    help = 'Render mvc tests'

    def handle_noargs(self, **options):
        qunit = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             '..', '..', 'scripts', 'run-qunit.js')

        request = HttpRequest()
        data = RequestContext(request)
        for template_dir in settings.TEMPLATE_DIRS:
            path = os.path.join(template_dir, 'js-tests')
            files = [f.replace('.html', '') for f in os.listdir(path)
                     if os.path.isfile(os.path.join(path, f))]
            for ignore_file in IGNORE_QUNIT_HTML_FILES:
                if ignore_file in files:
                    files.remove(ignore_file)
            for filename in files:
                file_path = 'js-tests/%s.html' % (filename)
                output = render_to_string(file_path, data).encode('utf-8')
                if options['local_paths']:
                    output = str(output)
                    output = output.replace('src="/static/', "src=\"${0}/"
                                            .format(settings.STATIC_ROOT))
                with open('reports/%s.html' % filename, 'w') as f:
                    f.write(output)
                cmd = "phantomjs %s file://`pwd`/reports/%s.html junit-xml" % \
                      (qunit, filename)
                if sys.version_info > (2, 7):
                    try:
                        result = subprocess.check_output(cmd,
                                                         stderr=subprocess.STDOUT,
                                                         shell=True)
                    except subprocess.CalledProcessError as e:
                        result = e.output
                else:
                    result = commands.getstatusoutput(cmd)
                with open('reports/junit-%s.xml' % filename, 'w') as f:
                    f.write(result[1])
