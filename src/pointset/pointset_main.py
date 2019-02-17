#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     January 2019                                                                    #
#                                                                                           #
#############################################################################################

# Shape all functions as a single class


__all__ = ['pointset_main']

class pointset_main:
    import os, sys
    sys.path.append(os.path.dirname(__file__)[:-9])
    #
    from pointset.inputoutput import inputoutput as io
    from pointset.analysis import analysis as ays
    from pointset.visualization import visualization as vis