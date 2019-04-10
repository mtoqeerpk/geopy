#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# basic functions for lines

import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4])
from vis.color import color as color


__all__ = ['line']


LineStyleList = ['Solid', 'Dashed', 'Dashdot', 'Dotted', 'None']
LineWidthList = [i for i in range(1, 20)]


class line:
    # Pack all functions as a class
    #
    LineStyleList = LineStyleList
    LineWidthList = LineWidthList
    LineColorList = color.ColorList