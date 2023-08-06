# This file is placed in the Public Domain.


"event"


import threading


from bot.obj import Object
from bot.hdl import Bus


def __dir__():
    return (
        "Event",
    )


class Event(Object):

    def __init__(self):
        super().__init__()
        self._ready = threading.Event()
        self.channel = ""
        self.exc = None
        self.orig = ""
        self.result = []
        self.thrs = []
        self.type = "event"

    def bot(self):
        return Bus.byorig(self.orig)

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result.append(txt)

    def show(self):
        assert self.orig
        for txt in self.result:
            Bus.say(self.orig, self.channel, txt)

    def wait(self):
        self._ready.wait()
        for thr in self.thrs:
            thr.join()
        return self.result


class Command(Event):

    def __init__(self):
        Event.__init__(self)
        self.type = "command"
