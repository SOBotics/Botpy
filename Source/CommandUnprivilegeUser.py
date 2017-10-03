#
# CommandUnprivilegeUser.py
# Botpy
#
# Created by Ashish Ahuja on 28th September 2017.
#
#

from .Command import *

class CommandUnprivilegeUser(Command):
    @staticmethod
    def usage():
        return ["unprivilege * *", "unprivilege user * *", "remove privileges * *"]

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

        command_room.remove_privileged_user(user_id, privilege_type)
        self.reply("The user specified has been removed from the privileges specified.")
