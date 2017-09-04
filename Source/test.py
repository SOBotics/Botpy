import Bot
import os
import chatexchange as ce
import CommandAlive
from CommandManager import CommandManager
from BackgroundTask import *

email = os.environ['SockEmail']
password = os.environ['SockPass']

client = ce.Client("stackoverflow.com", email, password)

bot = Bot.Bot("sock", client, [CommandAlive.CommandAlive], [123602], [BackgroundTask(CommandManager.cleanup_finished_commands)])

bot.start_bot()
