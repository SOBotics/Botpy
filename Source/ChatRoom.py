#
# ChatRoom.py
# Botpy
#
# Created by Ashish Ahuja on 12th September 2017.
#
#

class ChatRoom:
    def __init__(self, client, room_id, function_callback):
        self.room_id = room_id
        self.client = client
        self.function_callback = function_callback

    def join_room(self):
        self.room = self.client.get_room(self.room_id)
        self.room.join()
        print("Joined room '" + self.room.name + "' with room id " + str(self.room_id) + ".")

    def leave_room(self):
        self.room.leave()

    def watch_room(self):
        self.room.watch(self.function_callback)

    def add
