# This file is placed in the Public Domain.


"object programming tests"


import inspect
import os
import sys
import unittest


from gcd.obj import Object, keys, values
from gcd.hdl import Table


import gcd.cmds


Table.add(gcd.cmds)


class Test_Table(unittest.TestCase):

    def test_mod(self):
        self.assertTrue("gcd.cmds" in keys(Table.mod))
