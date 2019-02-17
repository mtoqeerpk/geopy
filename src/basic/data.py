#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# basic functions for processing data

import numpy as np
import os, sys


__all__ = ['data']


def str2int(str):
    try:
        return int(str)
    except ValueError:
        return False


def str2float(str):
    try:
        return float(str)
    except ValueError:
        return False


class data:
    # Pack all functions as a class
    str2int = str2int
    str2float = str2float
