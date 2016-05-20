#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import sys
from aws.ec2 import Ec2

__author__ = 'Masato Morita'
__version__ = '1.0.1'


HELP_SENTENCE = 'Usage: aws-ec2-manager.py <command> <instanceId>\n\n' + \
                'Common commands:\n' + \
                'help     shows the help for a subcommand.\n' + \
                'start    starts the instance.\n' + \
                'status   outputs status of the instance.\n' + \
                'stop     stops the instance.\n'

if __name__ == '__main__':
    try:
        command = sys.argv[1] if len(sys.argv) >= 2 else ''
        instanceId = sys.argv[2] if len(sys.argv) >= 3 else ''

        if command == 'start':
            # start command procedures.
            ec2 = Ec2(instanceId)
            if not ec2.start():
                raise Exception(ec2.message)

            print('Public IP: %s' % ec2.public_ip_address)
            print('Status: %(Name)s' % ec2.state)

        elif command == 'stop':
            # stop command procedures.
            ec2 = Ec2(instanceId)
            
            if not ec2.stop():
                raise Exception(ec2.message)

            print('Status: %(Name)s' % ec2.state)

        elif command == 'status':
            # status command procedures.
            ec2 = Ec2(instanceId)
            print('Status: %(Name)s' % ec2.state)

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
