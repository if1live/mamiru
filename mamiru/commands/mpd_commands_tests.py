#-*- coding: utf-8 -*-

import unittest
from mamiru.commands import mpd_commands as cmds



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
