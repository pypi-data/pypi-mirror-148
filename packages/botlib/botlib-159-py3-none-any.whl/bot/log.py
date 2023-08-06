# This file is placed in the Public Domain.


"log text"


def __dir__():
    return (
        "log",
    )


from bot.obj import Class, Object, save
from bot.hdl import Commands


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""


Class.add(Log)


def log(event):
    if not event.rest:
        event.reply("log <txt>")
        return
    o = Log()
    o.txt = event.rest
    save(o)
    event.reply("ok")


Commands.add(log)
