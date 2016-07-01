#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
from unittest.mock import patch
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

    def test_init(self):
        # false
        with self.assertRaises(Exception) as e:
            EC2('')

        self.assertEqual(str(e.exception), 'You must specify a region.')

    def test_start(self):
        ec2 = StubEC2()
        ec2._EC2__instance = InstanceId()

        with patch.object(StubEC2, 'state', {'Code': 0, 'Name': 'PENDING'}):
            with self.assertRaises(Exception) as e:
                ec2.start()

            self.assertEqual(str(e.exception), 'The instance is PENDING, Can\'t start.')

        with patch.object(StubEC2, 'state', {'Code': 16, 'Name': 'RUNNING'}):
            ec2.start()

        with patch.object(StubEC2, 'state', {'Code': 32, 'Name': 'SHUTTING_DOWN'}):
            ec2.start()

        with patch.object(StubEC2, 'state', {'Code': 48, 'Name': 'TERMINATED'}):
            ec2.start()

        with patch.object(StubEC2, 'state', {'Code': 64, 'Name': 'STOPPING'}):
            ec2.start()

        with patch.object(StubEC2, 'state', {'Code': 80, 'Name': 'STOPPED'}):
            ec2.start()

    def test_stop(self):
        ec2 = StubEC2()
        ec2._EC2__instance = InstanceId()

        with patch.object(StubEC2, 'state', {'Code': 0, 'Name': 'PENDING'}):
            ec2.stop()

        with patch.object(StubEC2, 'state', {'Code': 16, 'Name': 'RUNNING'}):
            ec2.stop()

        with patch.object(StubEC2, 'state', {'Code': 32, 'Name': 'SHUTTING_DOWN'}):
            ec2.stop()

        with patch.object(StubEC2, 'state', {'Code': 48, 'Name': 'TERMINATED'}):
            ec2.stop()

        with patch.object(StubEC2, 'state', {'Code': 64, 'Name': 'STOPPING'}):
            ec2.stop()

        with patch.object(StubEC2, 'state', {'Code': 80, 'Name': 'STOPPED'}):
            ec2.stop()

    def test_run_command(self):
        ec2 = StubEC2()
        ec2._EC2__instance = InstanceId()
        ec2._EC2__ssm = SSM()

        with patch.object(StubEC2, 'state', {'Code': 0, 'Name': 'PENDING'}):
            with self.assertRaises(Exception) as e:
                ec2.run_command('')

        self.assertEqual(str(e.exception), 'The instance is PENDING, Can\'t run command.')

        with patch.object(StubEC2, 'state', {'Code': 16, 'Name': 'RUNNING'}):
            self.assertEqual(ec2.run_command(''), 'Pending')

        with patch.object(StubEC2, 'state', {'Code': 32, 'Name': 'SHUTTING_DOWN'}):
            with self.assertRaises(Exception) as e:
                ec2.run_command('')

        self.assertEqual(str(e.exception), 'The instance is SHUTTING_DOWN, Can\'t run command.')

        with patch.object(StubEC2, 'state', {'Code': 48, 'Name': 'TERMINATED'}):
            with self.assertRaises(Exception) as e:
                ec2.run_command('')

        self.assertEqual(str(e.exception), 'The instance is TERMINATED, Can\'t run command.')

        with patch.object(StubEC2, 'state', {'Code': 64, 'Name': 'STOPPING'}):
            with self.assertRaises(Exception) as e:
                ec2.run_command('')

        self.assertEqual(str(e.exception), 'The instance is STOPPING, Can\'t run command.')

        with patch.object(StubEC2, 'state', {'Code': 80, 'Name': 'STOPPED'}):
            with self.assertRaises(Exception) as e:
                ec2.run_command('')

        self.assertEqual(str(e.exception), 'The instance is STOPPED, Can\'t run command.')
