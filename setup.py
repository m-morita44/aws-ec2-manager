#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='aws-ec2-manager',
      version='1.5',
      description='AWS EC2 Manager',
      author='Masato Morita',
      author_email='m.morita44@hotmail.com',
      url='https://github.com/m-morita44',
      scripts=['aws-ec2-manager.py'],
      packages=["aws", "command"],
      test_suite="test",
      )
