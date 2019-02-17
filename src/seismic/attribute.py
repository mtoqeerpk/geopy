#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     September 2018                                                                  #
#                                                                                           #
#############################################################################################

# seismic attribute analysis functions

from PyQt5 import QtCore
import sys
import numpy as np


def calcSeisCuSum(seis3dmat):
    """
    Calculate cusum attribute
    Argus:
        seis3dmat: seismic data in 3D matrix [Z/XL/IL]
    Return:
    """
    if np.ndim(seis3dmat) != 3:
        print('ERROR in calcSeisCuSum: 3D seismic matrix expected')
        sys.exit()
    #
    return np.cumsum(seis3dmat, axis=0)


class attribute:
    # pack all functions as a class
    #
    calcSeisCuSum = calcSeisCuSum