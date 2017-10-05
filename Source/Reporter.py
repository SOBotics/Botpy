#
# Reporter.py
# Botpy
#
# Created by Ashish Ahuja on 5th October 2017.
#
#

class Reporter:
    def __init__(self, bot_name, error_rooms, report_rooms, bot_link):
        self.bot_name = bot_name
        self.error_rooms = error_rooms
        self.report_rooms = report_rooms
        self.bot_link = bot_link

    def get_start_link(self):
        return "\[ [" + self.bot_name + "](" + self.bot_link + ") ]"

    def report(self, message, error_rooms=False):
        for each_room in self.report_rooms:
            each_room.send_message(get_start_link
