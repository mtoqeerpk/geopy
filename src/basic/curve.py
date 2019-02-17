#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     March 2018                                                                      #
#                                                                                           #
#############################################################################################

# basic functions for processing curves

import numpy as np
from scipy import interpolate


__all__ = ['curve']


def changeCurveSize(curve, length, length_new, kind='cubic'):
    """
    Change curve size through 1D interpolation
        curve:
        length:
        length_new:
        kind:
    Return:
        1D array of curves after interpolation
    """

    ncurve = np.shape(curve)[0]

    line = np.linspace(0.0, 1.0, length)
    line_new = np.linspace(0.0, 1.0, length_new)

    curve_new = np.zeros([ncurve, length_new])
    for i in range(ncurve):
        curve_i = curve[i, :]
        f = interpolate.interp1d(line, curve_i, kind=kind)
        curve_new[i, :] = f(line_new)

    return curve_new


class curve:
    # Pack all functions as a class
    #
    changeCurveSize = changeCurveSize