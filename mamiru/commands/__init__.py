#-*- coding: utf-8 -*-

from .mpd_commands import (
    MPDPlayCommand,
    MPDPauseCommand,
    MPDNextCommand,
)
from .mpd_commands import MPDPlayer

class CommandFactory(object):
    MPD_CLS_LIST = (
        MPDPlayCommand,
        MPDPauseCommand,
        MPDNextCommand,
    )

    def __init__(self, mpd_player):
        self.mpd_player = mpd_player

    def create_cmd(self, cmd_cls):
        if cmd_cls in MPD_CLS_LIST:
            return cmd_cls(self.mpd_player)
        else:
            return cmd_cls()
