#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
requirements = open('requirements.txt').readlines()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='vauxootools',
    version='0.1.8',
    description='Tools to work with python and Odoo',
    long_description=readme + '\n\n' + history,
    author='Nhomar Hernandez',
    author_email='nhomar@vauxoo.com',
    url='https://github.com/vauxoo/vauxootools',
    packages=[
        'vauxootools',
    ],
    scripts = [
        'scripts/openerp_verify',
        'scripts/simpletimetracker',
    ],
    package_dir={'vauxootools': 'vauxootools'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='vauxootools',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
)
