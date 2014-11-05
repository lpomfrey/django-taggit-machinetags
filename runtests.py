# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys

import django


os.environ['PYTHONPATH'] = os.path.dirname(__file__)
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'


def runtests():
    if django.VERSION >= (1, 7):
        django.setup()
    from django.conf import settings
    from django.test.utils import get_runner
    test_runner = get_runner(settings)(verbosity=2)
    failures = test_runner.run_tests(['taggit_machinetags'])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
