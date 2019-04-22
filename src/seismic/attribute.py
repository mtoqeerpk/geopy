#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# seismic attribute analysis functions

from PyQt5 import QtCore
import sys
import numpy as np


def calcCumulativeSum(seis3dmat):
    """
    Calculate cusum attribute
    Argus:
        seis3dmat: seismic data in 3D matrix [Z/XL/IL]
    Return:
    """
    if np.ndim(seis3dmat) != 3:
        print('ERROR in calcCumulativeSum: 3D seismic matrix expected')
        sys.exit()
    #
    return np.cumsum(seis3dmat, axis=0)

def calcFirstDerivative(seis3dmat):
    """
    Calculate first derivative attribute
    Argus:
        seis3dmat: seismic data in 3D matrix [Z/XL/IL]
    Return:
    """
    if np.ndim(seis3dmat) != 3:
        print('ERROR in calcFirstDerivative: 3D seismic matrix expected')
        sys.exit()
    #
    attrib = seis3dmat.copy()
    if np.shape(seis3dmat)[0] > 1:
        attrib[1:, :, :] -= seis3dmat[0:-1, :, :]
        # attrib[0, :, :] *= 0
    #
    return attrib


class attribute:
    # pack all functions as a class
    #
    calcCumulativeSum = calcCumulativeSum
    calcFirstDerivative = calcFirstDerivative