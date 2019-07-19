# Botpy

A python framework for creating bots on the StackExchange network.
Builds upon ChatExchange to create a nice framework to help you make bots
without the nitty-gritty you would otherwise have.

Features:

 - ChatUser management, along with privilege levels.
   Set up privilege levels using a single line of code.
   Botpy also provides different privilege chat commands to
   get your privilege system up and running in seconds!
 - Command management, which you can easily extend with your own commands.
   Provides a simple template to make commands.
   Also provides a huge number of default commands you can configure.
 - Redunda support, to help you run multiple instances at the same time
   and also have backups of all your bot data.
 - A fully functional background task manager using threads,
   which allows you to add your own tasks.
   Automatically stops and starts tasks based on the status of the instance. 

# Installation

Botpy does not support any versions of Python before Python3.
It has been thoroughly tested on Python 3.6 (and *should* work for 3.x).
To install Botpy, run:

    pip3.6 install BotpySE --user

or

    sudo -H pip3.6 install BotpySE

Botpy depends on ChatExchange.
Upstream has a slightly experimental facility called `send_aggressively`
which is not yet part of an official release;
if you wish to use this functionality,
you will also need to install ChatExchange from source, not from PyPI.


# Documentation

Some incomplete documentation of Botpy exists here: 
https://botpy.readthedocs.io/en/latest/ 

# Changelog

 - **v0.7.8**: Fix behavior for ChatExchange from PyPI; document same
 - **v0.7.7**: Fix default callback from 0.7.6.
 - **v0.7.6**: Add optional event callback; #10.
 - **v0.7.5**: Allows the usage of the `send_aggressively` option in CE;
   fix LICENSE copyright.
 - **v0.7.4**: Fixes privilege level bug.
 - **v0.7.3**: Finally fixes the bug introduced in 0.6.7.
   All default commands have been moved to `AllCommands.py`; this also fixes #11. 
 - **v0.7.2**: Another attempt at 0.7.1.
 - **v0.7.1**: Fixes bug introduced in 0.6.7.
 - **v0.7.0**: Allow multiple aliases for a bot; #7.
 - **v0.6.7**: Command directory structure organization; #8.
 - **v0.6.6**: Implement a reboot method (#6).
 - **v0.6.5**: Use logging instead of prints.
 - **v0.6.4**: Let Botpy users override commands and choose privileges.
 - **v0.6.3**: Allow addition of files to be synced with Redunda.
 - **v0.6.2**: Small changes to location support.
 - **v0.6.1**: Add location support.
 - **v0.6.0**: Add Redunda support.
 - **v0.5.1**: Allow change of storage prefix.
 - **v0.5.0**: Huge overhaul; a lot has changed.
   Most classes now inherited from ChatExchange.
 - **v0.4.3**: Misc Changes
 - **v0.3.10**: A bug fix in the reboot check background task.
 - **v0.3.9**: Missed uploading a file.
 - **v0.3.8**: Fix a bug in v0.3.7.
 - **v0.3.7**: Add a command to reboot the bot.
 - **v0.3.6**: Add a parameter in the Bot class to indicate whether the bot is alive or not.
 - **v0.3.5**: Add a command to list privileged users.
 - **v0.3.4**: (Possible) Critical bug fix in command manager.
 - **v0.3.3**: Fix a couple of exceptions.
 - **v0.3.2**: Fix a bug in command initialization. 
 - **v0.3.1**: Typo bug fix.
 - **v0.3.0**: Completed the privilege system by adding more commands.
 - **v0.2.5**: Finally fixed the bug fix for the bot name problem.
 - **v0.2.4**: Another possible bug fix for not allowing names with more than 4 chars.
 - **v0.2.3**: Possible bug fix for a bug which does not allow bot names with
   more than 4 letters.
