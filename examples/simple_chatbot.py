# 15th April 2019

import os
import getpass
import BotpySE as bp

if "ChatbotEmail" in os.environ:
    email = os.environ["ChatbotEmail"]
else:
    email = input("Email: ")

if "ChatbotPass" in os.environ:
    password = os.environ["ChatbotPass"]
else:
    password = getpass.getpass("Password: ")

commands = bp.all_commands # We are using all of Botpy's default commands, and not creating any of our own.

rooms = [1]                # This bot will join only one room, that is the Sandbox room (room id 1) on StackOverflow chat.

background_tasks = []      # We will not be having any background tasks in this bot.
                           # All tasks required to keep the bot alive such as monitoring rooms will be automatically added.

host = "stackoverflow.com" # Our chat room is on StackOverflow chat.

bot = bp.Bot("TestBot", commands, rooms, background_tasks, host, email, password)

# Erase email and password from memory.
email = ""
password = ""

def test(event):
    print(event)
    print("woot")

bot.add_event_callback(test)

# Start the bot. The bot will run forever till a stop command is run. The reboot command will automatically reboot the bot.
# All background tasks specified and those automatically added will continue running till the bot stops.
bot.start()
