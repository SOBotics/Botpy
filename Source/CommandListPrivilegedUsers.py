#
# CommandListPrivilegedUsers.py
# Botpy
#
# Created by Ashish Ahuja on 1st October 2017.
#
#

from .Command import *
import tabulate

class CommandListPrivilegedUsers(Command):
    def usage():
        return ["membership", "privileged", "listprivileged"]

    def run(self):
        for each_room in self.command_manager.rooms:
            if self.message.room.id == each_room.room_id:
                command_room = each_room
        
        privilege_list = list()

        for each_user in command_room.privileged_users:
            if each_user.room_id == message.room.id:
                privilege_list.append([each_user.user_id, each_user.privilege_type.name])

        table = tabulate.tabulate(privilege_list, headers=["User ID", "Privilege level"], tablefmt="orgtbl")

        self.post("    " + table.replace("\n", "\n    "))
