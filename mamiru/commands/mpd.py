#-*- coding: utf-8 -*-

import logging
from .base import Command
from mpd import MPDClient


class MPCPlayer(object):
    def __init__(self):
        self.client = MPDClient()
        self.client.timeout = 10
        self.client.idletimeout = None

    def connect(self):
        self.client.connect('localhost', 6600)
        logging.info('connect MPD')

    def disconnect(self):
        self.client.close()
        self.client.disconnect()
        logger.info('disconnect MPD')

    def __del__(self):
        self.disconnect()

    def __getattr__(self):
        return 'fdsf'
    

class MPDPlayCommand(Command):
    def __init__(self, player):
        self.player = player

    def __call__(self):
        logger.info('MPD Play')
        self.player.play()


class MPDPauseCommand(Command):
    def __init__(self, player):
        self.player = player
        
    def __call__(self):
        logger.info('MPD Pause')
        self.player.pause()


class MPDNextCommand(Command):
    def __init__(self, player):
        self.player = player

    def __call__(self):
        logger.info('MPD Next')
        self.player.next()
