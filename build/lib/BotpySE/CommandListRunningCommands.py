#
# CommandListRunningCommands.py
# Botpy
#
# Created by Ashish Ahuja on 6th September 2017.
#
#

from .Command import *
import tabulate
import re

class CommandListRunningCommands(Command):
    @staticmethod
    def usage():
        return ["running commands", "rc"]

    def run(self):
        command_list = list()

        for each_command, _ in self.command_manager.running_commands:
            command_list.append([each_command.message.user.name, each_command.usage()[each_command.usage_index]])

        table = tabulate.tabulate(command_list, headers=["User", "Command"], tablefmt="orgtbl")

        self.post("    " + re.sub('\n', '\n    ', table)) 
