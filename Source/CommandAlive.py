from Command import *

class CommandAlive(Command):
    def usage(self):
        return ["alive", "status"]

    def run(self):
        reply("Yes")
