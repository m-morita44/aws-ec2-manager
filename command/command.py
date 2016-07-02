#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
from aws import EC2


class Command(object):

    __help_sentence__ = 'Usage: aws-ec2-manager.py [options] <command> [<args>]\n\n' + \
                        '--help        Print this help.\n' + \
                        '\nCommon commands:\n' + \
                        'start         starts the instance.\n' + \
                        'status        outputs status of the instance.\n' + \
                        'stop          stops the instance.\n' + \
                        'run_command   run command to the instance.\n'

    def __init__(self, args: list):
        self.__command = args[1] if len(args) >= 2 else ''
        self.__arguments = args

        if self.__command == '--help':
            print(Command.__help_sentence__)
            exit(0)
        elif self.__command not in ['start', 'status', 'stop', 'run_command']:
            raise ValueError(Command.__help_sentence__)

    @property
    def command(self):
        return self.__command

    def start(self):
        """start command procedures."""
        options = dict()
        instance_id = ''

        # check arguments.
        try:
            args = iter(self.__arguments[2:])
            for a in args:
                if a[0] == '-':
                    if a == '--timeout':
                        options['timeout'] = next(args, '')
                        if not options['timeout'].isdigit():
                            raise ValueError('Usage: aws-ec2-manager.py start [options] <instance id>\n\n' +
                                             '--timeout sec    Tell init(8) to wait sec seconds, then shuts the system down');
                    else:
                        raise ValueError('Usage: aws-ec2-manager.py start [options] <instance id>\n\n' +
                                         '--timeout sec    Tell init(8) to wait sec seconds, then shuts the system down')
                else:
                    instance_id = a
        except StopIteration:
            pass

        ec2 = EC2(instance_id)
        ec2.start()

        print('Status: %(Name)s' % ec2.state)
        print('Public IP: %s' % ec2.public_ip_address)

        if 'timeout' in options:
            print('Result Status: %s' % ec2.run_command('shutdown -h +%s' % options['timeout']))

    def stop(self):
        """stop command procedures."""

        # check arguments.
        if not len(self.__arguments) == 3:
            raise ValueError('Usage: aws-ec2-manager.py stop <instance id>')

        ec2 = EC2(self.__arguments[2])
        ec2.stop()

        print('Status: %(Name)s' % ec2.state)

    def status(self):
        """status command procedures."""

        # check arguments.
        if not len(self.__arguments) == 3:
            raise ValueError('Usage: aws-ec2-manager.py status <instance id>')

        ec2 = EC2(self.__arguments[2])

        print('Status: %(Name)s' % ec2.state)
        print('Public IP: %s' % ec2.public_ip_address)

    def run_command(self):
        """run_command command procedures."""

        # check arguments.
        if not len(self.__arguments) == 4:
            raise ValueError('Usage: aws-ec2-manager.py run_command <instance id> <shell command>')

        ec2 = EC2(self.__arguments[2])
        print('Result Status: %s' % ec2.run_command(self.__arguments[3]))
