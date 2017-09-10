import Bot
import os
import chatexchange as ce

email = os.environ['SockEmail']
password = os.environ['SockPass']

client = ce.Client("stackoverflow.com", email, password)

commands = [Bot.CommandAlive, Bot.CommandStop, Bot.CommandListRunningCommands]

bot = Bot.Bot("sock", client, commands, [123602])

bot.add_essential_background_tasks()

bot.start_bot()
