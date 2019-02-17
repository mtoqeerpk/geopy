#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     January 2019                                                                    #
#                                                                                           #
#############################################################################################

# pre-stack seismic data processing functions

from PyQt5 import QtCore
import sys
import numpy as np
import numpy.matlib as npmat


__all__ = ['analysis']


def checkPsSeis(psseis):
    if len(psseis.keys()) < 1:
        return False
    #
    for shot in psseis.keys():
        if 'ShotData' not in psseis[shot].keys() or 'ShotInfo' not in psseis[shot].keys():
            return False
        if 'ZNum' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'ZStart' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'ZEnd' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'ZStep' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'ZRange' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'TraceNum' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'TraceStart' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'TraceEnd' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'TraceStep' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'TraceRange' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'TraceMissing' not in psseis[shot]['ShotInfo'].keys():
            return False
    #
    return True


def createShotInfo(shotdata):
    info = {}
    info['ZNum'] = np.shape(shotdata)[0]
    info['TraceNum'] = np.shape(shotdata)[1]
    info['ZStart'] = 0
    info['ZStep'] = -1
    info['ZEnd'] = 0 + (info['ZNum'] - 1) * info['ZStep']
    info['ZRange'] = np.linspace(info['ZStart'], info['ZEnd'], info['ZNum'])
    info['TraceStart'] = 0
    info['TraceStep'] = 1
    info['TraceEnd'] = 0 + (info['TraceNum'] - 1) * info['TraceStep']
    info['TraceRange'] = np.linspace(info['TraceStart'], info['TraceEnd'], info['TraceNum'])
    info['TraceMissing'] = []
    #
    return info


class analysis:
    checkPsSeis = checkPsSeis
    #
    createShotInfo = createShotInfo