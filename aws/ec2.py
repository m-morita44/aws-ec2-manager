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
        self.__instance = Session().resource('ec2').Instance(instance_id)
        self.__message = ''

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

    @property
    def message(self) -> str:
        """Start message."""
        return self.__message

    def start(self) -> bool:
        """Start procedures."""
        # initialize
        self.__message = ''

        # Check state of the instance.
        if self.state['Code'] == State.running:
            self.__message = 'Already started.'
            return True
        elif self.state['Code'] == State.pending:
            self.__message = 'ERROR: The instance is %(Name)s, Can\'t start.' % self.state
            return False

        # start instance
        self.__instance.start()
        self.__instance.wait_until_running()
        return True

    def stop(self) -> bool:
        """Stop procedures."""
        # initialize
        self.__message = ''

        # Check state of the instance.
        if self.state['Code'] in [State.shutting_down, State.stopping,
                                  State.terminated, State.stopped]:
            self.__message = 'Already stopped.'
            return True

        # start instance
        self.__instance.stop()
        self.__instance.wait_until_stopped()
        return True
