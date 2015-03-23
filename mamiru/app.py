#!/usr/bin/env python
#!-*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

from asyncore import file_dispatcher, loop
from evdev import InputDevice, categorize, ecodes
from importd import d
import thread
import sys

class InputDeviceDispatcher(file_dispatcher):
    def __init__(self, device):
        self.device = device
        file_dispatcher.__init__(self, device)

    def recv(self, ign=None):
        return self.device.read()

    def handle_read(self):
        for event in self.recv():
            print(repr(event))

d(
    DEBUG=True,
    INSTALLED_APPS=(
        # django library
        'django_nose',
    ),
    TEST_RUNNER='django_nose.NoseTestSuiteRunner'
 )


def run_device_input_thread():
    print("device input thread start")
    dev = InputDevice('/dev/input/event0')
    try:
        InputDeviceDispatcher(dev)
        loop()
    except KeyboardInterrupt:
        print("quit")

def run_web_server_thread():
    #print("web server thread start")
    d.main()
    #print("web server thread stop")

@d('/')
def hello(request):
    return d.HttpResponse('Hello world')

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        if sys.argv[1] in ('runserver',):
            thread.start_new_thread(run_device_input_thread, ())
    run_web_server_thread()
