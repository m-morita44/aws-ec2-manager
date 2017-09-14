#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
from unittest.mock import patch, Mock
from botocore.exceptions import NoRegionError
from aws import EC2
import unittest


class StubEC2(EC2):

    def __init__(self):
        self.__instance = None
        self.__message = ''


class InstanceId(object):

    @property
    def instance_id(self):
        return None

    @staticmethod
    def start():
        return None

    @staticmethod
    def stop():
        return None

    @staticmethod
    def wait_until_running():
        return None

    @staticmethod
    def wait_until_stopped():
        return None


class SSM(object):

    @staticmethod
    def send_command(*args, **kwargs) -> dict:
        return {'Command': {'Status': 'Pending'}}


# noinspection PyUnresolvedReferences
class TestEC2(unittest.TestCase):

    def setUp(self):
        self.ec2 = StubEC2()
        self.ec2._EC2__instance = InstanceId()
        self.ec2._EC2__ssm = SSM()

    def test_init(self):
        # failure
        with patch.object(EC2, '__init__', Mock(side_effect=NoRegionError())):
            with self.assertRaises(NoRegionError) as e:
                EC2('')

        self.assertEqual(str(e.exception), 'You must specify a region.')

    def test_start(self):
        # failure
        with patch.object(StubEC2, 'state', {'Code': 0, 'Name': 'PENDING'}):
            with self.assertRaises(Exception) as e:
                self.ec2.start()

            self.assertEqual(str(e.exception), 'The instance is PENDING, Can\'t start.')

        # success
        with patch.object(StubEC2, 'state', {'Code': 16, 'Name': 'RUNNING'}):
            self.ec2.start()

        # success
        with patch.object(StubEC2, 'state', {'Code': 32, 'Name': 'SHUTTING_DOWN'}):
            self.ec2.start()

        # success
        with patch.object(StubEC2, 'state', {'Code': 48, 'Name': 'TERMINATED'}):
            self.ec2.start()

        # success
        with patch.object(StubEC2, 'state', {'Code': 64, 'Name': 'STOPPING'}):
            self.ec2.start()

        # success
        with patch.object(StubEC2, 'state', {'Code': 80, 'Name': 'STOPPED'}):
            self.ec2.start()

    def test_stop(self):
        # success
        with patch.object(StubEC2, 'state', {'Code': 0, 'Name': 'PENDING'}):
            self.ec2.stop()

        # success
        with patch.object(StubEC2, 'state', {'Code': 16, 'Name': 'RUNNING'}):
            self.ec2.stop()

        # success
        with patch.object(StubEC2, 'state', {'Code': 32, 'Name': 'SHUTTING_DOWN'}):
            self.ec2.stop()

        # success
        with patch.object(StubEC2, 'state', {'Code': 48, 'Name': 'TERMINATED'}):
            self.ec2.stop()

        # success
        with patch.object(StubEC2, 'state', {'Code': 64, 'Name': 'STOPPING'}):
            self.ec2.stop()

        # success
        with patch.object(StubEC2, 'state', {'Code': 80, 'Name': 'STOPPED'}):
            self.ec2.stop()

    def test_run_command(self):
        # failure
        with patch.object(StubEC2, 'state', {'Code': 0, 'Name': 'PENDING'}):
            with self.assertRaises(Exception) as e:
                self.ec2.run_command('')

        self.assertEqual(str(e.exception), 'The instance is PENDING, Can\'t run command.')

        # success
        with patch.object(StubEC2, 'state', {'Code': 16, 'Name': 'RUNNING'}):
            self.assertEqual(self.ec2.run_command(''), 'Pending')

        # failure
        with patch.object(StubEC2, 'state', {'Code': 32, 'Name': 'SHUTTING_DOWN'}):
            with self.assertRaises(Exception) as e:
                self.ec2.run_command('')

        self.assertEqual(str(e.exception), 'The instance is SHUTTING_DOWN, Can\'t run command.')

        # failure
        with patch.object(StubEC2, 'state', {'Code': 48, 'Name': 'TERMINATED'}):
            with self.assertRaises(Exception) as e:
                self.ec2.run_command('')

        self.assertEqual(str(e.exception), 'The instance is TERMINATED, Can\'t run command.')

        # failure
        with patch.object(StubEC2, 'state', {'Code': 64, 'Name': 'STOPPING'}):
            with self.assertRaises(Exception) as e:
                self.ec2.run_command('')

        self.assertEqual(str(e.exception), 'The instance is STOPPING, Can\'t run command.')

        # failure
        with patch.object(StubEC2, 'state', {'Code': 80, 'Name': 'STOPPED'}):
            with self.assertRaises(Exception) as e:
                self.ec2.run_command('')

        self.assertEqual(str(e.exception), 'The instance is STOPPED, Can\'t run command.')
