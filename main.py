#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# Shape all as a single class

__all__ = ['gui']

import os, sys
#
sys.path.append(os.path.dirname(__file__))
from src.gui.gui_main import gui_main as gui

if __name__ == "__main__":
    gui()
