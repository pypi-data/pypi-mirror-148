# This file is placed in the Public Domain.


"handler"


import threading


from .bus import Bus
from .cbs import Callbacks
from .que import Queued
from .thr import launch



def __dir__():
    return (
        "Handler",
    )


class Handler(Queued):

    errors = []

    def __init__(self):
        Queued.__init__(self)
        self.stopped = threading.Event()
        self.threaded = True

    def announce(self, txt):
        self.raw(txt)

    def handle(self, e):
        Callbacks.dispatch(e)

    def loop(self):
        while not self.stopped.isSet():
            self.handle(self.poll())

    def poll(self):
        return self.queue.get()

    def raw(self, txt):
        raise NotImplementedError

    def register(self, typ, cb):
        Callbacks.add(typ, cb)

    def restart(self):
        self.stop()
        self.start()

    def say(self, channel, txt):
        self.raw(txt)

    def start(self):
        Bus.add(self)
        self.stopped.clear()
        launch(self.loop)

    def stop(self):
        self.stopped.set()
