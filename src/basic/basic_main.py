#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     March 2018                                                                      #
#                                                                                           #
#############################################################################################

# Shape all functions as a single class


__all__ = ['basic_main']


class basic_main:
    import os, sys
    sys.path.append(os.path.dirname(__file__)[:-6])
    #
    from basic.data import  data as data
    from basic.matdict import matdict as mdict
    from basic.curve import curve as curve
    from basic.image import image as image
    from basic.video import video as video
