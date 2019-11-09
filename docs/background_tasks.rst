Background Tasks
================

Botpy contains a background task manager, which schedules various background tasks to be run at certain intervals. It also manages them appropriately during instances when the bot is in standby, or is just rebooting or shutting down.

The bot, by default, has many background tasks running which are necessary for its basic functionality, such as listening to commands. Custom background tasks can also be added.

All background tasks are run in their separate threads.

A Background Task
-----------------

A single instance of a background task is defined by the :code:`BackgroundTask` class (`bg_task_source`_).

.. _bg_task_source: https://github.com/SOBotics/Botpy/blob/master/Source/BackgroundTask.py

.. code:: python

    __init__(self, function_callback, interval=30)

The first argument of the background task object is the function callback, i.e, the callback to the function which needs to be called on a scheduled basis.

The second argument, :code:`interval`, defines the interval between consecutive function calls in seconds. This is set to half a minute by default.

Background Task Manager
-----------------------

All background tasks are handled by the background task manager. The function :code:`add_background_task` in the Bot class adds a background task to the background task manager of the bot.

.. code:: python
    
    add_background_task(self, background_task)

An example in practice can be seen below.

.. code:: python

    import BotpySE as bp

    def foo():
        print("foo")

    def bar(a, b):
        print(a + b)

    # ...
    # Bot initialisation code here 
    # ...

    bot.add_background_task(bp.BackgroundTask(foo, 10))
    bot.add_background_task(bp.BackgroundTask(lambda x: bar(5, 10), 1));
    bot.start()

    # ...

In the above example, the function :code:`foo` will be invoked every 10 seconds, while the function :code:`bar` will be invoked every second with the parameters 5 and 10.

