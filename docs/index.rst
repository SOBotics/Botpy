.. Botpy documentation master file, created by
   sphinx-quickstart on Mon Aug 20 12:30:21 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Botpy
=================================

A python framework for creating bots on the StackExchange network. Builds upon ChatExchange to create a nice framework to help you make bots without the nitty-gritty you would otherwise have.

Features
--------

 - ChatUser management, along with privilege levels. Set up privilege levels using a single line of code. Botpy also provides different privilege chat commands to get your privilege system up and running in seconds!
 - Command management, which you can easily extend with your own commands. Provides a simple template to make commands. Also provides a huge number of default commands you can configure.
 - Redunda support, to help you run multiple instances at the same time and also have backups of all your bot data.
 - A fully functional background task manager using threads, which allows you to add your own tasks. Automatically stops and starts tasks based on the status of the instance.

Installation
------------

Botpy has been thoroughly tested on Python 3.6 (and *should* work on all versions above Python 3). To install the latest version from PyPi, simply run:

    $ pip3.6 install -U BotpySE

or

    $ sudo -H pip3.6 install BotpySE

.. note:: Compatibility issues with versions of python below 3.6 will not be fixed by the author.

.. warning:: The PyPi package is named `BotpySE`, not `Botpy`.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
