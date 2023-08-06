# This file is placed in the Public Domain.


"callbacks"


from .obj import Object, get, register
from .thr import launch


def __dir__():
    return (
        "Callbacks",
    )


class Callbacks(Object):

    cbs = Object()
    errors = []
    threaded = True

    @staticmethod
    def add(name, cb):
        register(Callbacks.cbs, name, cb)

    @staticmethod
    def callback(e):
        f = Callbacks.get(e.type)
        if not f:
            e.ready()
            return
        try:
            f(e)
        except Exception as ex:
            Callbacks.errors.append(ex)
            e.exc = ex
            e.ready()

    @staticmethod
    def get(cmd):
        return get(Callbacks.cbs, cmd)


    @staticmethod
    def dispatch(e):
        if Callbacks.threaded:
            e.thrs.append(launch(Callbacks.callback, e, name=e.txt))
            return
        Callbacks.callback(e)
