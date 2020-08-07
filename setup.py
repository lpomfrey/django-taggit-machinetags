#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from setuptools import setup


_PUBLISH_WARNING = '''
******************
!!! DEPRECATED !!!
******************

Use twine to publish packages to pypi now.

Ensure you have the `wheel` and `twine` packages installed with

    pip install wheel twine

Then create some distributions like

    python setup.py sdist bdist_wheel

Then upload with twine

    twine upload dist/*
'''

if sys.argv[-1] == 'publish':
    print(_PUBLISH_WARNING)
    sys.exit()


setup(test_suite='runtests.runtests')
