#-*- coding: utf-8 -*-

import unittest
from mamiru.commands import mpd_commands as cmds

class MPDPlayerTest(unittest.TestCase):
    def test_create(self):
        player = cmds.MPDPlayer()
        self.assertIsNotNone(player)

    def test_open_without_mpd(self):
        player = cmds.MPDPlayer()
        player.open()

    def test_close_without_mpd(self):
        player = cmds.MPDPlayer()
        player.open()
        player.close()

    def test_call_mpd_client_func(self):
        player = cmds.MPDPlayer()
        self.assertIsNotNone(player.play)


class MPDCommandTest(unittest.TestCase):
    def test_run(self):
        player = cmds.MPDPlayer()

        cmd_cls_list = [
            cmds.MPDPlayCommand,
            cmds.MPDPauseCommand,
            cmds.MPDNextCommand
        ]
        for cmd_cls in cmd_cls_list:
            cmd = cmd_cls(player)
            cmd()
