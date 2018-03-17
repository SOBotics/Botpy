import sys
from . import PrivilegeType

sys.modules['PrivilegeType'] = PrivilegeType

from .Bot import Bot
from .BackgroundTask import BackgroundTask
from .BackgroundTaskManager import BackgroundTaskManager
from .ChatRoom import ChatRoom
from .Command import Command
from .CommandAlive import CommandAlive
from .CommandListRunningCommands import CommandListRunningCommands
from .CommandManager import CommandManager
from .CommandPrivilegeUser import CommandPrivilegeUser
from .CommandStop import CommandStop
from .PrivilegeType import PrivilegeType
from .ChatUser import ChatUser
from . import Utilities
from .CommandUnprivilegeUser import CommandUnprivilegeUser
from .CommandAmiprivileged import CommandAmiprivileged
from .CommandListPrivilegedUsers import CommandListPrivilegedUsers
from .CommandReboot import CommandReboot

all_commands = [CommandAlive, CommandListRunningCommands, CommandPrivilegeUser, CommandStop, CommandUnprivilegeUser, CommandAmiprivileged, CommandListPrivilegedUsers, CommandReboot]
