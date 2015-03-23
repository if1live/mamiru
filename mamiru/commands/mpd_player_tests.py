#-*- coding: utf-8 -*-

import unittest
from mamiru.mpd_player import MPDPlayer

class MPDPlayerTest(unittest.TestCase):
    def test_create(self):
        player = MPDPlayer()
        self.assertIsNotNone(player)

    def test_open_without_mpd(self):
        player = MPDPlayer()
        player.open()

    def test_close_without_mpd(self):
        player = MPDPlayer()
        player.open()
        player.close()

    def test_call_mpd_client_func(self):
        player = MPDPlayer()
        self.assertIsNotNone(player.play)
