#
# PrivilegeType.py
# Botpy
#
# Created by Ashish Ahuja on 12th September 2017.
#
#

class PrivilegeType:
    def __init__(self, privilege_level, privilege_name):
        self.level = privilege_level
        self.name = privilege_name

    def change_privilege_level(self, new_level):
        self.level = new_level
