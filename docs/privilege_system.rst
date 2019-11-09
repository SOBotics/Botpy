The Privilege System
====================

Botpy has an inbuilt privilege system to allow only trusted users to run certain commands, and to keep your bot safe and secure at all times.

System Design
-------------

Botpy's privilege system can have an unlimited number of privilege levels. Each level is associated with a number which tells us how much power each level has. By default, there are no privilege levels, and therefore each command of the bot can be run by anyone.

For example, a bot can have two privilege levels:

============ ===========
Level Name   Grant Level
============ ===========
regular user 1
owner        2
============ ===========

Each user is associated with a privilege level. A user does not have a privilege level till assigned one. In other words, by default, every user's grant level is 0. All users who have a privilege level can be listed using the default :code:`membership` command (`code reference here`_).

.. _code reference here: https://github.com/SOBotics/Botpy/blob/6eab00049cfbaebe51c413f171ee130aae696865/Source/CommandListPrivilegedUsers.py  

Each command has a minimum grant level, which can be configured as you wish (see commands section for more information). So, if a command's minimum grant level is set to 1, but the user running the command has no privilege level (or one with the grant level lower than 1), the command will not run. For a command to be executed, the command's privilege level needs to be lesser than or equal to the user's grant level.

A user's privileges can be changed by using the  

.. warning:: Setting a command's grant level higher than the maximum grant level of the privilege levels will render the command unusable, even for users with the highest privileges.  

.. note:: User privileges are room based. This means that a user with privileges or an RO with privileges in one room will not have privileges in another unless added. 

Now, let's see how to implement the above described system through Botpy.

Adding a privilege level
------------------------

A function named :code:`add_privilege_type` (`github reference here`_) which is a part of the :code:`Bot` class is defined as follows:

.. _github reference here: https://github.com/SOBotics/Botpy/blob/6eab00049cfbaebe51c413f171ee130aae696865/Source/Bot.py#L258-L260

.. code:: python

    add_privilege_type(self, privilege_level, privilege_name)

The first (excluding :code:`self`) argument :code:`privilege_level` is an integer containing the grant level. The second argument, :code:`privilege_name` contains the name of the privilege level. 

Example code to implement two privilege levels follows.

.. code:: python

    bot.add_privilege_type(1, "regular_user")
    bot.add_privilege_type(2, "owner")

The two privilege types have now been added!

.. note:: Add privilege levels only *after* the bot has started.

Granting all room owners maximum privileges
-------------------------------------------

Often, granting all room owners (ROs) of a room privileges makes sense. Now, instead of manually adding all ROs to the privilege list, Botpy provides a function to privilege all ROs, which is defined as follows:

.. code:: python

    set_room_owner_privs_max(self, ids=[])

The function :code:`set_room_owner_privs_max` (`reference here`_) will grant all ROs maximum privileges. By default, it does this for all rooms the bot runs in. If you want ROs to have privileges in specific rooms only, specify the room ids in the second argument, :code:`ids`.

.. _reference here: https://github.com/SOBotics/Botpy/blob/6eab00049cfbaebe51c413f171ee130aae696865/Source/Bot.py#L95-L116

The following

.. code:: python

    bot.set_room_owner_privs_max()

will grant maximum privileges to all ROs in all rooms the bot is in!

.. warning:: Once this has been run, ROs in these rooms will have the privileges forever. Simply deleting this line from the bot's code will not revert this. Their privileges will have to be manually removed through bot commands.
