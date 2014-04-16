#-*- coding: utf-8 -*-

import logging
from .base import Command
import mpd
import socket


class MPDPlayer(object):
    def __init__(self):
        self.client = mpd.MPDClient()
        self.client.timeout = 10
        self.client.idletimeout = None

    def open(self):
        try:
            self.client.connect('localhost', 6600)
            logging.info('connect MPD')
            return True
        except socket.error:
            return False

    def close(self):
        try:
            self.client.close()
            self.client.disconnect()
            logger.info('disconnect MPD')
            return True
        except mpd.ConnectionError:
            return False

    def __del__(self):
        self.close()

    def __getattr__(self, key):
        return getattr(self.client, key)

class MPDCommand(Command):
    def __init__(self, player):
        self.player = player

    def __call__(self):
        try:
            return self.run()
        except mpd.ConnectionError as e:
            msg = '{} Fail : {}'.format(type(self), e)
            logging.info(msg)
            return False

    def run(self):
        raise NotImplementedError()


class MPDPlayCommand(MPDCommand):
    def __init__(self, player):
        MPDCommand.__init__(self, player)

    def run(self):
        logging.info('MPD Play')
        self.player.play()
        return True


class MPDPauseCommand(MPDCommand):
    def __init__(self, player):
        MPDCommand.__init__(self, player)

    def run(self):
        logging.info('MPD Pause')
        self.player.pause()
        return True


class MPDNextCommand(MPDCommand):
    def __init__(self, player):
        MPDCommand.__init__(self, player)

    def run(self):
        logging.info('MPD Next')
        self.player.next()
        return True
