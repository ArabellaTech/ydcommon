from django.test import TestCase, override_settings

from ydcommon.utils.settings import get_template_dirs


class UtilsTests(TestCase):
    def test_settings(self):
        # test old Django configuration
        template_dirs = ['a', 'b']
        with override_settings(TEMPLATES=[{'BACKEND': '1'}], TEMPLATE_DIRS=template_dirs):
            self.assertListEqual(get_template_dirs(), template_dirs)

        # test Django > 1.8
        with override_settings(TEMPLATES=[{'BACKEND': '1', 'DIRS': template_dirs}]):
            self.assertListEqual(get_template_dirs(), template_dirs)
