#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# basic functions for fonts

import matplotlib.pyplot as plt
import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4])
from vis.color import color as color


__all__ = ['font']


FontNameList = ['Arial', 'Helvetica', 'Segoe UI', 'Tahoma', 'Times New Roman', 'Verdana']
FontStyleList = ['Normal', 'Italic', 'Oblique']
FontWeightList = ['Normal', 'Light', 'Medium', 'Bold', 'Semibold', 'Heavy', 'Black']
FontSizeList = [i for i in range(1, 50)]

def updatePltFont(fontstyle):
    if fontstyle is None or len(fontstyle.keys()) < 1:
        return
    #
    if 'Name' in fontstyle.keys():
        plt.rcParams['font.sans-serif'] = fontstyle['Name']
    if 'Size' in fontstyle.keys():
        plt.rcParams['font.size'] = fontstyle['Size']
        plt.rcParams['axes.titlesize'] = fontstyle['Size']
        plt.rcParams['axes.labelsize'] = fontstyle['Size']
    if 'Weight' in fontstyle.keys():
        plt.rcParams['font.weight'] = fontstyle['Weight'].lower()
        plt.rcParams['axes.titleweight'] = fontstyle['Weight'].lower()
        plt.rcParams['axes.labelweight'] = fontstyle['Weight'].lower()
    if 'Color' in fontstyle.keys():
        plt.rcParams['text.color'] = fontstyle['Color'].lower()
        plt.rcParams['axes.labelcolor'] = fontstyle['Color'].lower()
        plt.rcParams['xtick.color'] = fontstyle['Color'].lower()
        plt.rcParams['ytick.color'] = fontstyle['Color'].lower()


class font:
    # Pack all functions as a class
    #
    FontNameList = FontNameList
    FontColorList = color.ColorList
    FontStyleList = FontStyleList
    FontWeightList = FontWeightList
    FontSizeList = FontSizeList
    #
    updatePltFont = updatePltFont