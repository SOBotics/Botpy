#
# BackgroundTask.py
# Botpy
#
# Created by Ashish Ahuja on 4th September 2017.
#
#

import threading


class BackgroundTask:
    def __init__(self, function_callback, interval=30):
        self.function_callback = function_callback
        self.interval = interval
        self.stop_event = threading.Event()

    def call_function(self):
        while not self.stop_event.wait(self.interval):
            self.function_callback()

    def start_task(self):
        self.stop_event.clear()
        background_thread = threading.Thread(target=self.call_function)
        background_thread.start()

    def stop_task(self):
        self.stop_event.set()

    def is_alive(self):
        return not self.stop_event.is_set()
