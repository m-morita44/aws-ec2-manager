#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import sys
from aws import EC2

HELP_SENTENCE = 'Usage: aws-ec2-manager.py [options] <command> [<args>]\n\n' + \
                '--help        Print this help.\n' + \
                '\nCommon commands:\n' + \
                'start         starts the instance.\n' + \
                'status        outputs status of the instance.\n' + \
                'stop          stops the instance.\n' + \
                'run_command   run command to the instance.\n'

if __name__ == '__main__':
    try:

        # check command or option.
        command = sys.argv[1] if len(sys.argv) >= 2 else ''
        if command in ['--help']:
            print(HELP_SENTENCE)
            exit(0)
        elif command not in ['start', 'status', 'stop', 'run_command']:
            raise ValueError(HELP_SENTENCE)

        # execute command.
        if command == 'start':
            # start command procedures.
            options = dict()
            instance_id = ''

            # check arguments.
            try:
                args = iter(sys.argv[2:])
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

            print('Public IP: %s' % ec2.public_ip_address)
            print('Status: %(Name)s' % ec2.state)

            if 'timeout' in options:
                print('Result Status: %s' % ec2.run_command('shutdown -t %s' % options['timeout']))

        elif command == 'stop':
            # stop command procedures.

            # check arguments.
            if not len(sys.argv) == 3:
                raise ValueError('Usage: aws-ec2-manager.py stop <instance id>')

            ec2 = EC2(sys.argv[2])
            ec2.stop()

            print('Status: %(Name)s' % ec2.state)

        elif command == 'status':
            # status command procedures.

            # check arguments.
            if not len(sys.argv) == 3:
                raise ValueError('Usage: aws-ec2-manager.py status <instance id>')

            ec2 = EC2(sys.argv[2])

            print('Status: %(Name)s' % ec2.state)
            print('Public IP: %s' % ec2.public_ip_address)

        elif command == 'run_command':
            # run_command command procedures.

            # check arguments.
            if not len(sys.argv) == 4:
                raise ValueError('Usage: aws-ec2-manager.py run_command <instance id> <shell command>')

            ec2 = EC2(sys.argv[2])
            print('Result Status: %s' % ec2.run_command(sys.argv[3]))

        exit(0)
    except Exception as e:
        print(e)
        exit(1)
