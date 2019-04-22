#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# pre-stack seismic data visualization functions

from PyQt5 import QtCore
import sys, os
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
#
sys.path.append(os.path.dirname(__file__)[:-10])
from vis.font import font as vis_font
from vis.colormap import colormap as vis_cmap
from psseismic.analysis import analysis as psseis_ays


__all__ = ['visualization']


def remove_keymap_conflicts(new_keys_set):
    for prop in plt.rcParams:
        if prop.startswith('keymap.'):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)


def first_shot(ax, shotlist, pref='', surf=''):
    """Go to the first shot."""
    volume = ax.volume
    ax.index = 0
    ax.set_title(pref + shotlist[ax.index] + surf)
    #
    nsample = np.shape(volume[shotlist[ax.index]]['ShotData'])[0]
    data = np.reshape(np.transpose(volume[shotlist[ax.index]]['ShotData'], [0, 2, 1]), [nsample, -1])
    ax.images[0].set_array(data)



def previous_shot(ax, shotlist, step=1, pref='', surf=''):
    """Go to the previous slice."""
    volume = ax.volume
    ax.index = (ax.index - step) % len(shotlist)  # wrap around using %
    ax.set_title(pref + shotlist[ax.index] + surf)
    #
    nsample = np.shape(volume[shotlist[ax.index]]['ShotData'])[0]
    data = np.reshape(np.transpose(volume[shotlist[ax.index]]['ShotData'], [0, 2, 1]), [nsample, -1])
    ax.images[0].set_array(data)


def next_shot(ax, shotlist, step=1, pref='', surf=''):
    """Go to the next slice."""
    volume = ax.volume
    ax.index = (ax.index + step) % len(shotlist)  # wrap around using %
    ax.set_title(pref + shotlist[ax.index] + surf)
    #
    nsample = np.shape(volume[shotlist[ax.index]]['ShotData'])[0]
    data = np.reshape(np.transpose(volume[shotlist[ax.index]]['ShotData'], [0, 2, 1]), [nsample, -1])
    ax.images[0].set_array(data)


def last_shot(ax, shotlist, pref='', surf=''):
    """Go to the last slice."""
    volume = ax.volume
    ax.index = -1
    ax.set_title(pref + shotlist[ax.index] + surf)
    #
    nsample = np.shape(volume[shotlist[ax.index]]['ShotData'])[0]
    data = np.reshape(np.transpose(volume[shotlist[ax.index]]['ShotData'], [0, 2, 1]), [nsample, -1])
    ax.images[0].set_array(data)


def plotPsSeisShot(psseis, shotlist=None,
                   colormap=None, flipcmap=False,
                   valuemin=-1.0, valuemax=1.0,
                   titlesurf='', colorbaron=False,
                   verbose=True):
    if psseis_ays.checkPsSeis(psseis) is False:
        print('ERROR in plotPsSeisShot: no pre-stack seismic found')
        sys.exit()
    #
    if shotlist is None:
        print('WARNING in plotPsSeisShot: plot all shots')
        shotlist = list(psseis.keys())
    #
    nshot = len(shotlist)
    if verbose:
        print('Plot ' + str(nshot) + ' shots')
    for i in range(nshot):
        shot = shotlist[i]
        #
        if shot in psseis.keys():
            tracestart = psseis[shot]['ShotInfo']['XLStart']
            traceend = psseis[shot]['ShotInfo']['XLEnd']
            zstart = psseis[shot]['ShotInfo']['ZStart']
            zend = psseis[shot]['ShotInfo']['ZEnd']
            tracerange = psseis[shot]['ShotInfo']['XLRange']
            zrange = psseis[shot]['ShotInfo']['ZRange']
            x, y = np.meshgrid(tracerange, zrange)
            #
            seisdata = psseis[shot]['ShotData']
            plt.figure(facecolor='white')
            plt.pcolormesh(x, y, seisdata,
                           cmap=vis_cmap.makeColorMap(colormap, flipcmap),
                           shading='gouraud',
                           vmin=valuemin, vmax=valuemax)
            plt.xlim([tracestart, traceend])
            plt.ylim([zend, zstart])
            plt.title('Shot No.' + shot + titlesurf)
            plt.xlabel('Trace No.')
            plt.ylabel('Vertical (z) Depth/Time')
            if colorbaron:
                plt.colorbar()
    plt.show()
    #
    return True


def plotPsSeisShotPlayer(psseis, initshot=None,
                         colormap=None, flipcmap=False,
                         valuemin=-1.0, valuemax=1.0,
                         titlesurf='', colorbaron=False,
                         interpolation='bicubic',
                         playerconfig=None,
                         fontstyle=None,
                         qicon=None
                         ):
    if psseis_ays.checkPsSeis(psseis) is False:
        print('ERROR in plotPsSeisShotPlayer: no pre-stack seismic found')
        sys.exit()
    #
    shotlist = list(sorted(psseis.keys()))
    #
    if initshot is None:
        print('WARNING in plotPsSeisShotPlayer: to be initialized by the first shot')
        initshot = shotlist[0]
    if playerconfig is None:
        playerconfig = {}
        playerconfig['First'] = 'A'
        playerconfig['Previous'] = 'S'
        playerconfig['Backward'] = 'Z'
        playerconfig['Pause'] = 'X'
        playerconfig['Forward'] = 'C'
        playerconfig['Next'] = 'D'
        playerconfig['Last'] = 'F'
        playerconfig['Interval'] = 5
    #
    def process_key(event):
        fig = event.canvas.figure
        ax = fig.axes[0]
        if event.key == playerconfig['First'].lower():
            first_shot(ax, shotlist, pref='Shot No. ', surf=titlesurf)
            fig.canvas.draw()
        if event.key == playerconfig['Previous'].lower():
            previous_shot(ax, shotlist, step=playerconfig['Interval'], pref='Shot No. ', surf=titlesurf)
            fig.canvas.draw()
        if event.key == playerconfig['Next'].lower():
            next_shot(ax, shotlist, step=playerconfig['Interval'], pref='Shot No. ', surf=titlesurf)
            fig.canvas.draw()
        if event.key == playerconfig['Last'].lower():
            last_shot(ax, shotlist, pref='Shot No. ', surf=titlesurf)
            fig.canvas.draw()
        if event.key == playerconfig['Backward'].lower():
            while True:
                previous_shot(ax, shotlist, step=playerconfig['Interval'], pref='Shot No. ', surf=titlesurf)
                fig.canvas.draw()
                plt.pause(0.2)
        if event.key == playerconfig['Forward'].lower():
            while True:
                next_shot(ax, shotlist, step=playerconfig['Interval'], pref='Shot No. ', surf=titlesurf)
                fig.canvas.draw()
                plt.pause(0.2)
        if event.key == playerconfig['Pause'].lower():
            plt.pause(0)
    #
    remove_keymap_conflicts({playerconfig['First'].lower(), playerconfig['Previous'].lower(),
                             playerconfig['Backward'].lower(), playerconfig['Pause'].lower(),
                             playerconfig['Forward'].lower(), playerconfig['Next'].lower(),
                             playerconfig['Last'].lower()})
    #
    vis_font.updatePltFont(fontstyle)
    #
    fig, ax = plt.subplots(facecolor='white', figsize=(8, 8))
    ax.set_xlabel('Trace No.')
    ax.set_ylabel('Vertical (z) Depth/Time')
    volume = psseis
    ax.volume = volume
    ax.index = shotlist.index(initshot)
    ax.set_title('Shot No. ' + shotlist[ax.index] + titlesurf)
    #
    zstart = volume[shotlist[ax.index]]['ShotInfo']['ZStart']
    zend = volume[shotlist[ax.index]]['ShotInfo']['ZEnd']
    #
    ntrace = np.shape(volume[shotlist[ax.index]]['ShotData'])
    ntrace = ntrace[1] * ntrace[2]
    data = np.reshape(np.transpose(volume[shotlist[ax.index]]['ShotData'], [0, 2, 1]), [-1, ntrace])
    cat = ax.imshow(data,
                    cmap=vis_cmap.makeColorMap(colormap, flipcmap),
                    aspect='auto', #float(len(tracerange)) / float(len(zrange)),
                    extent=[1, ntrace, zend, zstart],
                    interpolation=interpolation,
                    vmin=valuemin, vmax=valuemax)

    #
    if colorbaron:
        fig.colorbar(cat)
    fig.canvas.mpl_connect('key_press_event', process_key)
    if qicon is not None:
        fig.canvas.set_window_title('2D Window - Pre-stack Gather')
        #
        # Commented by HD on June 7, 2018 to avoid crash
        # plt.get_current_fig_manager().window.setWindowIcon(qicon)
    plt.show()
    #
    return


def loadPsSeisShot(imagename, shots, ispref=True,
                   inlnum=100, xlnum=100, znum=100,
                   inlstart = 0, xlstart=0, zstart=0,
                   inlstep=1, xlstep=1, zstep=-1,
                   verbose=True, qpgsdlg=None):
    """
    Load pre-stack seismic shots from image files to 3D matrix
    Argus:
        imagename:  name of image files.
        shots:      list of shot in array [inl1, inl2, ...]
        ispref:     image name is given as pref
                    'Shot_XXX.jpg' is added with XXX representing shot No.
        inlnum:     number of inline slices fro create 3D matrix. Default is 100
        xlnum:      number of crossline slices for creating 3D matrix. Default is 100
        znum:       number of z slices for creating 3D matrix. Default is 100
        verbose:    flag for message display. Default is True
    Return:
        psseis:     pre-stack seismic in a dictionary
    Note:
        Negative z is used in the vertical direction
    """

    if np.ndim(shots) != 1:
        print('ERROR in loadPsSeisShot: 1D array of shot lists expected')
        sys.exit()

    xrange = np.linspace(0.0, 1.0, inlnum*xlnum)
    zrange = np.linspace(0.0, -1.0, znum)

    nshot = len(shots)
    if verbose:
        print('Load ' + str(nshot) + ' shot images to pre-stack seismic')

    psseis = {}

    if qpgsdlg is not None:
        qpgsdlg.setMaximum(nshot)

    for i in range(nshot):
        #
        if qpgsdlg is not None:
            QtCore.QCoreApplication.instance().processEvents()
            qpgsdlg.setValue(i)
        #
        if ispref:
            shotpath = imagename + 'Shot_' + str(shots[i]) + '.jpg'
        else:
            shotpath = imagename[i]
        #
        data = plt.imread(shotpath).astype(float)
        #
        image_data = 0.2989 * data[:, :, 0] + 0.5870 * data[:, :, 1] + 0.1140 * data[:, :, 2]
        if np.max(data[:, :, 0]) * np.max(data[:, :, 1]) * np.max(data[:, :, 2]) != 0:
            image_data = image_data * 3.0 / (np.max(data[:, :, 0]) + np.max(data[:, :, 1]) + np.max(data[:, :, 2]))
        if np.shape(data)[2] > 3:
            image_data = image_data + 1.0 - data[:, :, 3]
        #
        image_x = np.linspace(0.0, 1.0, np.shape(image_data)[1])
        image_z = np.linspace(-1.0, 0.0, np.shape(image_data)[0])
        f_interp = interpolate.interp2d(image_x, image_z, image_data)

        psdata = {}
        psdata['ShotData'] = np.transpose(np.reshape(f_interp(xrange, zrange), [znum, inlnum, xlnum]),
                                          [0, 2, 1])
        psdata['ShotInfo'] = psseis_ays.createShotInfo(psdata['ShotData'],
                                                       zstart=zstart, zstep=zstep,
                                                       xlstart=xlstart, xlstep=xlstep,
                                                       inlstart=inlstart, inlstep=inlstep)
        #
        psseis[str(shots[i])] = psdata
    #
    if qpgsdlg is not None:
        qpgsdlg.setValue(nshot)

    return psseis


class visualization:
    plotPsSeisShot = plotPsSeisShot
    plotPsSeisShotPlayer = plotPsSeisShotPlayer
    #
    loadPsSeisShot = loadPsSeisShot