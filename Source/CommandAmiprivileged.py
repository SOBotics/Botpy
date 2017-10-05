#
# CommandAmiprivileged.py
# Botpy
#
# Created by Ashish Ahuja on 29th September 2017.
# 
#

from .Command import *

class CommandAmiprivileged(Command):
    def usage():
        return ["amiprivileged", "doihaveprivs", "privileges"]

    def run(self):
        user_id = self.message.user.id

        for each_room in self.command_manager.rooms:
            if self.message.room.id == each_room.room_id:
                command_room = each_room

        user_privileges = list()

        for each_privilege_type in command_room.privilege_types:
            if command_room.is_user_privileged(user_id, each_privilege_type.level):
                user_privileges.append(each_privilege_type.name)

        if len(user_privileges) == 0:
            self.reply("You do not have any privileges.")
        else:
            self.reply("You have the privileges: " + ",".join(user_privileges) + ".")
