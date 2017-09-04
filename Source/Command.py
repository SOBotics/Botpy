#
# Command.py
# Botpy
#
# Created by Ashish Ahuja on 1st August 2017
#

import chatexchange as ce

class Command:
    def __init__(self, message, arguments, usageIndex=0):
        self.message = message
        self.arguments = arguments
        self.usageIndex = usageIndex

    def usage(self):
        raise NotImplementedError

    #Whether the command has completed execution.
    finished = False

    def reply(self, text, length_check=True):
        self.message.reply(text, length_check=length_check)
        
    def post(self, text, length_check=True):
        self.message.room.send_message(text, length_check=length_check)
        
    def run(self):
        raise NotImplementedError
