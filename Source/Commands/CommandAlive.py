#
# CommandAlive.py
# Botpy
#
# Created by Ashish Ahuja.
#
#

from .Command import *


class CommandAlive(Command):
    @staticmethod
    def usage():
        return ["alive", "status"]

    def run(self):
        self.reply("Yes")
