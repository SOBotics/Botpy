#
# CommandReboot.py
# Botpy
#
# Created by Ashish Ahuja on 5th October 2017.
#
#

from .Command import *
from . import Utilities


class CommandReboot(Command):
    @staticmethod
    def usage():
        return ['reboot', 'restart']

    def run(self):
        self.reply("Rebooting...")
        Utilities.StopReason.reboot = True
