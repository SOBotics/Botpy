#
# Utilities.py
# Botpy
#
# Created by Ashish Ahuja on 5th September 2017.
#
#

import weakref

should_shutdown = False
should_reboot = False

def convert_weak_value_dict_to_list(to_convert):
    new_list = list()
    for first, second in to_convert.items():
        new_list.append([first, second])

    return new_list
