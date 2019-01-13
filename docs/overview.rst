Overview
========

This section will provide a small introduction to headstart you understanding Botpy. At the end, we will construct a simple chatbot.

The Bot Object
--------------

Botpy is heavily based around one object, that is the :code:`Bot` object.

First, you have to initialise a :code:`Bot` which is defined as follows:

.. code:: python

    __init__(self, bot_name, commands, room_ids, background_tasks=[], host='stackexchange.com', email=None, password=None)

1. :code:`bot_name` is a string which will hold the name of the bot. This name will be used in a multitude of places, but most crucially, in recognizing commands. 

  1. All chat messages (in rooms the bot is in) starting with :code:`@<bot name>` will be recognised as a command directed towards the bot. 
  2. If the name specified is :code:`testbot`, then pings ranging from :code:`@tes` to :code:`@testbot` will be recognised. Three letter of the bot name is a minimum for recognition.
  3. The case of this argument does not matter.

2. :code:`commands` is a list consisting of :code:`Command` objects.

  1. All commands which can be run by the bot will have to be listed in this argument. 
  2. The command will have appropriate functions for command usage, privileges and code to be run on invocation. Look at the commands section in the User Guide for more information on writing commands.

.. warning:: Objects passed through this argument which do not adhere to the given command format will lead to the bot malfunctioning to an extent which cannot be predicted.

3. :code:`room_ids` is a list consisting of room ids the bot should join.

  1. The Bot will not listen to any messages and recognise any commands from rooms not specified in this list.
  2. The room id must exist on the specified host (SO, SE, or MSE).

4. :code:`background_tasks` is a list consisting of :code:`BackgroundTask` objects. 

  1. The BackgroundTaskManager opens up threads for processes which will run while the bot is alive. If you have another process to run during the life of the bot, it is advised to use the BackgroundTaskManager since it will shut down and start these tasks automatically whenever required.
  2. Leave this field blank (:code:`[]`) if no extra processes are required to run during the life of the bot, or if you choose to not use the BackgroundTask Manager.
  3. For more information on constructing :code:`BackgroundTask` objects, look at the background tasks section.

5. :code:`host` is a string consisting of the chat host the bot will run on.

  1. Possible hosts are:

    1. :code:`stackexchange.com` (default)
    2. :code:`stackoverflow.com`
    3. :code:`meta.stackexchange.com`

6. :code:`email` is a string consisting of the email of the account the bot will use (default: :code:`None`).

7. :code:`password` is a string consisting of the password of the account the bot will use (default: :code:`None`).

.. note:: It is recommended to store your email and password in environment variables, or read them in during program execution. Please *avoid* hardcoding them in your program.

Running the bot
---------------

Once the bot object has been constructed, a majority of the work has been done. As you will see in further sections, using the privilege system, using Redunda, etc. will require more changes after the bot object has been created. For now though, we can simply focus on starting and stopping the bot.

.. code:: python
    
    bot.start()

The above line will start the bot (where :code:`bot` is the :code:`Bot` object) and start running all background processes specified. Processes required to keep the bot alive such as listening to rooms, running commands, etc. will automatically run.

.. code:: python

    bot.stop()

This will stop the bot. For your convenience, the bot is automatically stopped when the stop command is run. A `background task runs to continuously check`_ whether the bot has to be rebooted or stopped. Use this method to stop the bot if need be, and if you know what you're doing. 

.. note:: If stopping the bot manually is a real necessity, it is recommended to set :code:`Utilities.StopReason.shutdown` (`code reference here`_) to :code:`True` instead of directly using the :code:`stop` function. Eventually, the :code:`stop` function will be triggered. 

.. _background task runs to continuously check: https://github.com/SOBotics/Botpy/blob/6eab00049cfbaebe51c413f171ee130aae696865/Source/Bot.py#L321-L326
.. _code reference here: https://github.com/SOBotics/Botpy/blob/6eab00049cfbaebe51c413f171ee130aae696865/Source/Utilities.py#L10 


A simple chatbot
----------------

This section consists of a simple example of a chatbot named "Testbot" using all of Botpy's default features. The bot constructed here will have all functional commands (start, stop, reboot, alive, etc.) and will monitor and store room and user data. In this specific example, I will be using the Sandbox room on StackOverflow chat.

.. code:: python

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

    # Start the bot. The bot will run forever till a stop command is run. The reboot command will automatically reboot the bot.
    # All background tasks specified and those automatically added will continue running till the bot stops.
    bot.start() 

Before you run this bot, there is one more requirement needed to be fulfilled. Botpy stores all required user files at :code:`~/.<bot name>`. In this case, before you run the bot, you need to create a directory. Run:

.. code:: bash

    $ mkdir ~/.testbot

You're now all good to go! Try running the bot. Go to the sandbox room on SO chat and run some commands. This is all what is required to run a fully functional chatbot on the StackExchange network.

.. note:: The bot account you are using needs to have at least 20 reputation on StackOverflow to chat. If you do not have a bot account, or simply do not have 20 rep in it, you can use your own account. It might be slightly weird with the bot responding to your own messages from the same account, but it'll work.
