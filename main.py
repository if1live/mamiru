#!/usr/bin/env python
#-*- coding: utf-8 -*-

import logging
from asyncore import file_dispatcher, loop
from evdev import InputDevice, categorize, ecodes, events
from mpd import MPDClient
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

class MPDClientHelper(object):
    def create(self):
        client = MPDClient()
        client.timeout = 10
        client.idletimeout = None
        return client

    def connect(self, client):
        client.connect('localhost', 6600)
        logger.info('connect MPD')
        return client

    def disconnect(self, client):
        client.close()
        client.disconnect()
        logger.info('disconnect MPD')
        return client

# create singleton
mpd_helper = MPDClientHelper()
mpd_client = mpd_helper.create()
mpd_helper.connect(mpd_client)


class Command(object):
    def __call__(self):
        raise NotImplementedError()

class MPDPlayCommand(Command):
    def __init__(self, client):
        self.client = client

    def __call__(self):
        logger.info('MPD Play')
        self.client.play()

class MPDPauseCommand(Command):
    def __init__(self, client):
        self.client = client
        
    def __call__(self):
        logger.info('MPD Pause')
        self.client.pause()

class MPDNextCommand(Command):
    def __init__(self, client):
        self.client = client

    def __call__(self):
        logger.info('MPD Next')
        self.client.next()


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

