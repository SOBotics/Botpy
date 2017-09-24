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
   
    def handle_message(self, message, _):
        if not isinstance(message, ce.events.MessagePosted):
            #Ignore non-message posted events
            return

        try:
            print("(%s) %s: %s" % (message.room.name, message.user.name, message.content))
        except UnicodeEncodeError as unicode_err:
            print("Unicode encode error occurred: " + str(unicode_err))

        try:
            content_split = message.content.lower().split()
        except AttributeError:
            print("Attribute error occurred.")
            return

        if content_split[0].startswith(self.short_name.lower()):
            self.command_manager.handle_command(message)
