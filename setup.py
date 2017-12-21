#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
from setuptools import setup, find_packages


def get_version(package):
    '''
    Return package version as listed in `__version__` in `init.py`.
    '''
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search(
        '^__version__ = [\'"]([^\'"]+)[\'"]', init_py, re.MULTILINE
    ).group(1)


version = get_version('taggit_machinetags')

required = [
    'django-taggit>=0.12'
]

if sys.argv[-1] == 'publish':
    try:
        import wheel  # NOQA
    except ImportError:
        sys.stderr.write(
            'You need to `pip install wheel` before running publish'
        )
        sys.exit(1)
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    args = {'version': version}
    print('You probably want to also tag the version now:')
    print(' git tag -a {version} -m \'version {version}\''.format(
        **args))
    print(' git push --tags')
    sys.exit()


setup(
    name='django-taggit-machinetags',
    version=version,
    url='http://github.com/lpomfrey/django-taggit-machinetags',
    license='BSD',
    description='Machine tagging built upon django-taggit',
    author='Luke Pomfrey',
    author_email='lpomfrey@gmail.com',
    packages=find_packages(exclude=['test_project']),
    install_requires=required,
    tests_require=['mock'],
    test_suite='runtests.runtests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
