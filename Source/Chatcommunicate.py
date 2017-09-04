#
# Chatcommunicate.py
# Botpy
#
# Created by Ashish Ahuja on 2nd August 2017.
#
#

import chatexchange as ce
from Command import *
import threading

class Chatcommunicate:
    def __init__(self, bot_name, commands):
        self.commands = commands
        self.bot_name = bot_name
        self.short_name = bot_name[:-(len(bot_name) - 4)]
        self.running_commands = []

    def run_command(self, command):
        command_thread = threading.Thread(target=command.run())
        running_commands.append([command, command_thread])
        command_thread.start()

    def handle_command(self, message):
        try:
            message_content = message.content.lower().split()
            del message_content[0]
        except AttributeError:
            return

        for command in self.commands:
            command_usage = command.usage()

            usage_index = 0

            for usage in command_usage:
                usage_index += 1
                usage_components = usage.split()
                args = []
                match = True
                last_index = min(len(usage_components), len(message_content))

                for i in range(last_index):
                    content_component = message_content[i]
                    usage_component = usage_components[i]
                
                    if usage_component == '*':
                        args.append(content_component)
                    elif usage_component == '...':
                        #Everything else is arguments
                        temp_index = i
                        while temp_index < len(message_content):
                            args.append(message_content[temp_index])
                            temp_index += 1
                    elif content_component != usage_component:
                        match = False

                    min_count = (len(usage_components) - 1) if (usage_components[-1] == '...') else len(usage_components)
                    if len(message_content) < min_count:
                        match = False

                    if match:
                        self.run_command(command(message, args, usage_index))

    def handle_message(self, message, _):
        if not isinstance(message, ce.events.MessagePosted):
            #Ignore non-message posted events
            return

        try:
            print("(%s) %s: %s" % (message.room.name, message.user.name, message.content)
        except UnicodeEncodeError as unicode_err:
            print("Unicode encode error occurred: " + str(unicode_err))

        try:
            content_split = message.content.lower().split()
        except AttributeError:
            return

        if content_split[0].startswith(self.short_name.lower())
            self.handle_command(message)
