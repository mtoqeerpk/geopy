#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# pointset processing functions

from PyQt5 import QtCore
import sys
import numpy as np
import numpy.matlib as npmat


__all__ = ['analysis']


def checkPoint(point):
    if len(point.keys()) < 1:
        return False
    #
    if 'Inline' not in point.keys() or 'Crossline' not in point.keys() or 'Z' not in point.keys():
            return False
    #
    return True


class analysis:
    checkPoint = checkPoint
