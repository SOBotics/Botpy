#
# Chatcommunicate.py
# Botpy
#
# Created by Ashish Ahuja on 2nd August 2017.
#
#

import chatexchange as ce
import threading

class Chatcommunicate:
    def __init__(self, bot_name, command_manager):
        self.bot_name = bot_name
        self.command_manager = command_manager
        self.short_name = '@' + bot_name[:3]
   
    def handle_event(self, event, _):
        if isinstance(event, ce.events.MessagePosted):
            message = event

            try:
                print("(%s) %s (id: %d): %s" % (message.room.name, message.user.name, message.user.id, message.content))
            except UnicodeEncodeError as unicode_err:
                print("Unicode encode error occurred: " + str(unicode_err))

            try:
                content_split = message.content.lower().split()
            except AttributeError:
                print("Attribute error occurred.")
                return

            if content_split[0].startswith(self.short_name.lower()):
                self.command_manager.handle_command(message)
        elif isinstance(event, ce.events.UserEntered):
            # A user has entered the room.
