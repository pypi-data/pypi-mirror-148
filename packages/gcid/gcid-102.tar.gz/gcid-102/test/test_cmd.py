# This file is placed in the Public Domain.


"object programming tests"


import inspect
import unittest


from gcid.obj import Class, Config, Object, format, get, values
from gcid.cbs import Callbacks
from gcid.cmd import Commands, Command, dispatch
from gcid.evt import Event
from gcid.hdl import Handler
from gcid.shl import CLI
from gcid.tbl import Table
from gcid.thr import launch


events = []


param = Object()
param.add = ["test@shell", "bart", ""]
param.cfg = ["nick=opb", "server=localhost", ""]
param.dlt = ["root@shell"]
param.dne = ["test4", ""]
param.dpl = ["reddit title,summary,link"]
param.flt = ["0", ""]
param.fnd = ["cfg", "log", "rss", "cfg server==localhost", "rss rss==reddit"]
param.log = ["test1", ""]
param.met = ["root@shell"]
param.nck = ["opb"]
param.pwd = ["bart blabla"]
param.rem = ["reddit", ""]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.tdo = ["things todo"]


def getmain(name):
    m = __import__("__main__")
    return getattr(m, name, None)


c = getmain("c")
c.start()

def consume(events):
    fixed = []
    res = []
    for e in events:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            events.remove(f)
        except ValueError:
            continue
    return res


class Test_Commands(unittest.TestCase):


    def test_commands(self):
        cmds = sorted(Commands.cmd)
        for cmd in cmds:
            for ex in getattr(param, cmd, [""]):
                e = Command()
                e.txt = cmd + " " + ex
                e.orig = repr(c)
                c.put(e)
                events.append(e)
        consume(events)
        self.assertTrue(not events)
