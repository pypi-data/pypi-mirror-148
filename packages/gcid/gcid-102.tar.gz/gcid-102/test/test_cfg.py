# This file is placed in the Public Domain.


"config tests"


import os
import sys
import unittest


from gcid.obj import Object, edit, update
from gcid.prs import parse


class Cfg(Object):

    pass


class Test_Cfg(unittest.TestCase):

    def test_parse(self):
        p = Cfg()
        parse(p, "mod=irc")
        self.assertEqual(p.prs.sets.mod, "irc")

    def test_parse2(self):
        p = Cfg()
        parse(p, "mod=irc,rss")
        self.assertEqual(p.prs.sets.mod, "irc,rss")

    def test_edit(self):
        d = Object()
        update(d, {"mod": "irc,rss"})
        edit(Cfg, d)
        self.assertEqual(Cfg.mod, "irc,rss")
