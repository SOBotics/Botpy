#
# Bot.py
# Botpy
#
# Created by Ashish Ahuja on 1st August 2017.
#
#

import chatexchange as ce
import Chatcommunicate

class Bot:
    def __init__(self, bot_name, client, room_ids, bot_link="https://example.com", github_link="https://github.com"):
        self.name = bot_name
        self.client = client
        self.rooms = []
        self.room_ids = room_ids
        self.bot_link = bot_link
        self.github_link = github_link
        self.chatcommunicate = Chatcommunicate.Chatcommunicate(bot_name, commands) 

    def join_rooms(self):
        for each_id in self.room_ids:
            self.rooms.append(self.client.get_room(each_id))

        for each_room in self.rooms:
            each_room.join()
            print("Joined room " + str(each_room.id) + ".")

    def leave_rooms(self):
        for each_room in self.rooms:
            each_room.leave()
            self.rooms.remove(each_room)

    def watch_rooms(self, function_callback):
        for each_room in self.rooms:
            each_room.watch(function_callback)     

    def start_bot(self):
        self.join_rooms()
        self.watch_rooms(self.chatcommunicate.handle_message)

    def stop_bot(self):
        self.leave_rooms() 
