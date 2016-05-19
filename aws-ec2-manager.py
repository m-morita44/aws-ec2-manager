#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import sys
import enum
import boto3

__author__ = 'Masato Morita'
__version__ = '1.0.0'


HELP_SENTENCE = 'Usage: aws-ec2-manager.py <command> <instanceId>\n\n' + \
                'Common commands:\n' + \
                'help     shows the help for a subcommand.\n' + \
                'start    starts the instance.\n' + \
                'status   outputs status of the instance.\n' + \
                'stop     stops the instance.\n'


class State(enum.Enum):
    """
    State of the EC2 instance enumeration.
    """
    PENDING = 0
    RUNNING = 16
    SHUTTING_DOWN = 32
    TERMINATED = 48
    STOPPING = 64
    STOPPED = 80


def get_ec2_instance(id):
    """
    Get the EC2 instance from the configuration file.
    """
    ec2 = boto3.Session().resource('ec2')
    return ec2.Instance(id)


if __name__ == '__main__':
    try:
        command = sys.argv[1] if len(sys.argv) >= 2 else ''
        instanceId = sys.argv[2] if len(sys.argv) >= 3 else ''

        if command == 'start':
            # start command procedures.
            instance = get_ec2_instance(instanceId)
            
            # Check state of the instance.
            if State(instance.state['Code']) == State.RUNNING:
                print('Already started.')
                exit(0)
            elif State(instance.state['Code']) == State.PENDING:
                raise Exception('ERROR: The instance is {}, Can\'t start.'.format(instance.state['Name']))

            # start instance
            instance.start()
            instance.wait_until_running()
            print('Public IP: {}'.format(instance.public_ip_address))
            print('Status: {}'.format(instance.state['Name']))

        elif command == 'stop':
            # stop command procedures.
            instance = get_ec2_instance(instanceId)
            
            # Check state of the instance.
            if State(instance.state['Code']) in [State.SHUTTING_DOWN, State.STOPPING,
                                                 State.TERMINATED, State.STOPPED]:
                print('Already stopped.')
                exit(0)

            # stop instance
            instance.stop()
            instance.wait_until_stopped()
            print('Status: %(Name)s' % instance.state)

        elif command == 'status':
            # status command procedures.
            instance = get_ec2_instance(instanceId)
            print('Status: %(Name)s' % instance.state)

        elif command == 'help':
            # help command procedures.
            print(HELP_SENTENCE)

        else:
            # invalid command procedures.
            raise Exception(HELP_SENTENCE)

        exit(0)
    except Exception as e:
        print(e)
        exit(1)
