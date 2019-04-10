#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# basic functions for processing video

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#
sys.path.append(os.path.dirname(__file__))
from colormap import colormap as vis_cmap


__all__ = ['video']


def animateVideo(video, video_height, video_width, video_depth,
                 frame_list=[],
                 cmapname='Red-White-Blue', flipcmap=False, fontsize=12,
                 savepath='./', savename='video.mp4',
                 verbose=True):
    """
    Generate animation of a single video
    Args:
        video:          2D matrix of videos [1, npixel]
        video_height:   height of video
        video_width:    width of video
        video_depth:    depth of video
        frame_list:     list of frames. Default is [] for all frames
        cmapname:       name of colormap as listed below:
                            'seismic', 'phase', 'frequency',
                            'red_white_blue',
                            'black_white_red', 'black_white_green', 'black_white_blue',
                            'white_gray_black',
                            'white_red_black', 'white_green_black', 'white_blue_black',
                            'black_red', 'black_green', 'black_blue'
                        Default is 'red_white_blue'
        flipcmap:       Flip colormap. Default is False
        fontsize:       font size
        savepath:       path of saving the animation. Default is current directory
        savename:       name of saving the animation. Default is tfgan_er.mp4
        verbose:        display the animation process. Default is True
    Returns:
        None
    """

    if np.ndim(video) != 2:
        print('ERROR in animateVideo: 2D video matrix expected')
        sys.exit()
    if video_height <= 1 or video_width <= 1 or video_depth <= 1:
        print('ERROR in animateVideo: Video height/width/depth be > 1')
        sys.exit()

    if os.path.exists(savepath) is False:
        print('ERROR in animateVideo: No directory found for saving animation file')
        sys.exit()
    if os.path.exists(os.path.join(savepath, savename)) is True:
        print('WARNING in animateVideo: Overwrite pre-existing animation file')

    nvideo, npixel = np.shape(video)

    if nvideo > 1:
        print('WARNING in animateVideo: Only first video selected')
        video = video[0, :]

    if npixel != video_height * video_width * video_depth:
        print('ERROR in animateVideo: Video height/width/depth not match')
        sys.exit()

    if len(frame_list) < 1 or np.min(frame_list) < 0 or np.max(frame_list) > video_depth-1:
        print('WARNING in animateVideo: All frames selected')
        frame_list = np.linspace(0, video_depth - 1, video_depth, dtype=np.int)

    frame_list = frame_list.astype(int)

    video = np.reshape(video, [video_height, video_width, video_depth])

    fig = plt.figure(facecolor='white')

    def animate(i):
        if verbose and (i + 1) % 10 == 0:
            print('Animate ' + str(i + 1) + ' of ' + str(len(frame_list)) + ' frames')
        fig.clear()
        fig.suptitle('Frame No. = ' + str(frame_list[i]))
        plt.rc('font', size=fontsize)
        ims = []
        im = plt.imshow(video[:, :, frame_list[i]],
                        interpolation='bicubic',
                        cmap=vis_cmap.makeColorMap(cmapname, flipcmap))
        plt.axis('off')
        ims.append(im)
        return ims

    anim = animation.FuncAnimation(fig, animate, frames=len(frame_list), interval=500,
                                   blit=True, init_func=None)

    writer = animation.FFMpegWriter()
    anim.save(os.path.join(savepath, savename), writer=writer, dpi=300)

    return True


def animateVideoGallery(video, video_height, video_width, video_depth,
                        frame_list=[], ncol = 5,
                        cmapname='red_white_blue', flipcmap=False,
                        spacing=False, maxfigsize=10, fontsize=12,
                        savepath='./', savename='video.mp4',
                        verbose=True):
    """
    Generate animation of multiple videos
    Args:
        video:          2D matrix of videos [nvideo, npixel]
        video_height:   height of video
        video_width:    width of video
        video_depth:    depth of video
        frame_list:     list of frames. Default is [] for all frames
        ncol:           number of videos per row
        cmapname:       name of colormap as listed below:
                            'seismic', 'phase', 'frequency',
                            'red_white_blue',
                            'black_white_red', 'black_white_green', 'black_white_blue',
                            'white_gray_black',
                            'white_red_black', 'white_green_black', 'white_blue_black',
                            'black_red', 'black_green', 'black_blue'
                        Default is 'red_white_blue'
        flipcmap:       Flip colormap. Default is False
        spacing:        spacing or not between subplots. Default is False
        maxfigsize:     maximum figure size. Default is 10
        fontsize:       font size. Default is 12
        savepath:       path of saving the animation. Default is current directory
        savename:       name of saving the animation. Default is tfgan_er.mp4
        verbose:        display the animation process. Default is True
    Returns:
        None
    """

    if np.ndim(video) != 2:
        print('ERROR in animateVideoGallery: 2D video matrix expected')
        sys.exit()
    if video_height <= 1 or video_width <= 1 or video_depth <= 1:
        print('ERROR in animateVideoGallery: Video height/width/depth be > 1')
        sys.exit()

    if os.path.exists(savepath) is False:
        print('ERROR in animateVideoGallery: No directory found for saving animation file')
        sys.exit()
    if os.path.exists(os.path.join(savepath, savename)) is True:
        print('WARNING in animateVideoGallery: Overwrite pre-existing animation file')

    nvideo, npixel = np.shape(video)

    if ncol < 1:
        print('ERROR in animateVideoGallery: Column number be >= 1')
        sys.exit()

    nrow = int(nvideo / ncol)

    if npixel != video_height * video_width * video_depth:
        print('ERROR in animateVideoGallery: Video height/width/depth not match')
        sys.exit()

    if len(frame_list) < 1 or np.min(frame_list) < 0 or np.max(frame_list) > video_depth-1:
        print('WARNING in animateVideoGallery: All frames selected')
        frame_list = np.linspace(0, video_depth - 1, video_depth, dtype=np.int)

    frame_list = frame_list.astype(int)

    video = np.reshape(video,[nvideo, video_height, video_width, video_depth])

    figwidth = float(ncol * video_width)
    figheight = float(nrow * video_height)
    if figwidth > figheight:
        figheight = figheight / figwidth * maxfigsize
        figwidth = maxfigsize
    else:
        figwidth = figwidth / figheight * maxfigsize
        figheight = maxfigsize

    fig = plt.figure(facecolor='white', figsize=(figwidth, figheight))

    # initialization function: plot the background of each frame
    def init():
        ims = []
        for k in range(nrow * ncol):
            plt.subplot(nrow, ncol, k + 1)
            im = plt.imshow(np.zeros([video_height, video_width]),
                            interpolation='bicubic',
                            cmap=vis_cmap.makeColorMap(cmapname, flipcmap))
            plt.axis('off')
            ims.append(im)
        return ims

    def animate(i):
        if verbose and (i + 1) % 10 == 0:
            print('Animate ' + str(i + 1) + ' of ' + str(len(frame_list)) + ' frames')
        fig.clear()
        fig.suptitle('Frame No. = ' + str(frame_list[i]))
        plt.rc('font', size=fontsize)
        ims = []
        for k in range(nrow*ncol):
            plt.subplot(nrow, ncol, k+1)
            im = plt.imshow(video[k, :, :, frame_list[i]],
                            interpolation='bicubic',
                            cmap=vis_cmap.makeColorMap(cmapname, flipcmap))
            plt.axis('off')
            ims.append(im)
        if spacing is False:
            plt.subplots_adjust(wspace=0, hspace=0)
        return ims

    anim = animation.FuncAnimation(fig, animate, frames=len(frame_list), interval=500,
                                   blit=True, init_func=None)

    writer = animation.FFMpegWriter()
    anim.save(os.path.join(savepath, savename), writer=writer, dpi=300)

    return True


class video:
    # Pack all functions as a class
    #
    animateVideo = animateVideo
    animateVideoGallery = animateVideoGallery