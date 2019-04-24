#
# Bot.py
# Botpy
#
# Created by Ashish Ahuja on 1st August 2017.
#
#

import os
import sys
import json
import logging

import jsonpickle as jp
import pyRedunda as redunda

from .CommandManager import *
from .BackgroundTaskManager import *
from .BackgroundTask import *
from . import ChatRoom
from . import ChatUser
from . import Utilities
from . import Redunda


class Bot(ce.client.Client):
    def __init__(self, bot_name, commands, room_ids, background_tasks=[], host='stackexchange.com', email=None, password=None, send_aggressively=False):
        super().__init__(host, email, password, send_aggressively=send_aggressively)

        background_tasks.append(BackgroundTask(self._stop_reason_check, interval=5))
        background_tasks.append(BackgroundTask(self._save_users, interval=60))

        self.name = bot_name
        self.aliases = []
        self.is_alive = False
        self.at_standby = False
        self._ids = room_ids
        self.commands = commands
        self._command_manager = CommandManager(commands)
        self._users = list()
        self._rooms = list()
        self._storage_prefix = os.path.expanduser("~") + "/." + self.name.lower() + "/"
        self._version = None
        self._location = "unknown location"
        self._startup_message = self.name + " starting..."
        self._standby_message = "Switching to standby mode."
        self._failover_message = "Failover received."
        self._on_event_callback = lambda event: None

        background_tasks.append(BackgroundTask(self._command_manager.cleanup_finished_commands, interval=3))
        self._background_task_manager = BackgroundTaskManager(background_tasks)

        # Redunda storage
        self._redunda = None
        self._redunda_key = None
        self._sync_files = list()
        self._using_redunda = False
        self._redunda_task_manager = None

        try:
            with open(self._storage_prefix + 'location.txt', 'r') as file_handle:
                content = [x.rstrip('\n') for x in file_handle.readlines()]
            if len(content) != 2:
                raise ValueError('Invalid format in "location.txt"')
            self._location = content[0] + "/" + content[1]
            logging.info(self._location)
        except IOError as ioerr:
            logging.error(str(ioerr))
            logging.info('"location.txt" probably does not exist at: ' + self._storage_prefix)
        except ValueError as value_error:
            logging.error(str(value_error))

    def add_event_callback(self, event_callback):
        """
        'event_callback' will now be called everytime a new event occurs in a room which the bot 
            is present in.
        """
        if not callable(event_callback):
            raise TypeError('Bot.add_event_callback: \'event_callback\' is not callable!')
        self._on_event_callback = event_callback

    def add_alias(self, alias):
        """
        Adds a new name alias for the bot.
        """
        if not isinstance(alias, str):
            raise TypeError('Bot.add_alias: "alias" can only be of type str!')
        self.aliases.append(alias)

    def set_startup_message(self, message):
        """
        Sets a startup message to be posted when the bot starts.
        """
        if not isinstance(message, str):
            raise TypeError('Bot.set_startup_message: "message" should be of type str!')
        self._startup_message = message

    def set_standby_message(self, message):
        """
        Sets a message posted across all rooms when the bot switches to standby.
        """
        if not isinstance(message, str):
            raise TypeError('Bot.set_standby_message: "message" should be of type str!')
        self._standby_message = message

    def set_failover_message(self, message):
        """
        Sets a message posted across all rooms when the bot exits standby (failover).
        """
        if not isinstance(message, str):
            raise TypeError('Bot.set_failover_message: "message" should be of type str!')
        self._failover_message = message

    def set_room_owner_privs_max(self, ids=[]):
        """
        Sets room owner privileges to maximum in all rooms.

        Keyword arguments:
        ids -- Sets maximum privs for only these rooms if specified.
        """

        room_ids = list()
        if len(ids) > 0:
            if not all(isinstance(x, int) for x in ids):
                raise TypeError('Bot.set_room_owner_privs_max: Argument "ids" should only consist Integers.')
            room_ids = ids
        else:
            room_ids = self._ids

        for id in room_ids:
            room = self.get_room(id)
            max_privs = room.get_max_privileges()
            for user in room.owners:
                if max_privs is not None:
                    user.change_privilege_level(max_privs)

    def set_storage_prefix(self, new_prefix):
        """
        Sets a new path for the bot's data files to be stored.
        """
        self._storage_prefix = new_prefix

        try:
            with open(self._storage_prefix + 'location.txt', 'r') as file_handle:
                content = [x.rstrip('\n') for x in file_handle.readlines()]
            if len(content) != 2:
                raise ValueError('Invalid format in "location.txt"')
            self._location = content[0] + "/" + content[1]
        except IOError as ioerr:
            logging.error(str(ioerr))
            logging.info('"location.txt" probably does not exist at: ' + self._storage_prefix)
        except ValueError as value_error:
            logging.error(str(value_error))

    def set_bot_version(self, bot_version):
        """
        Sets a new bot version. Argument should be of type str.
        """
        if not isinstance(bot_version, str):
            raise TypeError('Bot.set_botversion: "bot_version" argument must be of type str!')
        self._version = bot_version

    def set_bot_location(self, new_location):
        """
        Sets a new location.
        """
        self._location = new_location

    def set_redunda_key(self, key):
        """
        Sets Redunda key necessary to use Redunda.
        """
        if not isinstance(key, str):
            raise TypeError('Bot.set_redundakey: "key" is not of type str!')
        self._redunda_key = key

    def add_file_to_sync(self, new_file_dict):
        """
        Adds a new file to sync; must be in sync file format supported by pyRedunda.
        """
        if not isinstance(new_file_dict, dict):
            raise TypeError('Bot.add_file_to_sync: "new_file_dict" must be of type dict')
        self._sync_files.append(new_file_dict)

    def redunda_init(self, file_sync=True, bot_version=None):
        """
        Initializes the self._redunda object for further use.

        Keyword arguments:
        file_sync -- specifies whether data files should be synced with Redunda (default: True).
        bot_version -- specifies the version to be sent to Redunda (default: self._version)

        Returns True on success.
        """
        if bot_version is None:
            bot_version = self._version

        if not isinstance(bot_version, str):
            raise TypeError('Bot.redunda_init: "bot_version" is not of type str!')
        if not isinstance(self._redunda_key, str):
            raise TypeError('Bot.redunda_init: "self._redunda_key" is not of type str!')

        if (self._redunda_key is None) or (bot_version is None):
            return False

        if file_sync:
            if not isinstance(self._sync_files, list):
                raise TypeError('Bot.redunda_init: "self._sync_files" is not a list!')
            for id in self._ids:
                self._sync_files.append({"name": self._convert_to_save_filename(id), "ispickle": False, "at_home": False})
        self._redunda = Redunda.RedundaManager(redunda.Redunda(self._redunda_key, self._sync_files, bot_version))
        self._redunda_task_manager = BackgroundTaskManager([BackgroundTask(self._redunda.update, interval=60)])

        return True

    def set_redunda_status(self, status):
        """
        Changes redunda status. If True, Redunda will now be actively used.

        Keyword arguments:
        status -- type Bool.

        Returns True on success.
        """
        if type(status) is not bool:
            raise TypeError('Bot.set_redunda_status: "status" is not of type bool!')
        if self._redunda is None and self._redunda_task_manager is None:
            return False
        self._using_redunda = status

        if self._using_redunda:
            self._redunda_task_manager.start_tasks()
            self._redunda.update()
            self.set_bot_location(self._redunda.location())
        elif not self._using_redunda:
            self._redunda_task_manager.stop_tasks()

    def set_redunda_standby_callback(self, callback):
        if self._redunda is None and self._redunda_task_manager is None:
            return
        self._redunda.set_standby_callback(callback)

    def set_redunda_standby_exit_callback(self, callback):
        if self._redunda is None and self._redunda_task_manager is None:
            return
        self._redunda.set_standby_exit_callback(callback)

    def set_new_event_callback(self, callback):
        if self._redunda is None and self._redunda_task_manager is None:
            return
        self._redunda.set_new_event_callback(callback)

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

    def post_global_message(self, message):
        """
        Posts the argument message across all rooms the bot is in.
        """
        for id in self._ids:
            room = self.get_room(id)
            room.send_message(message)

    def add_privilege_type(self, privilege_level, privilege_name):
        for each_room in self._rooms:
            each_room.add_privilege_type(privilege_level, privilege_name)

    def start(self):
        """
        Starts the bot.
        """
        self.is_alive = True
        self.join_rooms()
        self._load_users()
        self.watch_rooms()
        self._background_task_manager.start_tasks()

        self.post_global_message(self._startup_message)

        logging.info(self.name + " started.")

    def standby(self):
        """
        Puts the bot to standby. The bot does not respond to chat messages and shuts down all background tasks.
        """
        if not self.at_standby:
            self._background_task_manager.stop_tasks()
            self.at_standby = True

    def failover(self):
        """
        Undoes a standby; restarts all background tasks and normal functions.
        """
        if self.at_standby:
            self._background_task_manager.start_tasks()
            self.at_standby = False

    def set_redunda_default_callbacks(self):
        if self._redunda is None and self._redunda_task_manager is None:
            return
        self.set_redunda_standby_callback(self.standby)
        self.set_redunda_standby_exit_callback(self.failover)

    def stop(self):
        """
        Stops the bot. Automatically called when Utilities.should_shutdown is set to True.
        """
        self._background_task_manager.stop_tasks()

        if self._redunda_task_manager is not None:
            self._redunda_task_manager.stop_tasks()

        self._save_users()
        self.leave_rooms()

        logging.info(self.name + " stopping...")
        self.is_alive = False

    def reboot(self):
        """
        Reboots the bot. Automatically called when Utilities.StopReason.reboot = True.
        """
        #Reboot the bot by running it again. https://stackoverflow.com/a/30247200/4688119
        self.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def _stop_reason_check(self):
        stop_reason = Utilities.StopReason
        if stop_reason.reboot:
            self.reboot()
        elif stop_reason.shutdown:
            self.stop()

    def _handle_event(self, event, _):
        if isinstance(event, ce.events.MessagePosted):
            message = event
            short_name = '@' + self.name[:3]

            try:
                logging.info("(%s) %s (user id: %d): %s" % (message.room.name, message.user.name, message.user.id, message.content))
            except UnicodeEncodeError as unicode_err:
                logging.error("Unicode encode error occurred: " + str(unicode_err))

            try:
                content_split = message.content.lower().split()
            except AttributeError:
                logging.error("Attribute error occurred.")
                return

            if content_split[0].startswith(short_name.lower()):
                self._command_manager.handle_command(message)
            else:
                for each in self.aliases:
                    each  = '@' + each[:3]
                    if content_split[0].startswith(each.lower()):
                        self._command_manager.handle_command(message)
        elif isinstance(event, ce.events.UserEntered):
            logging.info("(%s) %s (user id: %d) entered the room" % (event.room.name, event.user.name, event.user.id))
            event.room.add_user(event.user)

        # Call event callback
        self._on_event_callback(event)

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
                logging.error("IOError occurred: ")
                logging.error(str(ioerr))
            except pickle.PickleError as perr:
                logging.error("Pickling error occurred: ")
                logging.error(str(perr))

    def _load_users(self):
        for room in self._rooms:
            filename = self._convert_to_save_filename(room.id)
            try:
                with open(filename, "r") as file_handle:
                    file_users = jp.decode(json.load(file_handle))
                    for user in file_users:
                        room._users = [x for x in room._users if x.id != user['id']]
                        room._users.append(self.get_user(user['id'], _privilege_type=user['_privilege_type']))
            except IOError as ioerr:
                logging.error("IOError occurred: ")
                logging.error(str(ioerr))
            except pickle.PickleError as perr:
                logging.error("Pickling error occurred: ")
                logging.error(str(perr))

    def _convert_to_save_filename(self, id):
        return self._storage_prefix + self.name.replace(' ', '_') + '_room_' + str(id) + '_data'

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
