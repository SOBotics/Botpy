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
     
