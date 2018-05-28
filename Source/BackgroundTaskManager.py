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

    def add_background_task(self, background_task):
        self.tasks.append(background_task)

    def start_tasks(self):
        for each_task in self.tasks:
            each_task.start_task()

    def stop_tasks(self):
        for each_task in self.tasks:
            each_task.stop_task()

    def restart_tasks(self):
        self.stop_tasks()
        self.start_tasks()
