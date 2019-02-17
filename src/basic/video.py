#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     March 2018                                                                      #
#                                                                                           #
#############################################################################################

# basic functions for processing video

import sys
import numpy as np
from scipy import interpolate


__all__ = ['video']


def changeVideoSize(video, video_height, video_width, video_depth,
                    video_height_new, video_width_new, video_depth_new):
    """
    Change video size through 3D interpolation
    Args:
        video:              2D matrix of videos [pixel 1, pixel 2, ..., pixel N]
                            Each row for all pixels in an video
        video_height:       original height of video
        video_width:        original width of video
        video_depth:        original depth of video
        video_height_new:   new height of video
        video_width_new:    new width of video
        video_depth_new:    new depth of video
    Returns:
        2D matrix of videos after interpolation
    """

    if np.ndim(video) != 2:
        print('ERROR in changeVideoSize: 2D video matrix expected')
        sys.exit()
    if video_height <= 1 or video_width <= 1 or video_depth <= 1:
        print('ERROR in changeVideoSize: Original video height/width/depth be > 1')
        sys.exit()
    if video_height_new <= 0 or video_width_new <= 0 or video_depth_new <= 0:
        print('ERROR in changeVideoSize: New video height/width/depth be >= 1')
        sys.exit()

    nvideo, npixel = np.shape(video)

    if npixel != video_height * video_width * video_depth:
        print('ERROR in changeVideoSize: Original video height/width/depth not match')
        sys.exit()

    height = np.linspace(0.0, 1.0, video_height)
    width = np.linspace(0.0, 1.0, video_width)
    depth = np.linspace(0.0, 1.0, video_depth)
    height_new = np.linspace(0.0, 1.0, video_height_new)
    width_new = np.linspace(0.0, 1.0, video_width_new)
    depth_new = np.linspace(0.0, 1.0, video_depth_new)
    npixel_new = video_height_new * video_width_new * video_depth_new
    height_new, width_new, depth_new = np.meshgrid(height_new, width_new, depth_new, indexing='ij')
    height_new = np.reshape(height_new, [npixel_new, 1])
    width_new = np.reshape(width_new, [npixel_new, 1])
    depth_new = np.reshape(depth_new, [npixel_new, 1])

    video_new = np.zeros([nvideo, npixel_new])
    for i in range(nvideo):
        video_i = video[i, :]
        video_i = np.reshape(video_i, [video_height, video_width, video_depth])

        f = interpolate.RegularGridInterpolator((height, width, depth), video_i, method='linear')
        video_i_new = f(np.concatenate((height_new, width_new, depth_new), axis=1))
        video_i_new = np.reshape(video_i_new, [video_height_new, video_width_new, video_depth_new])
        video_new[i, :] = np.reshape(video_i_new, [1, npixel_new])

    return video_new


class video:
    # Pack all functions as a class
    #
    changeVideoSize = changeVideoSize