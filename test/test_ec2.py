#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
from unittest.mock import patch
from aws import EC2
import unittest


class StubEC2(EC2):

    def __init__(self):
        self.__instance = None
        self.__message = ''


class InstanceId:

    def start(self):
        return None

    def stop(self):
        return None

    def wait_until_running(self):
        return None

    def wait_until_stopped(self):
        return None


# noinspection PyUnresolvedReferences
class TestEC2(unittest.TestCase):

    def test_init(self):
        # false
        with self.assertRaises(Exception) as e:
            EC2('')

        self.assertEqual(str(e.exception), 'You must specify a region.')

    def test_start(self):
        ec2 = StubEC2()
        ec2._EC2__instance = InstanceId()

        with patch.object(StubEC2, 'state', {'Code': 0, 'Name': 'pending'}):
            self.assertEqual(ec2.start(), False)
            self.assertEqual(ec2.message, 'ERROR: The instance is pending, Can\'t start.')

        with patch.object(StubEC2, 'state', {'Code': 16, 'Name': 'RUNNING'}):
            self.assertEqual(ec2.start(), True)
            self.assertEqual(ec2.message, 'Already started.')

        with patch.object(StubEC2, 'state', {'Code': 32, 'Name': 'SHUTTING_DOWN'}):
            self.assertEqual(ec2.start(), True)
            self.assertEqual(ec2.message, '')

        with patch.object(StubEC2, 'state', {'Code': 48, 'Name': 'TERMINATED'}):
            self.assertEqual(ec2.start(), True)
            self.assertEqual(ec2.message, '')

        with patch.object(StubEC2, 'state', {'Code': 64, 'Name': 'STOPPING'}):
            self.assertEqual(ec2.start(), True)
            self.assertEqual(ec2.message, '')

        with patch.object(StubEC2, 'state', {'Code': 80, 'Name': 'STOPPED'}):
            self.assertEqual(ec2.start(), True)
            self.assertEqual(ec2.message, '')

    def test_stop(self):
        ec2 = StubEC2()
        ec2._EC2__instance = InstanceId()

        with patch.object(StubEC2, 'state', {'Code': 0, 'Name': 'PENDING'}):
            self.assertEqual(ec2.stop(), True)
            self.assertEqual(ec2.message, '')

        with patch.object(StubEC2, 'state', {'Code': 16, 'Name': 'RUNNING'}):
            self.assertEqual(ec2.stop(), True)
            self.assertEqual(ec2.message, '')

        with patch.object(StubEC2, 'state', {'Code': 32, 'Name': 'SHUTTING_DOWN'}):
            self.assertEqual(ec2.stop(), True)
            self.assertEqual(ec2.message, 'Already stopped.')

        with patch.object(StubEC2, 'state', {'Code': 48, 'Name': 'TERMINATED'}):
            self.assertEqual(ec2.stop(), True)
            self.assertEqual(ec2.message, 'Already stopped.')

        with patch.object(StubEC2, 'state', {'Code': 64, 'Name': 'STOPPING'}):
            self.assertEqual(ec2.stop(), True)
            self.assertEqual(ec2.message, 'Already stopped.')

        with patch.object(StubEC2, 'state', {'Code': 80, 'Name': 'STOPPED'}):
            self.assertEqual(ec2.stop(), True)
            self.assertEqual(ec2.message, 'Already stopped.')
