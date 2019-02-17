#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# basic functions for processing image

import sys
import os
import numpy as np
import math
import matplotlib.pyplot as plt
#
sys.path.append(os.path.dirname(__file__))
from colormap import colormap as vis_cmap


__all__ = ['image']


InterpolationList = ['None', 'Nearest', 'Quadric', 'Bilinear', 'Bicubic', 'Kaiser']


def plotImage(image, image_height, image_width,
              index_list=[], cmapname='red_white_blue', flipcmap=False):
    """
    Plot images
    Args:
        image:          2D matrix of images [pixel 1, pixel 2, ..., pixel N]
                        Each row for all pixels in an image
        image_height:   height of image
        image_width:    width of image
        index_list:     index of the image row
        cmapname:       name of colormap as listed below:
                            'seismic', 'phase', 'frequency',
                            'red_white_blue',
                            'black_white_red', 'black_white_green', 'black_white_blue',
                            'white_gray_black',
                            'white_red_black', 'white_green_black', 'white_blue_black',
                            'black_red', 'black_green', 'black_blue'
                        Default is 'red_white_blue'
        flipcmap:   Flip colormap. Default is False
    Returns:
        None
    """

    if np.ndim(image) != 2:
        print('ERROR in plotImage: 2D image matrix expected')
        sys.exit()
    if image_height <= 1 or image_width <= 1:
        print('ERROR in plotImage: Image height/width be > 1')
        sys.exit()

    nimage, npixel = np.shape(image)

    if len(index_list) < 1 or np.min(index_list)<0 or np.max(index_list)>nimage-1:
        print('WARNING in plotImage: All images selected')
        index_list = np.linspace(0, nimage-1, nimage, dtype=np.int)

    index_list = index_list.astype(int)

    if npixel != image_height * image_width:
        print('ERROR in plotImage: Image height/width not match')
        sys.exit()
    for i in index_list:
        if i >=0 and i<nimage:
            plt.figure(facecolor='white')
            image_i = image[i, :]
            image_i = np.reshape(image_i, [image_height, image_width])
            plt.title('Image No. ' + str(i+1))
            plt.imshow(image_i, interpolation='bicubic',
                       cmap=vis_cmap.makeColorMap(cmapname, flipcmap))
            plt.axis('off')

    plt.show()

    return


def plotImageGallery(image, image_height, image_width, ncol=5,
                     cmapname='red_white_blue', flipcmap=False,
                     spacing=False, maxfigsize=10,
                     valuemin=None, valuemax=None):
    """
    Plot image gallery
    Args:
        image:          2D matrix of images [nimage, npixel]
        image_height:   height of image
        image_width:    width of image
        ncol:           number of columns for subplotting. Default is 5
        cmapname:       name of colormap as listed below:
                            'seismic', 'phase', 'frequency',
                            'red_white_blue',
                            'black_white_red', 'black_white_green', 'black_white_blue',
                            'white_gray_black',
                            'white_red_black', 'white_green_black', 'white_blue_black',
                            'black_red', 'black_green', 'black_blue'
                        Default is 'red_white_blue'
        flipcmap:       Flip colormap. Default is False
        maxfigsize:     maximum figure size. Default is 10
    Returns:
        None
    """

    if np.ndim(image) != 2:
        print('ERROR in plotImageGallery: 2D matrix expected for image')
        sys.exit()

    if ncol < 1:
        print('ERROR in plotImageGallery: Column number be >= 1')
        sys.exit()

    if maxfigsize <= 0:
        print('ERROR in plotImageGallery: Maximum figure size be >= 1')
        sys.exit()

    nimage = np.shape(image)[0]
    nrow = math.ceil(nimage / ncol)
    npixel = np.shape(image)[1]

    if npixel != image_height*image_width:
        print('ERROR in plotImageGallery: Image size not match')
        sys.exit()


    figwidth = float(ncol * image_width)
    figheight = float(nrow * image_height)
    if figwidth > figheight:
        figheight = figheight / figwidth * maxfigsize
        figwidth = maxfigsize
    else:
        figwidth = figwidth / figheight * maxfigsize
        figheight = maxfigsize

    plt.figure(facecolor='white', figsize=(figwidth, figheight))
    for i in range(nrow):
        for j in range(ncol):
            if i*ncol+j+1 > nimage:
                break
            if valuemax is None:
                _vmax = np.max(image[i * ncol + j, :])
            else:
                _vmax = valuemax
            if valuemin is None:
                _vmin = np.min(image[i * ncol + j, :])
            else:
                _vmin = valuemin
            plt.subplot(nrow, ncol, i * ncol + j + 1)
            plt.imshow(np.reshape(image[i * ncol + j, :], [image_height, image_width]),
                       interpolation='bicubic',
                       cmap=vis_cmap.makeColorMap(cmapname, flipcmap),
                       vmin=_vmin, vmax=_vmax,
                       )
            plt.axis('off')
    if spacing is False:
        plt.subplots_adjust(wspace=0.0, hspace=0.0)
    plt.show()

    return


class image:
    # Pack all functions as a class
    #
    InterpolationList = InterpolationList
    #
    plotImage = plotImage
    plotImageGallery = plotImageGallery
