#
# Redunda.py
# Botpy
#
# Created by Ashish Ahuja on 18th March 2018.
#
#

import urllib
import logging

import pyRedunda


class RedundaManager:
    def __init__(self, redunda_obj):
        if not isinstance(redunda_obj, pyRedunda.Redunda):
            raise TypeError('RedundaManager.__init__: "redunda_obj" should be an instance of pyRedunda.Redunda')
        self._redunda = redunda_obj
        self._standby_callback = lambda: None
        self._standby_exit_callback = lambda: None
        self._new_event_callback = None
        self._location = None
        self._standby_status = False

        try:
            self._redunda.downloadFiles()
        except urllib.error.HTTPError as httperror:
            logging.error(str(httperror))
            logging.info('The file probably does not exist in Redunda storage.')

        logging.info("RedundaManager initialised.")

    def update(self):
        """
        Sends a status ping, downloads files, checks for standby status, gets events, and calls
        appropriate callbacks.
        """
        self._redunda.sendStatusPing()
        self._location = self.location()

        if (self.standby_status()) and (not self._standby_status):
            self._standby_status = True
            self._standby_callback()
        elif (not self.standby_status()) and (self._standby_status):
            self._standby_status = False
            self._redunda.downloadFiles()
            self._standby_exit_callback()

        if (self.event_count() > 0) and (self._new_event_callback is not None):
            self._new_event_callback(self.events())

        if not self._standby_status:
            self._redunda.uploadFiles()

    def set_standby_callback(self, new_callback):
        """
        Sets a callback which will be called if Redunda instructs the bot to be at standby.
        """
        if not callable(new_callback):
            raise TypeError('RedundaManager.set_standby_callback: "new_callback" should be callable!')
        self._standby_callback = new_callback

    def set_standby_exit_callback(self, new_exit_callback):
        """
        Sets a callback which will be called when the instance exits standby status.
        """
        if not callable(new_exit_callback):
            raise TypeError('RedundaManager.set_standby_exit_callback: "new_exit_callback" should be callable!')
        self._standby_exit_callback = new_exit_callback

    def set_new_event_callback(self, event_callback):
        """
        Sets a callback which will be called when a new event is received.
        """
        if not callable(event_callback):
            raise TypeError('RedundaManager.set_new_event_callback: "event_callback" should be callable!')
        self._new_event_callback = event_callback

    def location(self):
        """
        Returns the specified location of the instance on Redunda.
        """
        return self._redunda.location

    def standby_status(self):
        """
        Returns true if current instance should be at standby.
        """
        return self._redunda.shouldStandby

    def event_count(self):
        """
        Returns the number of unread events.
        """
        return self._redunda.eventCount

    def events(self):
        """
        Returns all unread events.
        """
        return self._redunda.getEvents()


