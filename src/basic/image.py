#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     March 2018                                                                      #
#                                                                                           #
#############################################################################################

# basic functions for processing image

import sys
import numpy as np
from scipy import interpolate



__all__ = ['image']


def changeImageSize(image, image_height, image_width,
                    image_height_new, image_width_new,
                    kind='cubic'):
    """
    Change image size through 2D interpolation
    Args:
        image:              2D matrix of images [pixel 1, pixel 2, ..., pixel N]
                            Each row for all pixels in an image
        image_height:       original height of image
        image_width:        original width of image
        image_height_new:   new height of image
        image_width_new:    new width of image
        kind:               interpolation type 'linear', 'cubic', or 'quintic'. Default is 'cubic
    Returns:
        2D matrix of images after interpolation
    """

    if np.ndim(image) != 2:
        print('ERROR in changeImageSize: 2D image matrix expected')
        sys.exit()
    if image_height <= 1 or image_width <= 1:
        print('ERROR in changeImageSize: Original image height/width be > 1')
        sys.exit()
    if image_height_new <= 0 or image_width_new <= 0:
        print('ERROR in changeImageSize: New image height/width be >= 1')
        sys.exit()

    nimage, npixel = np.shape(image)

    if npixel != image_height * image_width :
        print('ERROR in changeImageSize: Original image height/width not match')
        sys.exit()


    height = np.linspace(0.0, 1.0, image_height)
    width = np.linspace(0.0, 1.0, image_width)
    height_new = np.linspace(0.0, 1.0, image_height_new)
    width_new = np.linspace(0.0, 1.0, image_width_new)
    npixel_new = image_height_new * image_width_new

    image_new = np.zeros([nimage, npixel_new])
    for i in range(nimage):
        image_i = image[i, :]
        image_i = np.reshape(image_i, [image_height, image_width])
        f = interpolate.interp2d(width, height, image_i, kind=kind)
        image_i_new = f(width_new, height_new)
        image_new[i, :] = np.reshape(image_i_new, [1, npixel_new])

    return image_new


def rotateImage(image, image_height, image_width, flag='180'):
    """
    Rotate images
    Args:
        image:          2D matrix of images [pixel 1, pixel 2, ..., pixel N]
                        Each row for all pixels in an image
        image_height:   height of image
        image_width:    width of image
        flag:           type of rotation. Default is '180'
                        180 for 180-degree rotation (anticlockwise)
                        90 for 90-degree rotation
                        270 for 270-degree rotation
                        lr for horizontally flipping
                        ud for vertically flipping
    Returns:
        2D matrix of images after rotation
    """

    if np.ndim(image) != 2:
        print('ERROR in rotateImage: 2D image matrix expected')
        sys.exit()
    if image_height <= 1 or image_width <= 1:
        print('ERROR in rotateImage: Original image height/width be > 1')
        sys.exit()
    nimage, npixel = np.shape(image)
    if npixel != image_height * image_width:
        print('ERROR in rotateImage: Image height/width not match')
        sys.exit()
    #
    image_rotate = np.reshape(image, [nimage, image_height, image_width])
    #
    if flag == '90':
        image_rotate = np.flip(np.transpose(image_rotate, [0, 2, 1]), axis=1)
    if flag == '180':
        image_rotate = np.flip(np.flip(image_rotate, axis=1), axis=2)
    if flag == '270':
        image_rotate = np.flip(np.transpose(image_rotate, [0, 2, 1]), axis=2)
    if flag == 'lr':
        image_rotate = np.flip(image_rotate, axis=2)
    if flag == 'ud':
        image_rotate = np.flip(image_rotate, axis=1)
    #
    return np.reshape(image_rotate, [nimage, npixel])


class image:
    # Pack all functions as a class
    #
    changeImageSize = changeImageSize
    rotateImage = rotateImage