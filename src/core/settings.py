#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# basic functions for setting

import numpy as np
import os, sys


__all__ = ['settings']

GUI = {}
GUI['Toolbar'] = {}
GUI['Toolbar']['Left'] = True
GUI['Toolbar']['Right'] = True
GUI['Toolbar']['Top'] = True
GUI['Toolbar']['Bottom'] = True

General = {}
General['RootPath'] = os.path.dirname(__file__)[:-15]

Visual = {}
Visual['Font'] = {}
Visual['Font']['Name'] = 'Times New Roman'
Visual['Font']['Color'] = 'Green'
Visual['Font']['Style'] = 'Normal'
Visual['Font']['Weight'] = 'Normal'
Visual['Font']['Size'] = 16
#
Visual['Line'] = {}
Visual['Line']['Color'] = 'Red'
Visual['Line']['Width'] = 3
Visual['Line']['Style'] = 'Solid'
Visual['Line']['MarkerStyle'] = 'None'
Visual['Line']['MarkerSize'] = 5
#
Visual['Image'] = {}
Visual['Image']['Colormap'] = 'Red-White-Blue'
Visual['Image']['Interpolation'] = 'Quadric'
#
Visual['Player'] = {}
Visual['Player']['First'] = 'A'
Visual['Player']['Previous'] = 'S'
Visual['Player']['Next'] = 'D'
Visual['Player']['Last'] = 'F'
Visual['Player']['Backward'] = 'Z'
Visual['Player']['Forward'] = 'C'
Visual['Player']['Pause'] = 'X'
Visual['Player']['Interval'] = 1


def checkGUI(gui):
    if len(gui.keys()) < 1:
        return False
    if 'Toolbar' not in gui.keys():
        return False
    if len(gui['Toolbar'].keys()) < 1:
        return False
    if 'Left' not in gui['Toolbar'].keys() \
        or 'Right' not in gui['Toolbar'].keys() \
        or 'Top' not in gui['Toolbar'].keys() \
        or 'Bottom' not in gui['Toolbar'].keys():
        return False
    #
    return True


def checkGeneral(general):
    if len(general.keys()) < 1:
        return False
    if 'RootPath' not in general.keys():
        return False
    if len(general['RootPath']) < 1:
        return False
    #
    return True


def checkVisual(visual):
    if len(visual.keys()) < 1:
        return False
    #
    if 'Font' not in visual.keys():
        return False
    if len(visual['Font'].keys()) < 1:
        return False
    if 'Name' not in visual['Font'].keys() \
        or 'Color' not in visual['Font'].keys() \
        or 'Style' not in visual['Font'].keys() \
        or 'Weight' not in visual['Font'].keys() \
        or 'Size' not in visual['Font'].keys():
        return False
    #
    if 'Line' not in visual.keys():
        return False
    if len(visual['Line'].keys()) < 1:
        return False
    if 'Color' not in visual['Line'].keys() \
        or 'Width' not in visual['Line'].keys() \
        or 'Style' not in visual['Line'].keys() \
        or 'MarkerStyle' not in visual['Line'].keys() \
        or 'MarkerSize' not in visual['Line'].keys():
        return False
    #
    if 'Image' not in visual.keys():
        return False
    if len(visual['Image'].keys()) < 1:
        return False
    if 'Colormap' not in visual['Image'].keys():
        return False
    if 'Interpolation' not in visual['Image'].keys():
        return False
    #
    if 'Player' not in visual.keys():
        return False
    if len(visual['Player'].keys()) < 1:
        return False
    if 'First' not in visual['Player'].keys():
        return False
    if 'Previous' not in visual['Player'].keys():
        return False
    if 'Next' not in visual['Player'].keys():
        return False
    if 'Last' not in visual['Player'].keys():
        return False
    if 'Backward' not in visual['Player'].keys():
        return False
    if 'Forward' not in visual['Player'].keys():
        return False
    if 'Pause' not in visual['Player'].keys():
        return False
    if 'Interval' not in visual['Player'].keys():
        return False
    #
    return True


def checkSettings(gui={}, general={}, visual={}):
    if checkGUI(gui) is False or checkGeneral(general) is False or checkVisual(visual) is False:
        return False
    #
    return True


class settings:
    # Pack all functions as a class
    GUI = GUI
    General = General
    Visual = Visual
    #
    checkGUI = checkGUI
    checkGeneral = checkGeneral
    checkVisual = checkVisual
    #
    checkSettings = checkSettings

