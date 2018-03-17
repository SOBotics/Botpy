#
# Client.py
# Botpy
#
# Created by Ashish Ahuja on 7th March 2018.
#
#

import chatexchange as ce

from . import ChatRoom
from . import ChatUser

class Client(ce.client.Client):
    def __init__(self, host='stackexchange.com', email=None, password=None):
        super().__init__(host, email, password)

    def get_room(self, room_id, **attrs_to_set):
        return self._get_and_set_deduplicated(
            ChatRoom.ChatRoom, room_id, self._rooms, attrs_to_set)

    def get_user(self, user_id, **attrs_to_set):
        return self._get_and_set_deduplicated(
            ChatUser.ChatUser, user_id, self._users, attrs_to_set)
