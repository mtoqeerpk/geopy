#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# basic functions for colormap

import numpy as np
import matplotlib.colors as clr


__all__ = ['colormap']


ColorMapList = ['Seismic', 'Phase', 'Frequency', 'Red-White-Blue', 'Gray',
                'Black-White-Red', 'Black-White-Green', 'Black-White-Blue',
                'White-Red-Black', 'White-Green-Black', 'White-Blue-Black',
                'Black-Red', 'Black-Green', 'Black-Blue']


def makeColorMap(cmapname=None, flip=False):
    """
    Make common colormap used for data visualization
    Argus:
        cmapname:   name of colormap as listed below:
                        'Seismic', 'Phase', 'Frequency',
                        'Red-White-Blue',
                        'Black-White-Red', 'Black-White-Green', 'Black-White-Blue',
                        'Gray',
                        'White-Red-Black', 'White-Green-Black', 'White-Blue-Black',
                        'Black-Red', 'Black-Green', 'Black-Blue'
                    Default is 'Red-White-Blue'
        flip:       flip colormap or not
    Return:
         colormap
    """

    if cmapname is None:
        cmapname = 'Red-White-Blue'

    colormap = {}

    # seismic
    col_loc = np.array([-1.0, -0.33, -0.2, 0.0, 0.2, 0.33, 1.0])
    col_r = np.array([161.0, 0.0, 77.0, 204.0, 97.0, 191.0, 255.0]) / 255.0
    col_g = np.array([255.0, 0.0, 77.0, 204.0, 69.0, 0.0, 255.0]) / 255.0
    col_b = np.array([255.0, 191.0, 77.0, 204.0, 0.0, 0.0, 0.0]) / 255.0
    col_r = np.interp(np.linspace(-1.0, 1.0, 2001), col_loc, col_r)
    col_g = np.interp(np.linspace(-1.0, 1.0, 2001), col_loc, col_g)
    col_b = np.interp(np.linspace(-1.0, 1.0, 2001), col_loc, col_b)
    col_r = np.reshape(col_r, [2001, 1])
    col_g = np.reshape(col_g, [2001, 1])
    col_b = np.reshape(col_b, [2001, 1])
    seismic = np.concatenate((col_r, col_g, col_b), axis=1)
    # Add to colormap dictionary
    colormap['Seismic'] = seismic

    # phase
    col_loc = np.linspace(0.0, 1.0, 11)
    col_r = np.array([255.0, 255.0, 255.0, 255.0, 198.0, 0.0, 0.0, 0.0, 0.0, 161.0, 255.0]) / 255.0
    col_g = np.array([0.0, 0.0, 114.0, 228.0, 255.0, 255.0, 255.0, 228.0, 114.0, 0.0, 0.0]) / 255.0
    col_b = np.array([255.0, 161.0, 0.0, 0.0, 0.0, 0.0, 198.0, 255.0, 255.0, 255.0, 255.0]) / 255.0
    col_r = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_r)
    col_g = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_g)
    col_b = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_b)
    col_r = np.reshape(col_r, [2001, 1])
    col_g = np.reshape(col_g, [2001, 1])
    col_b = np.reshape(col_b, [2001, 1])
    phase = np.concatenate((col_r, col_g, col_b), axis=1)
    # Add to colormap dictionary
    colormap['Phase'] = phase

    # frequency
    col_loc = np.linspace(0.0, 1.0, 11)
    col_r = np.array([0.0, 255.0, 255.0, 240.0, 147.0, 0.0, 0.0, 0.0, 0.0, 170.0, 255.0]) / 255.0
    col_g = np.array([0.0, 0.0, 190.0, 255.0, 255.0, 255.0, 255.0, 208.0, 85.0, 0.0, 0.0]) / 255.0
    col_b = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 120.0, 225.0, 255.0, 255.0, 255.0, 255.0]) / 255.0
    col_r = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_r)
    col_g = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_g)
    col_b = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_b)
    col_r = np.reshape(col_r, [2001, 1])
    col_g = np.reshape(col_g, [2001, 1])
    col_b = np.reshape(col_b, [2001, 1])
    frequency = np.concatenate((col_r, col_g, col_b), axis=1)
    # Add to colormap dictionary
    colormap['Frequency'] = frequency

    # red_white_blue
    col_r = np.concatenate((np.ones([1001]), np.linspace(0.999, 0.0, 1000)))
    col_r = np.reshape(col_r, [2001, 1])
    col_g = np.concatenate((np.linspace(0.0, 1.0, 1001), np.linspace(0.999, 0.0, 1000)))
    col_g = np.reshape(col_g, [2001, 1])
    col_b = np.concatenate((np.linspace(0.0, 0.999, 1000), np.ones([1001])))
    col_b = np.reshape(col_b, [2001, 1])
    red_white_blue = np.concatenate((col_r, col_g, col_b), axis=1)
    # Add to colormap dictionary
    colormap['Red-White-Blue'] = red_white_blue

    # black_white_red/green/blue
    col_1 = np.concatenate((np.linspace(0.0, 0.999, 1000), np.ones([1001])))
    col_1 = np.reshape(col_1, [2001, 1])
    col_2 = np.concatenate((np.linspace(0.0, 1.0, 1001), np.linspace(0.999, 0.0, 1000)))
    col_2 = np.reshape(col_2, [2001, 1])
    black_white_red = np.concatenate((col_1, col_2, col_2), axis=1)
    black_white_green = np.concatenate((col_2, col_1, col_2), axis=1)
    black_white_blue = np.concatenate((col_2, col_2, col_1), axis=1)
    # Add to colormap dictionary
    colormap['Black-White-Red'] = black_white_red
    colormap['Black-White-Green'] = black_white_green
    colormap['Black-White-Blue'] = black_white_blue

    # white_gray_black
    col = np.linspace(1.0, 0.0, 2001)
    col = np.reshape(col, [2001, 1])
    white_gray_black = np.concatenate((col, col, col), axis=1)
    # Add to colormap dictionary
    colormap['Gray'] = white_gray_black

    # white_red/green/blue_black
    col_1 = np.concatenate((np.ones([1001]), np.linspace(0.999, 0.0, 1000)))
    col_1 = np.reshape(col_1, [2001, 1])
    col_2 = np.concatenate((np.linspace(1.0, 0.0, 1001), np.zeros([1000])))
    col_2 = np.reshape(col_2, [2001, 1])
    white_red_black = np.concatenate((col_1, col_2, col_2), axis=1)
    white_green_black = np.concatenate((col_2, col_1, col_2), axis=1)
    white_blue_black = np.concatenate((col_2, col_2, col_1), axis=1)
    # Add to colormap dictionary
    colormap['White-Red-Black'] = white_red_black
    colormap['White-Green-Black'] = white_green_black
    colormap['White-Blue-Black'] = white_blue_black

    # black_red/green/blue
    col_1 = np.linspace(0.0, 1.0, 2001)
    col_1 = np.reshape(col_1, [2001, 1])
    col_2 = np.zeros([2001])
    col_2 = np.reshape(col_2, [2001, 1])
    black_red = np.concatenate((col_1, col_2, col_2), axis=1)
    black_green = np.concatenate((col_2, col_1, col_2), axis=1)
    black_blue = np.concatenate((col_2, col_2, col_1), axis=1)
    # Add to colormap dictionary
    colormap['Black-Red'] = black_red
    colormap['Black-Green'] = black_green
    colormap['Black-Blue'] = black_blue

    cmapdata = colormap['Red-White-Blue']
    if cmapname in colormap:
        cmapdata = colormap[cmapname]
    if flip:
        cmapdata = np.flipud(cmapdata)

    return clr.ListedColormap(cmapdata)


class colormap:
    # Pack all functions as a class
    #
    ColorMapList = ColorMapList
    #
    makeColorMap = makeColorMap
