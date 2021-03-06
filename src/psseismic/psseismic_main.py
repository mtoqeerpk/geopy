#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Shape all functions as a single class


__all__ = ['psseismic_main']

class psseismic_main:
    import os, sys
    sys.path.append(os.path.dirname(__file__)[:-10])
    #
    from psseismic.inputoutput import inputoutput as io
    from psseismic.analysis import analysis as ays
    from psseismic.visualization import visualization as vis