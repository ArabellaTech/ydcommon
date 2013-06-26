import os
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse

from ydcommon.settings import IGNORE_QUNIT_HTML_FILES


class QunitTestsView(TemplateView):
    template_name = 'ydcommon/js-tests/index.html'

    def get_context_data(self, **kwargs):
        context = super(QunitTestsView, self).get_context_data(**kwargs)
        if not kwargs['path'] or kwargs['path'] == 'index':
            for template_dir in settings.TEMPLATE_DIRS:
                path = os.path.join(template_dir, 'js-tests')
                files = [f.replace('.html', '') for f in os.listdir(path)
                         if os.path.isfile(os.path.join(path, f))]
                for ignore_file in IGNORE_QUNIT_HTML_FILES:
                    if ignore_file in files:
                        files.remove(ignore_file)
                tests = []
                for f in files:
                    tests.append({'file': f,
                                  'url': reverse(qunit_view, args=[f])})
            context['tests'] = tests
        return context

    def get(self, request, *args, **kwargs):
        if not kwargs['path']:
            self.template_name = 'ydcommon/js-tests/index.html'
        else:
            self.template_name = 'js-tests/%s.html' % kwargs['path']
        return super(QunitTestsView, self).get(request, *args, **kwargs)

qunit_view = staff_member_required(QunitTestsView.as_view())
