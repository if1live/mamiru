#!/usr/bin/env python
#-*- coding: utf-8 -*-

import logging
from asyncore import file_dispatcher, loop
from evdev import InputDevice, categorize, ecodes, events
import sys
from . import config
from .commands import CommandFactory

def create_command_dict(keylist):
    command_dict = {}
    factory = CommandFactory()
    for key, cmd_cls in keylist.items():
        cmd = factory.create_cmd(cmd_cls)
        command_dict[key] = cmd
    return command_dict


# TODO: if /dev/input/event0 is not keyboard...
dev = InputDevice('/dev/input/event0')

class InputDeviceDispatcher(file_dispatcher):
    def __init__(self, device):
        self.device = device
        file_dispatcher.__init__(self, device)

    def recv(self, ign=None):
        return self.device.read()

    def handle_read(self):
        for event in self.recv():
            if event.type != ecodes.EV_KEY:
                continue

            if event.value != events.KeyEvent.key_up:
                continue

            if event.code in command_dict:
                cmd = command_dict[event.code]
                cmd()


def main():
    InputDeviceDispatcher(dev)
    loop()
