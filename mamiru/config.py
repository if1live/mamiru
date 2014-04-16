#-*- coding: utf-8 -*-

from .commands import *
from evdev import ecodes

KEYLIST = {
    ecodes.KEY_Q: MPDPlayCommand,
    ecodes.KEY_W: MPDPauseCommand,
    ecodes.KEY_E: MPDNextCommand,
}
