# Botpy

A python framework for creating bots on the StackExchange network. 

# Installation

Botpy does not support any versions of Python before Python3. It has been thoroughly tested on Python 3.6 (and *should* work for 3.x).To install Botpy, run:

    pip3.6 install BotpySE --user

or

    sudo -H pip3.6 install BotpySE

# Changelog

 - **v0.6.4**: Let Botpy users override commands and choose privileges.
 - **v0.6.3**: Allow addition of files to be synced with Redunda.
 - **v0.6.2**: Small changes to location support.
 - **v0.6.1**: Add location support.
 - **v0.6.0**: Add Redunda support.
 - **v0.5.1**: Allow change of storage prefix.
 - **v0.5.0**: Huge overhaul; a lot has changed. Most classes now inherited from ChatExchange.
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
 - **v0.2.3**: Possible bug fix for a bug which does not allow bot names with more than 4 letters.
