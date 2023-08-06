# This file is placed in the Public Domain.


"commands"


from .obj import Object, get, register
from .evt import Event
from .prs import parse


class Commands(Object):

    cmd = Object()

    @staticmethod
    def add(command):
        register(Commands.cmd, command.__name__, command)

    @staticmethod
    def get(command):
        f =  get(Commands.cmd, command)
        return f


class Command(Event):

    def __init__(self):
        Event.__init__(self)
        self.type = "command"


def dispatch(e):
    parse(e, e.txt)
    f = Commands.get(e.cmd)
    if f:
        f(e)
        e.show()
    e.ready()
