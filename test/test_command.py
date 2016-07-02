#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
from unittest.mock import patch, Mock
from botocore.exceptions import NoRegionError
from command import Command
import unittest
from aws import EC2


# noinspection PyUnresolvedReferences
class TestCommand(unittest.TestCase):

    def test_init(self):
        # initialize
        help_sentence = 'Usage: aws-ec2-manager.py [options] <command> [<args>]\n\n' + \
                        '--help        Print this help.\n' + \
                        '\nCommon commands:\n' + \
                        'start         starts the instance.\n' + \
                        'status        outputs status of the instance.\n' + \
                        'stop          stops the instance.\n' + \
                        'run_command   run command to the instance.\n'

        # failure
        with self.assertRaises(ValueError) as e:
            Command([])

        self.assertEqual(str(e.exception), help_sentence)

        # failure
        with self.assertRaises(ValueError) as e:
            Command(['', 'invalid_method'])

        self.assertEqual(str(e.exception), help_sentence)

        # success
        cmd = Command(['', 'start'])
        self.assertEqual(cmd.command, 'start')

    def test_start(self):
        # initialize
        start_sentence = 'Usage: aws-ec2-manager.py start [options] <instance id>\n\n' + \
                         '--timeout sec    Tell init(8) to wait sec seconds, then shuts the system down'

        # success
        with patch.object(EC2, '__init__', Mock(side_effect=NoRegionError())):
            with self.assertRaises(NoRegionError) as e:
                Command(['', 'start']).start()

        self.assertEqual(str(e.exception), 'You must specify a region.')

        # failure
        with self.assertRaises(ValueError) as e:
            Command(['', 'start', '--invalid']).start()

        self.assertEqual(str(e.exception), start_sentence)

        # failure
        with self.assertRaises(ValueError) as e:
            Command(['', 'start', '--timeout']).start()

        self.assertEqual(str(e.exception), start_sentence)

        # failure
        with self.assertRaises(ValueError) as e:
            Command(['', 'start', '--timeout', 'sec']).start()

        self.assertEqual(str(e.exception), start_sentence)

        # success
        with patch.object(EC2, '__init__', Mock(side_effect=NoRegionError())):
            with self.assertRaises(NoRegionError) as e:
                Command(['', 'start', '--timeout', '55']).start()

        self.assertEqual(str(e.exception), 'You must specify a region.')

    def test_stop(self):
        # initialize
        stop_sentence = 'Usage: aws-ec2-manager.py stop <instance id>'

        # failure
        with self.assertRaises(ValueError) as e:
            Command(['', 'stop']).stop()

        self.assertEqual(str(e.exception), stop_sentence)

        # success
        with patch.object(EC2, '__init__', Mock(side_effect=NoRegionError())):
            with self.assertRaises(NoRegionError) as e:
                Command(['', 'stop', 'instance_id']).stop()

        self.assertEqual(str(e.exception), 'You must specify a region.')

        # failure
        with self.assertRaises(ValueError) as e:
            Command(['', 'stop', 'instance_id', 'invalid']).stop()

        self.assertEqual(str(e.exception), stop_sentence)

    def test_status(self):
        # initialize
        status_sentence = 'Usage: aws-ec2-manager.py status <instance id>'

        # failure
        with self.assertRaises(ValueError) as e:
            Command(['', 'status']).status()

        self.assertEqual(str(e.exception), status_sentence)

        # success
        with patch.object(EC2, '__init__', Mock(side_effect=NoRegionError())):
            with self.assertRaises(NoRegionError) as e:
                Command(['', 'status', 'instance_id']).status()

        self.assertEqual(str(e.exception), 'You must specify a region.')

        # failure
        with self.assertRaises(ValueError) as e:
            Command(['', 'status', 'instance_id', 'invalid']).status()

        self.assertEqual(str(e.exception), status_sentence)

    def test_run_command(self):
        # initialize
        run_command_sentence = 'Usage: aws-ec2-manager.py run_command <instance id> <shell command>'

        # failure
        with self.assertRaises(ValueError) as e:
            Command(['', 'run_command']).run_command()

        self.assertEqual(str(e.exception), run_command_sentence)

        # failure
        with self.assertRaises(ValueError) as e:
            Command(['', 'run_command', 'instance_id']).run_command()

        self.assertEqual(str(e.exception), run_command_sentence)

        # success
        with patch.object(EC2, '__init__', Mock(side_effect=NoRegionError())):
            with self.assertRaises(NoRegionError) as e:
                Command(['', 'run_command', 'instance_id', 'shell_command']).run_command()

        self.assertEqual(str(e.exception), 'You must specify a region.')

        # failure
        with self.assertRaises(ValueError) as e:
            Command(['', 'run_command', 'instance_id', 'shell_command', 'invalid']).run_command()

        self.assertEqual(str(e.exception), run_command_sentence)
