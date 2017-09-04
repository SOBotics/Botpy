#
# BackgroundTaskManager.py
# Botpy
#
# Created by Ashish Ahuja on 4th September 2017.
#
#

class BackgroundTaskManager:
    def __init__(self, background_tasks):
        self.tasks = background_tasks

    def start_tasks(self):
        for each_task in self.tasks:
        
