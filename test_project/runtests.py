#!/usr/bin/env python
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'
test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)


def runtests(*test_args):
    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    import django
    if hasattr(django, 'setup'):
        django.setup()

    from django.test.utils import get_runner
    from test_project import settings
    TestRunner = get_runner(settings)

    failures = TestRunner(
        verbosity=1,
        interactive=True,
        failfast=False).run_tests(['ydcommon'], *test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
