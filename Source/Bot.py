#
# Bot.py
# Botpy
#
# Created by Ashish Ahuja on 1st August 2017.
#
#

import chatexchange as ce
from Chatcommunicate import *
from CommandAlive import *
from CommandStop import *
from CommandListRunningCommands import *
from CommandManager import *
from BackgroundTaskManager import *
from BackgroundTask import *
from ChatRoom import *
from Utilities import *
import Utilities

class Bot:
    def __init__(self, bot_name, client, commands, room_ids, background_tasks=[], bot_link="https://example.com", github_link="https://github.com"):
        self.name = bot_name
        self.commands = commands
        self.client = client
        self.rooms = []
        self.room_ids = room_ids
        self.bot_link = bot_link
        self.github_link = github_link
        self.background_task_manager = BackgroundTaskManager(background_tasks)
        self.chatcommunicate = Chatcommunicate(bot_name, CommandManager(commands, self.rooms)) 

    def add_background_task(self, background_task, interval=30, restart=True):
        self.background_task_manager.add_background_task(background_task)
        if restart:
            self.background_task_manager.restart_tasks()

    def add_essential_background_tasks(self, restart=True):
        self.add_background_task(BackgroundTask(self.chatcommunicate.command_manager.cleanup_finished_commands, interval=3))
        self.add_background_task(BackgroundTask(self.shutdown_check, interval=5))

        self.background_task_manager.restart_tasks()

    def join_rooms(self, watch_callback):
        self.rooms[:] = []
        for each_id in self.room_ids:
            self.rooms.append(ChatRoom(self.client, each_id, watch_callback))

        for each_room in self.rooms:
            each_room.join_room()        

    def leave_rooms(self):
        for each_room in self.rooms:
            each_room.leave_room()

        self.rooms[:] = []

    def watch_rooms(self):
        for each_room in self.rooms:
            each_room.watch_room()

    def start_bot(self):
        self.join_rooms(self.chatcommunicate.handle_message)
        self.watch_rooms()
        self.background_task_manager.start_tasks()

    def stop_bot(self):
        self.background_task_manager.stop_tasks()
        self.leave_rooms()
    
    def shutdown_check(self):
        if Utilities.should_shutdown:
            self.stop_bot() 
