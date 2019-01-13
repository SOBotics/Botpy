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

Commands usually have multiple arguments. Some commands *require* a minimum number of requirements. Often, the command code you write may have to check whether a number of arguments have been provided or not. Now, with appropriate usage of the :code:`usage` method, you do not need to check for these arguments; Botpy does it for you.

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

.. warning:: All asterisk symbols *must* be space separated from the command, from each other and from all other symbols. If the asterisks aren't space separated from each other, such as :code:`test **`, Botpy will not recognize the asterisk as a symbol, but as a part of the command; that will lead to the command being invoked only when the chat message is :code:`@<name> test **`**. 

Some commands can accept an unspecified number of arguments. For such cases, use `...`.

When `...` is used, it specifies than any number of arguments will lead to the command being executed, even zero.

.. code:: python

    def usage():
        return ["test ...", "demo ..."]

will lead to the command being invoked irrespective of the number of arguments provided (including zero). As before, all arguments provided will be available in the `arguments` list present in the command instance.

In cases where a minimum number of arguments are required, combine both the techniques mentioned above and use something like 

.. code:: python

    def usage():
        return ["test * ...", "demo * ..."]

which will invoke the command when *at least* 1 argument is provided.

.. warning:: Use these methods with care; wrong usage won't lead to warnings or errors, just undefined behavior.

The Run Method
--------------

Every command instance must contain a method named `run`, which gets called upon command invocation.

Say, in our test command, we want to print a message to the CLI when it gets invoked. Here is what the code would look like:

.. code:: python

    def run(self):
        print("Hello, World!")

Now, when the command is invoked through chat, this message will appear in the CLI.

.. warning:: Not implementing the `run` method will lead to a `NotImplementedError` being raised.

Arguments provided to the command can be accessed through a list named `arguments`.

.. code:: python
    
    def run(self):
        print(self.arguments)

The message which invoked the command will also be present in a `Message` instance (https://github.com/Manishearth/ChatExchange/blob/master/chatexchange/messages.py#L9).

A command can have multiple aliases; in our previous example, we could invoke our command using both `test` and `demo`. To find out the index of the element in the aliases list which invoked the command, simply check `self.usage_index`.

The Botpy command manager can also be accessed: `self.command_manager`.

Privileged Commands
-------------------

If your bot has multiple privilege levels (see the Privileges section for more information), you might want to allow some command to be run by only some users, who belong to a specific privilege level. For this, a method named `privileges` exists in each command instance.

This method returns a single integer, which corresponds to a privilege level. All users who have a privilege level with the value being *at least* this returned integer, will be allowed to execute the command.

.. code:: python

    def privileges(self):
        return 2

The above code will make the command accessable only by users who belong to a privilege level with a value of at least 2.

.. note:: If the `privileges` method is not created, the privilege level defaults to 0.

Members
-------

.. code:: python

    self.command_manager = command_manager   # CommandManager Instance
    self.message = message                   # chatexchange.Message Instance
    self.arguments = arguments               # List consisting of provided arguments
    self.usage_index = usage_index           # Index of alias invoking the command

Other Helper Functions
----------------------

The Command Class consists of two helper functions.

The `post` method allows you to post a message in the chatroom in which the command was invoked.

.. code:: python

    def post(self, text, length_check=True)

`text` should be a string which contains the content to be posted to the chatroom. `length_check` is a boolean, which is True by default. StackExchange chat rooms have a character-limit for single line chat-messages. Set this to False if you do not want ChatExchange checking for this character-limit, or if you are posting a multi-line message.

.. code:: python

    def run(self):
        self.post("Hello, fellow users!")

Will lead to a message being posted in the chat room in which the command was invoked.

The `reply` method directly replies to the chat message which invoked the command.

.. code:: python

    def reply(self, text, length_check=True)

The usage is the same as for the `post` method.

An example command
------------------

.. code:: python

    class CommandTest(Command):
        @staticmethod
        def usage():
            return ["test ...", "demo ..."]

        def privileges(self):
            return 2

        def run(self):
            print(self.arguments)
            self.reply("Hello, fellow users!")

