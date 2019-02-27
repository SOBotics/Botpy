#
# ChatRoom.py
# Botpy
#
# Created by Ashish Ahuja on 12th September 2017.
#
#

import os
import pickle
import weakref
import logging

import chatexchange as ce

from . import ChatUser
from . import PrivilegeType
from . import Utilities


class ChatRoom(ce.rooms.Room):
    def __init__(self, room_id, client, save_directory=None):
        super().__init__(room_id, client)

        if save_directory is None:
            save_directory = os.getcwd()

        self._filename = save_directory + "room_" + str(self.id) + "_name_" + self.name.replace(" ", "_") + "_users"
        self._privilege_types = list()
        self._users = list()

        self._users.extend(self.get_pingable_users())

    def join(self):
        logging.info("Joined room '" + self.name + "' with room id " + str(self.id) + ".")
        return self._client._join_room(self.id)

    def leave(self):
        return self._client._leave_room(self.id)

    def add_privilege_type(self, privilege_level, privilege_name):
        self._privilege_types.append(PrivilegeType.PrivilegeType(privilege_level, privilege_name))

    def remove_privilege_type(self, privilege_name):
        for each_type in self._privilege_types:
            if each_type.name == privilege_name:
                self._privilege_types.remove(each_type)

    def is_user_privileged(self, user_id, required_level):
        for each_user in self._users:
            if each_user.id == user_id:
                return each_user.is_privileged(required_level)
        return False

    def get_max_privileges(self):
        """
        Returns the privilege type with maximum privileges.
        Return value is None if no privilege types exist.
        """
        max_privs = None
        for priv in self._privilege_types:
            if max_privs is None:
                max_privs = priv
            elif priv.level > max_privs.level:
                max_privs = priv

        return max_privs

    def get_privilege_type_by_level(self, privilege_level):
        for each_type in self._privilege_types:
            if each_type.level == privilege_level:
                return each_type

        return None

    def get_privilege_type_by_name(self, name):
        for each_type in self._privilege_types:
            if each_type.name == name:
                return each_type

        return None

    def get_users(self):
        return self._users

    def change_privilege_level(self, user_id, privilege_type=None):
        if not isinstance(privilege_type, PrivilegeType.PrivilegeType) and privilege_type is not None:
            raise TypeError('privilege_user: Expected privilege type of type "PrivilegeType.PrivilegeType"')
            return False

        for each_user in self._users:
            if each_user.id == user_id:
                each_user.change_privilege_level(privilege_type)
                return True
        return False

    def add_user(self, user):
        if not isinstance(user, ChatUser.ChatUser):
            raise TypeError('add_user: Expected user of type "ChatUser.ChatUser"')
            return

        for each_user in self._users:
             if each_user.id == user.id:
                return
        self._users.append(user)
