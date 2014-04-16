#-*- coding: utf-8 -*-

from .loggers import create_logger
from .mpd_player import MPDPlayer

mpd_player = MPDPlayer()
mpd_player.open()

logger = create_logger('mamiru')



