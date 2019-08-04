#
# Bot.py
# Botpy
#
# Created by Ashish Ahuja on 1st August 2017.
#
#

from .CommandManager import *
from .BackgroundTaskManager import *
from .BackgroundTask import *
from . import ChatRoom
from . import ChatUser
from . import Utilities

import os
import json
import jsonpickle as jp

class Bot(ce.client.Client):
    def __init__(self, bot_name, commands, room_ids, background_tasks=[], host='stackexchange.com', email=None, password=None):
        super().__init__(host, email, password)

        background_tasks.append(BackgroundTask(self._shutdown_check, interval=5))
        background_tasks.append(BackgroundTask(self._reboot_check, interval=5))
        background_tasks.append(BackgroundTask(self._save_users, interval=60))

        self.name = bot_name
        self.is_alive = False
        self._ids = room_ids
        self.commands = commands
        self._command_manager = CommandManager(commands)
        self.save_directory = os.path.expanduser("~") + "/" + "." + self.name.lower() + "/"
        self._users = list()
        self._rooms = list()
        
        background_tasks.append(BackgroundTask(self._command_manager.cleanup_finished_commands, interval=3))
        self._background_task_manager = BackgroundTaskManager(background_tasks)
 
    def join_rooms(self):
        for each_id in self._ids:
            #self._rooms.setdefault(each_id, self.get_room(each_id))
            self.get_room(each_id)

        for each_room in self._rooms:
            each_room.join()        

    def leave_rooms(self):
        for each_room in self._rooms:
            each_room.leave()

    def watch_rooms(self):
        for each_room in self._rooms:
            each_room.watch(self._handle_event)

    def add_privilege_type(self, privilege_level, privilege_name):
        for each_room in self._rooms:
            each_room.add_privilege_type(privilege_level, privilege_name)
    
    def start_bot(self):
        self.is_alive = True
        self.join_rooms()
        self._load_users()
        self.watch_rooms()
        self._background_task_manager.start_tasks()

    def stop_bot(self):
        self._background_task_manager.stop_tasks()
        self._save_users()
        self.leave_rooms()
        self.is_alive = False
    
    def _shutdown_check(self):
        if Utilities.should_shutdown:
            self.stop_bot()

    def _reboot_check(self):
        if Utilities.should_reboot:
            Utilities.should_reboot = False
            self.stop_bot()
            self.start_bot() 
            self.add_essential_background_tasks()

    def _handle_event(self, event, _):
        if isinstance(event, ce.events.MessagePosted):
            message = event
            short_name = '@' + self.name[:3]

            try:
                print("(%s) %s (id: %d): %s" % (message.room.name, message.user.name, message.user.id, message.content))
            except UnicodeEncodeError as unicode_err:
                print("Unicode encode error occurred: " + str(unicode_err))

            try:
                content_split = message.content.lower().split()
            except AttributeError:
                print("Attribute error occurred.")
                return

            if content_split[0].startswith(short_name.lower()):
                self._command_manager.handle_command(message)
        elif isinstance(event, ce.events.UserEntered):
            event.room.add_user(event.user)

    def _save_users(self):
        for room in self._rooms:
            filename = self._convert_to_save_filename(room.id)
            try:
                save_list = list()
                for user in room._users:
                    save_list.append({'id': user.id, '_privilege_type': user._privilege_type})
    
                with open(filename, "w") as file_handle:
                    json.dump(jp.encode(save_list), file_handle)
            except IOError as ioerr:
                print("IOError occurred: ")
                print(str(ioerr))
            except pickle.PickleError as perr:
                print("Pickling error occurred: ")
                print(str(perr))

    def _load_users(self):
        for room in self._rooms:
            filename = self._convert_to_save_filename(room.id)
            try:
                with open(filename, "r") as file_handle:
                    file_users = jp.decode(json.load(file_handle))
                    for user in file_users:
                        room._users = [x for x in room._users if x.id != user['id']]
                        #room._users.append(self._set_dict(ChatUser.ChatUser, user['id'], user))
                        room._users.append(self.get_user(user['id'], _privilege_type=user['_privilege_type']))
            except IOError as ioerr:
                print("IOError occurred: ")
                print(str(ioerr))
            except pickle.PickleError as perr:
                print("Pickling error occurred: ")
                print(str(perr)) 

    def _convert_to_save_filename(self, id):
        return self.name.replace(' ', '_') + '_room_' + str(id) + '_data'

    def get_room(self, room_id, **attrs_to_set):
        return self._get_and_set_deduplicated_list(
            ChatRoom.ChatRoom, room_id, self._rooms, attrs_to_set)

    def get_user(self, user_id, **attrs_to_set):
        return self._get_and_set_deduplicated_list(
            ChatUser.ChatUser, user_id, self._users, attrs_to_set)

    def _get_and_set_deduplicated_list(self, cls, id, instances, attrs):
        instance = None
        for each in instances:
            if each.id == id:
                instance = each
                break
        if instance is None:
            instance = cls(id, self)
            instances.append(instance)

        for key, value in attrs.items():
            setattr(instance, key, value)
        return instance

    def _set_dict(self, cls, id, attrs):
        instance = cls(id, self)
    
        for key, value in attrs.items():
            setattr(instance, key, value)

        return instance
