#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# basic functions for markers

import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4])
from vis.color import color as color


__all__ = ['marker']


MarkerStyleList = ['*', '+', 'o', 'v', '^', '<', '<',
                   'x', 'X', '.', 'None']
MarkerSizeList = [i for i in range(1, 20)]


class marker:
    # Pack all functions as a class
    #
    MarkerStyleList = MarkerStyleList
    MarkerSizeList = MarkerSizeList
    MarkerColorList = color.ColorList