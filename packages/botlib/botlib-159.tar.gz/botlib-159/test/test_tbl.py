# This file is placed in the Public Domain.


"object programming tests"


import inspect
import os
import sys
import unittest


from bot.obj import Object, keys, values
from bot.hdl import Table


import bot.cmds


Table.add(bot.cmds)


class Test_Table(unittest.TestCase):

    def test_mod(self):
        self.assertTrue("bot.cmds" in keys(Table.mod))
