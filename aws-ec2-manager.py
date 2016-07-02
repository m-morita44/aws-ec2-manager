#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
import sys
from command import Command


if __name__ == '__main__':
    try:
        cmd = Command(sys.argv)
        invoker = getattr(cmd, cmd.command)
        invoker()
        exit(0)
    except Exception as e:
        print(e)
        exit(1)
