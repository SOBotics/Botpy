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
