#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# pre-stack seismic data processing functions

from PyQt5 import QtCore
import sys
import numpy as np


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
        if 'XLNum' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'XLStart' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'XLEnd' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'XLStep' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'XLRange' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'ILNum' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'ILStart' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'ILEnd' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'ILStep' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'ILRange' not in psseis[shot]['ShotInfo'].keys():
            return False
        if 'TraceFlag' not in psseis[shot]['ShotInfo'].keys():
            return False
    #
    return True


def createShotInfo(shotdata, zstart=0, zstep=-1, xlstart=0, xlstep=1, inlstart=0, inlstep=1):
    info = {}
    if np.ndim(shotdata) < 3:
        print('ERROR in createShotInfo: shot data in 3D matrix')
        sys.exit()
    info['ZNum'], info['XLNum'], info['ILNum'] = np.shape(shotdata)
    info['ZStart'] = zstart
    info['ZStep'] = zstep
    info['ZEnd'] = zstart + (info['ZNum'] - 1) * zstep
    info['ZRange'] = np.linspace(info['ZStart'], info['ZEnd'], info['ZNum'])
    info['XLStart'] = xlstart
    info['XLStep'] = xlstep
    info['XLEnd'] = xlstart + (info['XLNum'] - 1) * xlstep
    info['XLRange'] = np.linspace(info['XLStart'], info['XLEnd'], info['XLNum'])
    info['ILStart'] = inlstart
    info['ILStep'] = inlstep
    info['ILEnd'] = inlstart + (info['ILNum'] - 1) * inlstep
    info['ILRange'] = np.linspace(info['ILStart'], info['ILEnd'], info['ILNum'])
    info['TraceFlag'] = np.zeros([info['XLNum'], info['ILNum']])
    # check trace flag
    for i in range(info['ILNum']):
        for j in range(info['XLNum']):
            if np.min(shotdata[:, j, i]) >= np.max(shotdata[:, j, i]):
                info['TraceFlag'][j, i] = 1
    #
    return info


class analysis:
    checkPsSeis = checkPsSeis
    #
    createShotInfo = createShotInfo