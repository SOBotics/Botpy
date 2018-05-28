#
# Reporter.py
# Botpy
#
# Created by Ashish Ahuja on 5th October 2017.
#
#

import logging


class Reporter:
    def __init__(self, bot_name, error_rooms, report_rooms, bot_link):
        self.bot_name = bot_name
        self.error_rooms = error_rooms
        self.report_rooms = report_rooms
        self.bot_link = bot_link
        self.reports = list()
        self.pending_reports = list()

    def get_start_link(self):
        return "\[ [" + self.bot_name + "](" + self.bot_link + ") ]"

    def report(self, message, error_rooms=False):
        room_list = self.report_rooms

        if error_rooms:
            room_list.extend(self.error_rooms)

        for each_room in room_list:
            report = Report(self.get_start_link() + ' ' + message, each_room)
            report.report()
            self.reports.append(report)
            self.pending_reports.append(report)

    def check_message_for_report(self, message):
        logging.info(message)
        logging.debug('yo')
        if message.startswith(' &#91; <a href="'):
            logging.debug('bingo')

            for each_report in self.pending_reports:
                logging.debug('in')
                if message.room.id == each_report.room.id:
                    logging.debug('woohoo')
                    each_report.message_id = message.id
                    self.pending_reports.remove(each_report)
                    break

            return True
        return False

class Report:
    def __init__(self, message, room):
        self.message = message
        self.room = room
        self.message_id = -1

    def report(self):
        self.room.send_message(self.message)
