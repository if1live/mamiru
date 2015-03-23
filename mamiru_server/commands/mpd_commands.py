#-*- coding: utf-8 -*-

from mamiru.app import logger
import mpd
from .base import Command
from mamiru.mpd_player import MPDPlayer

class MPDCommand(Command):
    def __init__(self, player):
        self.player = player

    def __call__(self):
        try:
            return self.run()
        except mpd.ConnectionError as e:
            msg = '{} Fail : {}'.format(type(self).__name__, e)
            logger.info(msg)
            return False

    def run(self):
        raise NotImplementedError()


class MPDPlayCommand(MPDCommand):
    def __init__(self, player):
        MPDCommand.__init__(self, player)

    def run(self):
        logger.info('MPD Play')
        self.player.play()
        return True


class MPDPauseCommand(MPDCommand):
    def __init__(self, player):
        MPDCommand.__init__(self, player)

    def run(self):
        logger.info('MPD Pause')
        self.player.pause()
        return True


class MPDNextCommand(MPDCommand):
    def __init__(self, player):
        MPDCommand.__init__(self, player)

    def run(self):
        logger.info('MPD Next')
        self.player.next()
        return True
