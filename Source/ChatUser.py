#
# ChatUser.py
# Botpy
#
# Created by Ashish Ahuja on 7th March 2018.
#
#

import chatexchange as ce

from . import PrivilegeType


class ChatUser(ce.users.User):
    def __init__(self, id, client, privilege_type=None):
        super().__init__(id, client)
        self._privilege_type = privilege_type

    def is_privileged(self, privilege_req):
        if self._privilege_type:
            if self._privilege_type.level >= privilege_req:
                return True
        return False

    def change_privilege_level(self, privilege_level):
        if not isinstance(privilege_level, PrivilegeType.PrivilegeType) and privilege_level is not None:
            raise TypeError('ChatUser.change_privilege_level: privilege_level is not of type "PrivilegeType.PrivilegeType"')

        self._privilege_type = privilege_level

    def get_privilege_type(self):
        return self._privilege_type
