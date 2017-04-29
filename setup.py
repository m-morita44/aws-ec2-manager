#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(name='aws-ec2-manager',
      version='1.5.1',
      description='the tools is managing AWS EC2 instance by python3.',
      url='https://github.com/m-morita44',
      author='Masato Morita',
      author_email='m.morita44@hotmail.com',
      license='MIT',
      scripts=['aws-ec2-manager.py'],
      packages=find_packages(),
      install_requires=['boto3'],
      test_suite='tests')
