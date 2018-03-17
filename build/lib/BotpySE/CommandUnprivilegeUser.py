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
        return ["unprivilege *", "unprivilege user *", "remove privileges *"]

    def privileges(self):
        return 1

    def run(self):
        user_id = int(self.arguments[0])

        self.message.room.change_privilege_level(user_id)
        self.reply("The user specified has been stripped of all privileges.")
