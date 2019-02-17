#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# pointset data IO

import numpy as np
import os, sys


__all__ = ['inputoutput']

def readPointFromAscii(asciifile, comment='#', inlcol=0, xlcol=1, zcol=2):
    if os.path.exists(asciifile) is False:
        print("ERROR in readPointFromAscii: Pointset file not found")
        sys.exit()
    #
    data = np.loadtxt(asciifile, comments=comment)
    #
    npt, ncol = np.shape(data)
    #
    if inlcol >= ncol or inlcol < 0:
        print("ERROR in readPointFromAscii: Inline column index not found")
        sys.exit()
    if xlcol >= ncol or xlcol < 0:
        print("ERROR in readPointFromAscii: Crossline column index not found")
        sys.exit()
    if zcol >= ncol or zcol < 0:
        print("ERROR in readPointFromAscii: Z column index not found")
        sys.exit()
    #
    point = np.zeros([npt, ncol])
    point[:, 0:1] = data[:, inlcol:inlcol+1]
    point[:, 1:2] = data[:, xlcol:xlcol+1]
    point[:, 2:3] = data[:, zcol:zcol+1]
    # more columns
    idx = 3
    for i in range(ncol):
        if i != inlcol and i != xlcol and i != zcol:
            point[:, idx:idx+1] = data[:, i:i+1]
            idx = idx + 1
    #
    return point


class inputoutput:
    # group all functions as a single class
    readPointFromAscii = readPointFromAscii
