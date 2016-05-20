#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import enum
import boto3

__author__ = 'Masato Morita'
__version__ = '1.0.0'


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


class Ec2(object):
    """Object wrapper for resources.

    Provides an object interface to resources returned by the Soundcloud API.
    """
    def __init__(self, instance_id: str):
        self.__instance = boto3.Session().resource('ec2').Instance(instance_id)
        self.__message = ''

    @property
    def state(self) -> dict:
        """
        Get status.

        :return: Dictionary {Code: Int, Name: String}
        """
        return self.__instance.state

    @property
    def public_ip_address(self) -> str:
        """
        Get public ip address.

        :return: String
        """
        return self.__instance.public_ip_address

    @property
    def message(self) -> str:
        """
        Start message.

        :return: String
        """
        return self.__message

    def start(self) -> bool:
        """
        Start procedures.

        :return: Boolean
        """
        # initialize
        self.__message = ''

        # Check state of the instance.
        if State(self.state['Code']) == State.RUNNING:
            self.__message = 'Already started.'
            return True
        elif State(self.state['Code']) == State.PENDING:
            self.__message = 'ERROR: The instance is %(Name)s, Can\'t start.' % self.state
            return False

        # start instance
        self.__instance.start()
        self.__instance.wait_until_running()
        return True

    def stop(self) -> bool:
        """
        Stop procedures.

        :return: Boolean
        """
        # initialize
        self.__message = ''

        # Check state of the instance.
        if State(self.state['Code']) in [State.SHUTTING_DOWN, State.STOPPING,
                                         State.TERMINATED, State.STOPPED]:
            self.__message = 'Already stopped.'
            return True

        # start instance
        self.__instance.stop()
        self.__instance.wait_until_stopped()
        return True
