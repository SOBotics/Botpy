#
# CommandListPrivilegedUsers.py
# Botpy
#
# Created by Ashish Ahuja on 1st October 2017.
#
#

import tabulate

from .Command import *


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
