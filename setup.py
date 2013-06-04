#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()


setup(
    name='dota2',
    version='0.0.1',
    description='API Wrapper for Dota 2\'s WebAPI.',
    long_description=open('README.md').read(),
    author='Bryan Veloso',
    author_email='bryan@revyver.com',
    url='https://github.com/bryanveloso/dota2.py',
    py_modules=['dota2'],
    install_requires=['requests'],
    license='MIT',
)
