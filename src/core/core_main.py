#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Shape all functions as a single class


__all__ = ['core_main']


class core_main:
    import os, sys
    sys.path.append(os.path.dirname(__file__)[:-5])
    #
    from core.keyboard import keyboard as keyboard
    from core.settings import settings as settings
