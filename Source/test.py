import Bot
import os
import chatexchange as ce

email = os.environ['SockEmail']
password = os.environ['SockPass']

client = ce.Client("stackoverflow.com", email, password)

bot = Bot.Bot("sock", client, [Bot.CommandAlive, Bot.CommandStop], [123602])

bot.add_essential_background_tasks()

bot.start_bot()
