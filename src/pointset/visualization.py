#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# basic functions for crossplot

import sys, os
import numpy as np
import matplotlib.pyplot as plt
#
sys.path.append(os.path.dirname(__file__)[:-9])
from basic.matdict import matdict as basic_mdt
from vis.font import font as vis_font


__all__ = ['visualization']


def crossplot2D(pointdict,
                colorlist=[], linestylelist=[],
                linewidthlist=[],
                markerstylelist=[],
                markersizelist=[],
                xfeature='x', xlabel='x-label',
                yfeature='y', ylabel='y-label',
                xlim=[-10, 10], ylim=[-10, 10],
                fontstyle=None,
                legendon=True, qicon=None):


    # if len(colorlist) < len(pointdict):
    #     print('WARNING in crossplot2D: No color coding')
    #     colorlist = []
    # if len(markerlist) < len(pointdict):
    #     print('WARNING in crossplot2D: No marker coding')
    #     markerlist = []

    vis_font.updatePltFont(fontstyle)
    #
    fig = plt.figure(facecolor='white')
    for idx, name in enumerate(pointdict):
        color = 'Black'
        if idx < len(colorlist):
            color = colorlist[idx]
        linestyle = 'Solid'
        if idx < len(linestylelist):
            linestyle = linestylelist[idx]
        linewidth = 12
        if idx < len(linewidthlist):
            linewidth = linewidthlist[idx]
        markerstyle = '.'
        if idx < len(markerstylelist):
            markerstyle = markerstylelist[idx]
        markersize = '.'
        if idx < len(markersizelist):
            markersize = markersizelist[idx]
        #
        pointdata = pointdict[name]
        if xfeature not in pointdata.keys():
            print('ERROR in crossplot2D: %s not found in %s' %(xfeature, name))
            sys.exit()
        if yfeature not in pointdata.keys():
            print('ERROR in crossplot2D: %s not found in %s' %(yfeature, name))
            sys.exit()
        #
        pointnum = basic_mdt.maxDictConstantRow(pointdata)
        x = np.mean(np.reshape(pointdata[xfeature], [pointnum, -1]),
                    axis=1)
        y = np.mean(np.reshape(pointdata[yfeature], [pointnum, -1]),
                    axis=1)
        plt.plot(x, y, linestyle=linestyle, linewidth=linewidth,
                 color=color, marker=markerstyle, markersize=markersize, label=name)
    #
    if legendon:
        plt.legend()
    #
    plt.xlabel(xlabel)
    plt.xlim(xlim)
    plt.ylabel(ylabel)
    plt.ylim(ylim)
    plt.title(xfeature + ' vs ' + yfeature)

    if qicon is not None:
        fig.canvas.set_window_title('2D Window - PointSet Cross-plot')

    plt.show()


class visualization:
    # Pack all functions as a class
    #
    crossplot2D = crossplot2D