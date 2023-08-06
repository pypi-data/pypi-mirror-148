# This file is placed in the Public Domain.


"shell"


from .bus import Bus
from .cmd import Command
from .hdl import Handler


def __dir__():
    return (
        "CLI",
        "Shell",
        "cmd"
    )


class CLI(Handler):

    def cmd(self, txt):
        e = Command()
        e.orig = repr(self)
        e.txt = txt
        self.handle(e)

    def raw(self, txt):
        pass


class Shell(CLI):

    def announce(self, txt):
        pass

    def handle(self, e):
        Handler.handle(self, e)
        e.wait()

    def poll(self):
        e = Command()
        e.txt = input("> ")
        e.orig = repr(self)
        return e


def cmd(clt, txt):
    if not txt:
        return False
    Bus.add(clt)
    e = Command()
    e.channel = ""
    e.orig = repr(clt)
    e.txt = txt
    clt.handle(e)
    e.wait()
    return e.result
