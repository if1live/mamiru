#-*- coding: utf-8 -*-

from mamiru.loggers import create_logger
import mpd
import socket


logger = create_logger('MPD')

class MPDPlayer(object):
    def __init__(self):
        self.client = mpd.MPDClient()
        self.client.timeout = 10
        self.client.idletimeout = None

    def open(self):
        try:
            self.client.connect('localhost', 6600)
            logger.info('open MPD')
            return True
        except socket.error:
            return False

    def close(self):
        try:
            self.client.close()
            self.client.disconnect()
            logger.info('close MPD')
            return True
        except AttributeError:
            return False
        except TypeError:
            return False
        except mpd.ConnectionError:
            return False

    def __del__(self):
        self.close()

    def __getattr__(self, key):
        return getattr(self.client, key)
