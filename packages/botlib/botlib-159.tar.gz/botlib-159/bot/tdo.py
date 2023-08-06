# This file is placed in the Public Domain.


"todo items"


import time


from bot.obj import Class, Object, find, fntime, save
from bot.hdl import Commands


def __dir__():
    return (
        "Todo",
        "todo"
    )


class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""


Class.add(Todo)


def todo(event):
    if not event.rest:
        nr = 0
        for fn, o in find("todo"):
            event.reply("%s %s %s" % (nr, o.txt, elapsed(time.time() - fntime(fn))))
        return
    o = Todo()
    o.txt = event.rest
    save(o)
    event.reply("ok")


Commands.add(todo)
