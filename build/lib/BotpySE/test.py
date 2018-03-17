from Source import Bot
import os
import chatexchange as ce

email = os.environ['SockEmail']
password = os.environ['SockPass']

client = ce.Client("stackoverflow.com", email, password)

commands = [Bot.CommandAlive, Bot.CommandStop, Bot.CommandListRunningCommands]

bot = Bot.Bot("sock", client, commands, [123602])

bot.start_bot()

bot.add_essential_background_tasks()

bot.add_privilege_type(1, "owner")

#bot.rooms[0].add_privileged_user(4688119, bot.rooms[0].get_privilege_type_by_name("owner"))
