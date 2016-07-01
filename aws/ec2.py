#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
from enum import IntEnum, unique
from boto3 import Session


@unique
class State(IntEnum):
    """State of the EC2 instance enumeration."""
    pending = 0
    running = 16
    shutting_down = 32
    terminated = 48
    stopping = 64
    stopped = 80


class EC2(object):
    """Object wrapper for resources.

    Provides an object interface to resources returned by the Soundcloud API.
    """
    def __init__(self, instance_id: str):
        session = Session()
        self.__instance = session.resource('ec2').Instance(instance_id)
        self.__ssm = session.resource('ssm')

    @property
    def state(self) -> dict:
        """Get status.

        :return: Dictionary {Code: Int, Name: String}
        """
        return self.__instance.state

    @property
    def public_ip_address(self) -> str:
        """Get public ip address."""
        return self.__instance.public_ip_address

    def start(self):
        """Start procedures."""

        # Check state of the instance.
        if self.state['Code'] == State.running:
            return
        elif self.state['Code'] == State.pending:
            raise Exception('The instance is %(Name)s, Can\'t start.' % self.state)

        # Start instance
        self.__instance.start()
        self.__instance.wait_until_running()

    def stop(self):
        """Stop procedures."""

        # Check state of the instance.
        if self.state['Code'] in [State.shutting_down, State.stopping,
                                  State.terminated, State.stopped]:
            return

        # start instance
        self.__instance.stop()
        self.__instance.wait_until_stopped()

    def run_command(self, shell_command: str) -> str:
        """"Run Command procedures."""

        # Check state of the instance.
        if not self.state['Code'] == State.running:
            raise Exception('The instance is %(Name)s, Can\'t run command.' % self.state)

        result = self.__ssm.send_command([self.__instance.instance_id], 'AWS-RunShellScript',
                                         Parameters={'commands': [shell_command]})

        return result['Command']['Status']
