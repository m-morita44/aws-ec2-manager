#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='aws-ec2-manager',
    version='1.5.2',
    description='the tools is managing AWS EC2 instance by python3.',
    url='https://github.com/mmorita44/aws-ec2-manager',
    author='Masato Morita',
    author_email='m.morita44@hotmail.com',
    license='MIT',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Customer Service',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6'],
    scripts=['scripts/aws-ec2-manager'],
    packages=find_packages(),
    install_requires=['boto3'],
    test_suite='tests'
)
