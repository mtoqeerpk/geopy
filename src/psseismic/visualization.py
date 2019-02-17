#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
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
    ax.images[0].set_array(volume[shotlist[ax.index]]['ShotData'])
    ax.set_title(pref+shotlist[ax.index]+surf)
    #
    tracestart = volume[shotlist[ax.index]]['ShotInfo']['TraceStart']
    traceend = volume[shotlist[ax.index]]['ShotInfo']['TraceEnd']
    zstart = volume[shotlist[ax.index]]['ShotInfo']['ZStart']
    zend = volume[shotlist[ax.index]]['ShotInfo']['ZEnd']
    tracerange = volume[shotlist[ax.index]]['ShotInfo']['TraceRange']
    zrange = volume[shotlist[ax.index]]['ShotInfo']['ZRange']
    # ax.set_xticks(np.linspace(0, len(tracerange) - 1, 6, dtype=int))
    # ax.set_xticklabels(np.linspace(tracestart, traceend, 6, dtype=int))
    # ax.set_yticks(np.linspace(0, len(zrange) - 1, 6, dtype=int))
    # ax.set_yticklabels(np.linspace(zstart, zend, 6, dtype=int))
    ax.set_aspect(float(len(tracerange)) / float(len(zrange)))


def previous_shot(ax, shotlist, step=1, pref='', surf=''):
    """Go to the previous slice."""
    volume = ax.volume
    ax.index = (ax.index - step) % len(shotlist)  # wrap around using %
    ax.images[0].set_array(volume[shotlist[ax.index]]['ShotData'])
    ax.set_title(pref + shotlist[ax.index] + surf)
    #
    tracestart = volume[shotlist[ax.index]]['ShotInfo']['TraceStart']
    traceend = volume[shotlist[ax.index]]['ShotInfo']['TraceEnd']
    zstart = volume[shotlist[ax.index]]['ShotInfo']['ZStart']
    zend = volume[shotlist[ax.index]]['ShotInfo']['ZEnd']
    tracerange = volume[shotlist[ax.index]]['ShotInfo']['TraceRange']
    zrange = volume[shotlist[ax.index]]['ShotInfo']['ZRange']
    # ax.set_xticks(np.linspace(0, len(tracerange) - 1, 6, dtype=int))
    # ax.set_xticklabels(np.linspace(tracestart, traceend, 6, dtype=int))
    # ax.set_yticks(np.linspace(0, len(zrange) - 1, 6, dtype=int))
    # ax.set_yticklabels(np.linspace(zstart, zend, 6, dtype=int))
    ax.set_aspect(float(len(tracerange)) / float(len(zrange)))


def next_shot(ax, shotlist, step=1, pref='', surf=''):
    """Go to the next slice."""
    volume = ax.volume
    ax.index = (ax.index + step) % len(shotlist)  # wrap around using %
    ax.images[0].set_array(volume[shotlist[ax.index]]['ShotData'])
    ax.set_title(pref + shotlist[ax.index] + surf)
    #
    tracestart = volume[shotlist[ax.index]]['ShotInfo']['TraceStart']
    traceend = volume[shotlist[ax.index]]['ShotInfo']['TraceEnd']
    zstart = volume[shotlist[ax.index]]['ShotInfo']['ZStart']
    zend = volume[shotlist[ax.index]]['ShotInfo']['ZEnd']
    tracerange = volume[shotlist[ax.index]]['ShotInfo']['TraceRange']
    zrange = volume[shotlist[ax.index]]['ShotInfo']['ZRange']
    # ax.set_xticks(np.linspace(0, len(tracerange) - 1, 6, dtype=int))
    # ax.set_xticklabels(np.linspace(tracestart, traceend, 6, dtype=int))
    # ax.set_yticks(np.linspace(0, len(zrange) - 1, 6, dtype=int))
    # ax.set_yticklabels(np.linspace(zstart, zend, 6, dtype=int))
    ax.set_aspect(float(len(tracerange)) / float(len(zrange)))


def last_shot(ax, shotlist, pref='', surf=''):
    """Go to the last slice."""
    volume = ax.volume
    ax.index = -1
    ax.images[0].set_array(volume[shotlist[ax.index]]['ShotData'])
    ax.set_title(pref + shotlist[ax.index] + surf)
    #
    tracestart = volume[shotlist[ax.index]]['ShotInfo']['TraceStart']
    traceend = volume[shotlist[ax.index]]['ShotInfo']['TraceEnd']
    zstart = volume[shotlist[ax.index]]['ShotInfo']['ZStart']
    zend = volume[shotlist[ax.index]]['ShotInfo']['ZEnd']
    tracerange = volume[shotlist[ax.index]]['ShotInfo']['TraceRange']
    zrange = volume[shotlist[ax.index]]['ShotInfo']['ZRange']
    # ax.set_xticks(np.linspace(0, len(tracerange) - 1, 6, dtype=int))
    # ax.set_xticklabels(np.linspace(tracestart, traceend, 6, dtype=int))
    # ax.set_yticks(np.linspace(0, len(zrange) - 1, 6, dtype=int))
    # ax.set_yticklabels(np.linspace(zstart, zend, 6, dtype=int))
    ax.set_aspect(float(len(tracerange)) / float(len(zrange)))


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
            tracestart = psseis[shot]['ShotInfo']['TraceStart']
            traceend = psseis[shot]['ShotInfo']['TraceEnd']
            zstart = psseis[shot]['ShotInfo']['ZStart']
            zend = psseis[shot]['ShotInfo']['ZEnd']
            tracerange = psseis[shot]['ShotInfo']['TraceRange']
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
    cat = ax.imshow(volume[shotlist[ax.index]]['ShotData'],
                    cmap=vis_cmap.makeColorMap(colormap, flipcmap),
                    interpolation=interpolation,
                    vmin=valuemin, vmax=valuemax)
    #
    tracestart = volume[shotlist[ax.index]]['ShotInfo']['TraceStart']
    traceend = volume[shotlist[ax.index]]['ShotInfo']['TraceEnd']
    zstart = volume[shotlist[ax.index]]['ShotInfo']['ZStart']
    zend = volume[shotlist[ax.index]]['ShotInfo']['ZEnd']
    tracerange = volume[shotlist[ax.index]]['ShotInfo']['TraceRange']
    zrange = volume[shotlist[ax.index]]['ShotInfo']['ZRange']
    # ax.set_xticks(np.linspace(0, len(tracerange) - 1, 6, dtype=int))
    # ax.set_xticklabels(np.linspace(tracestart, traceend, 6, dtype=int))
    # ax.set_yticks(np.linspace(0, len(zrange) - 1, 6, dtype=int))
    # ax.set_yticklabels(np.linspace(zstart, zend, 6, dtype=int))
    ax.set_aspect(float(len(tracerange)) / float(len(zrange)))
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


class visualization:
    plotPsSeisShot = plotPsSeisShot
    plotPsSeisShotPlayer = plotPsSeisShotPlayer
