#
# PrivilegedChatUser.py
# Botpy
#
# Created by Ashish Ahuja on 12th September 2017.
#
#

class PrivilegedChatUser:
    def __init__(self, user_id, room_id, privilege_type):
        self.user_id = user_id
        self.room_id = room_id
        self.level = privilege_type.level
        self.privilege_type = privilege_type
        self.block = False

    def block_user(self):
        self.block = True

    def unblock_user(self):
        self.block = False

    def is_privileged(self, privilege_required):
        if self.privilege_level >= privilege_required and not self.block:
            return True

        return False
