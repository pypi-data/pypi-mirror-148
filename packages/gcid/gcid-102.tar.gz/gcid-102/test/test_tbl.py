# This file is placed in the Public Domain.


"object programming tests"


import inspect
import os
import sys
import unittest


from gcid.obj import Object, keys, values
from gcid.tbl import Table


import gcid


Table.add(gcid)


class Test_Table(unittest.TestCase):

    def test_mod(self):
        self.assertTrue("gcid" in keys(Table.mod))
