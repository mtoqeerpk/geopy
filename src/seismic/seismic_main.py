#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Shape all functions as a single class


__all__ = ['seismic_main']

class seismic_main:
    import os, sys
    sys.path.append(os.path.dirname(__file__)[:-8])
    #
    from seismic.inputoutput import inputoutput as io
    from seismic.analysis import analysis as ays
    from seismic.visualization import visualization as vis
    from seismic.attribute import attribute as attrib