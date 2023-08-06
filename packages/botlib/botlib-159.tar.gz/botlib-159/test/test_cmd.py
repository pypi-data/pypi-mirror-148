# This file is placed in the Public Domain.


"command tests"


import inspect
import random
import unittest


from bot.evt import Command, Event
from bot.hdl import Callbacks, Commands, Handler, Table, dispatch
from bot.obj import Config, Object, get, keys, values
from bot.thr import launch


events = []
cmds = "commands,delete,display,fetch,find,fleet,log,meet,more,remove,rss,threads,todo"


param = Object()
param.commands = [""]
param.config = ["nick=opbot", "server=localhost", "port=6699"]
param.display = ["reddit title,summary,link", ""]
param.fetch = [""]
param.find = ["log", "log txt==test", "rss", "rss rss==reddit", "config server==localhost"]
param.fleet = ["0", ""]
param.log = ["test1", "test2"]
param.meet = ["root@shell", "test@user"]
param.more = [""]
param.nick = ["opb", "opbot", "op_"]
param.password = ["bart blabla"]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.todo = ["things todo"]


class CLI(Handler):

     def __init__(self):
         Handler.__init__(self)

     def raw(self, txt):
         if Config.verbose:
             print(txt)
        
         
c = CLI()
c.threaded = True
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
        random.shuffle(cmds)
        for cmd in cmds:
            for ex in get(param, cmd, [""]):
                e = Event()
                e.txt = cmd + " " + ex
                e.orig = repr(c)
                Callbacks.callback(e)
                events.append(e)
        #consume(events)
        #self.assertTrue(not events)
