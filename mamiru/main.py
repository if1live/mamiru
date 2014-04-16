#!/usr/bin/env python
#-*- coding: utf-8 -*-

import logging
from asyncore import file_dispatcher, loop
from evdev import InputDevice, categorize, ecodes, events
import signal
import sys


def create_logger():
    logger = logging.getLogger('kyoko')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)

    return logger

logger = create_logger()

# create singleton
mpd_helper = MPDClientHelper()
mpd_client = mpd_helper.create()
mpd_helper.connect(mpd_client)





command_dict = {
    ecodes.KEY_Q: MPDPlayCommand(mpd_client),
    ecodes.KEY_W: MPDPauseCommand(mpd_client),
    ecodes.KEY_E: MPDNextCommand(mpd_client)
}

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

            
# http://danielkaes.wordpress.com/2009/06/04/how-to-catch-kill-events-with-python/
def signal_handler(signal, frame):
    mpd_helper.disconnect(mpd_client)
    sys.exit(0)
signal.signal(signal.SIGTERM, signal_handler)


try:
    InputDeviceDispatcher(dev)
    loop()
except KeyboardInterrupt:
    mpd_helper.disconnect(mpd_client)

