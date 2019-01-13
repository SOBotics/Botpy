#
# Command.py
# Botpy
#
# Created by Ashish Ahuja on 1st August 2017
#

import chatexchange as ce

class Command:
    def __init__(self, command_manager, message, arguments, usage_index=0):
        self.command_manager = command_manager
        self.message = message
        self.arguments = arguments
        self.usage_index = usage_index

    def usage():
        raise NotImplementedError("Function 'usage' must be implemented in the command.")

    def privileges(self):
        return 0

    #Whether the command has completed execution.
    finished = False

    def reply(self, text, length_check=True):
        self.message.message.reply(text, length_check=length_check)

    def post(self, text, length_check=True):
        self.message.room.send_message(text, length_check=length_check)

    def run(self):
        raise NotImplementedError("Function 'run' must be implemented in the command.")
