Commands
========

Botpy has a large number of default commands, and has multiple provisions to include new commands created by you. You can also add upon already existing commands. We will be constructing a simple command in this section. 

Command Design
--------------

In Botpy, each command has to be a class which builds upon the default :code:`Command` class (`class source code here`_). The class has three major functions which you need to configure, namely :code:`usage`, :code:`privileges` and :code:`run`. Their usage will be covered in detail in the next few sections. .

.. _class source code here: https://github.com/SOBotics/Botpy/blob/master/Source/Command.py 

All commands which the bot should listen for need to be passed in a list while constructing the :code:`Bot` object as mentioned in the overview section. This list should contain the complete class of each command.
 
So far, we know that our new command should inherit from the class :code:`Command`. Here's the code which represents this:

.. code:: python

    from BotpySE as bp

    class CommandTest(bp.Command):

The Usage method
----------------

The :code:`usage` method, as the name represents, defines the usage of the command, i.e what chat messages should invoke the command. This method is often called *before* the command object is initialised, so it does not have any arguments, *including* the :code:`self` argument which every method in a class ususally does. It is also recommended to use this method as a :code:`@staticmethod`.

A simple :code:`usage` method defined as follows

.. code:: python

    @staticmethod
    def usage():
        return ["test", "demo"]

will lead to the command being invoked whenever a user pings the bot name with message contents of either "test" or "demo". 

Commands usually have multiple arguments. Some command *require* a minimum number of requirements. Often, the command code you write may have to check whether a number of arguments have been provided or not. Now, with appropriate usage of the :code:`usage` method, you do not need to check for these arguments; Botpy does it for you.

In the command string being returned in the :code:`usage` method, simply specify a :code:`*` for every argument you need. So, a method specified as follows

.. code:: python

    def usage():
        return ["test *", "demo *"]

will make Botpy invoke the command if and *only if* 1 argument is specified after the command (a chat message such as :code:`@<name> demo abcd` will then lead to the command being invoked with :code:`abcd` as an argument). No arguments or more than 1 argument will lead to the bot not invoking the command. 

The following code

.. code:: python

    def usage():
        return ["test * * *", "demo * * *"]

will lead to the command being invoked *only if* 3 arguments are specified. 

.. warning:: All asterisk symbols *must* be space separated from the command, from each other and from all other symbols. If the asterisks aren't space separated from each other, such as :code:`test **`, Botpy will not recognize the asterisk as a symbol, but as a part of the command; that will lead to the command being invoked only when the chat message is :code:`@<name> test **`. 

Some commands can accept an unspecified number of arguments.
