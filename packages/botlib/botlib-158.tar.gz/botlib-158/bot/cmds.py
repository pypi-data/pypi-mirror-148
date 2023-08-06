# This file is placed in the Public Domain.


"commands"


import threading
import time


from bot.hdl import Bus, Commands
from bot.obj import Class, Object, get, keys, update
from bot.obj import Config, find, save
from bot.obj import edit, format
from bot.obj import Db, fntime
from bot.thr import getname


def __dir__():
    return (
        "cmd",
        "flt",
        "fnd",
        "thr",
    )


starttime = time.time()


def cmd(event):
    event.reply(",".join((sorted(keys(Commands.cmd)))))


Commands.add(cmd)


def flt(event):
    try:
        index = int(event.args[0])
        event.reply(Bus.objs[index])
        return
    except (KeyError, TypeError, IndexError, ValueError):
        pass
    event.reply(" | ".join([getname(o) for o in Bus.objs]))


Commands.add(flt)


def fnd(event):
    if not event.args:
        db = Db()
        res = ",".join(
            sorted({x.split(".")[-1].lower() for x in db.types()}))
        if res:
            event.reply(res)
        else:
            event.reply("no types yet.")
        return
    otype = event.args[0]
    nr = -1
    got = False
    for fn, o in find(otype):
        nr += 1
        txt = "%s %s" % (str(nr), format(o))
        got = True
        event.reply(txt)
    if not got:
        event.reply("no result")


Commands.add(fnd)


def thr(event):
    result = []
    for t in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(t).startswith("<_"):
            continue
        o = Object()
        update(o, vars(t))
        if get(o, "sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        result.append((up, t.getName()))
    res = []
    for up, txt in sorted(result, key=lambda x: x[0]):
        res.append("%s(%ss)" % (txt, up))
    if res:
        event.reply(" ".join(res))


Commands.add(thr)
