#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Shape all as a single class

__all__ = ['basic', 'core', 'vis', 'seismic', 'psseismic', 'pointset', 'gui']

import os, sys
#
sys.path.append(os.path.dirname(__file__))

from src.basic.basic_main import basic_main as basic
from src.core.core_main import core_main as core
from src.vis.vis_main import vis_main as vis
from src.seismic.seismic_main import seismic_main as seismic
from src.psseismic.psseismic_main import psseismic_main as psseismic
from src.pointset.pointset_main import pointset_main as pointset
from src.gui.gui_main import gui_main as gui

if __name__ == "__main__":
    gui()