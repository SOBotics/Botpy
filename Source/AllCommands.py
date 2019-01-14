#
# AllCommands.py
# Botpy
#
# Created by Ashish Ahuja on 13th January 2019.
# Licensed under WTFPL.
#

from .Command import *
from . import Utilities

import tabulate
import re

class CommandAlive(Command):
    @staticmethod
    def usage():
        return ["alive", "status"]

    def run(self):
        self.reply("Yes")

class CommandAmiprivileged(Command):
    def usage():
        return ["amiprivileged", "doihaveprivs", "privileges"]

    def run(self):
        user_privs = self.message.user.get_privilege_type()
        if user_privs is None:
            self.reply("You do not have any privileges.")
        else:
            self.reply("You have the privilege: " + user_privs.name)

class CommandListPrivilegedUsers(Command):
    def usage():
        return ["membership", "privileged", "listprivileged"]

    def run(self):
        privilege_list = list()

        for each_user in self.message.room.get_users():
            if each_user.get_privilege_type() is not None:
                privilege_list.append([each_user.id, each_user.get_privilege_type().name])

        table = tabulate.tabulate(privilege_list, headers=["User ID", "Privilege level"], tablefmt="orgtbl")

        self.post("    " + table.replace("\n", "\n    "))

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

class CommandPrivilegeUser(Command):
    def usage():
        return ["privilege * *", "addpriv * *"]

    def privileges(self):
        return 0

    def run(self):
        user_id = int(self.arguments[0])
        privilege_name = self.arguments[1]

        privilege_type = self.message.room.get_privilege_type_by_name(privilege_name)

        if privilege_type == None:
            self.reply("Please give a valid privilege type")
            return

        if self.message.room.is_user_privileged(user_id, privilege_type.level):
            self.reply("The user specified already has the required privileges.")
            return

        self.message.room.change_privilege_level(user_id, privilege_type)
        self.reply("The user specified has been given the privileges.")

class CommandUnprivilegeUser(Command):
    @staticmethod
    def usage():
        return ["unprivilege *", "unprivilege user *", "remove privileges *"]

    def run(self):
        user_id = int(self.arguments[0])

        self.message.room.change_privilege_level(user_id)
        self.reply("The user specified has been stripped of all privileges.")

class CommandReboot(Command):
    @staticmethod
    def usage():
        return ['reboot', 'restart']

    def run(self):
        self.reply("Rebooting...")
        Utilities.StopReason.reboot = True

class CommandStop(Command):
    @staticmethod
    def usage():
        return ['stop', 'shutdown']

    def run(self):
        self.reply("Shutting down...")
        Utilities.StopReason.shutdown = True




