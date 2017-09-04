from Command import *

class CommandAlive(Command):
    def usage():
        return ["alive", "status"]

    def run(self):
        self.reply("Yes")
