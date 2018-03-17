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
        user_privs = self.message.user.get_privilege_type()
        if user_privs is None:
            self.reply("You do not have any privileges.")
        else:
            self.reply("You have the privilege: " + user_privs.name)
