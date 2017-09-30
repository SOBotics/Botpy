#
# CommandPrivilegeUser.py
# Botpy
#
# Created by Ashish Ahuja on 17th September 2017.
#
#

from .Command import *

class CommandPrivilegeUser(Command):
    def usage():
        return ["privilege * *", "addpriv * *"]

    def privileges(self):
        return 1

    def run(self):
        for each_room in self.command_manager.rooms:
            if self.message.room.id == each_room.room_id:
                command_room = each_room

        user_id = int(self.arguments[0])
        privilege_name = self.arguments[1]

        privilege_type = command_room.get_privilege_type_by_name(privilege_name)

        if privilege_type == None:
            self.reply("Please give a valid privilege type")
            return

        if command_room.is_user_privileged(user_id, privilege_type.level):
            self.reply("The user specified already has the required privileges.")
            return

        command_room.add_privileged_user(user_id, privilege_type)
        self.reply("The user specified has been given the privileges.")
