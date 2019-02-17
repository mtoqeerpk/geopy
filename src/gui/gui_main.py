#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     December 2018                                                                   #
#                                                                                           #
#############################################################################################

# Create a GUI for GeoPy mainwindow

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os
import sys
import webbrowser
#
sys.path.append(os.path.dirname(__file__)[:-4])
#
from seismic.analysis import analysis as seis_ays
from psseismic.analysis import analysis as psseis_ays
from pointset.analysis import analysis as point_ays
from basic.matdict import matdict as basic_mdt
from core.settings import settings as core_set
#
from gui.importsurveymanual import importsurveymanual as gui_importsurveymanual
from gui.importseissegy import importseissegy as gui_importseissegy
from gui.importseisimageset import importseisimageset as gui_importseisimageset
from gui.importpointsetfile import importpointsetfile as gui_importpointsetfile
from gui.exportsurvey import exportsurvey as gui_exportsurvey
from gui.exportseissegy import exportseissegy as gui_exportseissegy
from gui.exportseisnpy import exportseisnpy as gui_exportseisnpy
from gui.exportseisimageset import exportseisimageset as gui_exportseisimageset
from gui.exportpsseisnpy import exportpsseisnpy as gui_exportpsseisnpy
from gui.exportpointsetnpy import exportpointsetnpy as gui_exportpointsetnpy
#
from gui.managesurvey import managesurvey as gui_managesurvey
from gui.manageseis import manageseis as gui_manageseis
from gui.managepsseis import managepsseis as gui_managepsseis
from gui.managepointset import managepointset as gui_managepointset
#
from gui.convertseis2pointset import convertseis2pointset as gui_convertseis2pointset
from gui.convertpointset2seis import convertpointset2seis as gui_convertpointset2seis
from gui.convertpsseis2seis import convertpsseis2seis as gui_convertpsseis2seis
#
from gui.calcmathattribsingle import calcmathattribsingle as gui_calcmathattribsingle
from gui.calcmathattribmultiple import calcmathattribmultiple as gui_calcmathattribmultiple
#
from gui.plot1dseisz import plot1dseisz as gui_plot1dseisz
from gui.plot2dseisinl import plot2dseisinl as gui_plot2dseisinl
from gui.plot2dseisxl import plot2dseisxl as gui_plot2dseisxl
from gui.plot2dseisz import plot2dseisz as gui_plot2dseisz
from gui.plot2dpsseisshot import plot2dpsseisshot as gui_plot2dpsseisshot
from gui.plot2dpointsetcrossplt import plot2dpointsetcrossplt as gui_plot2dpointsetcrossplt
#
from gui.settingsgui import settingsgui as gui_settingsgui
from gui.settingsgeneral import settingsgeneral as gui_settingsgeneral
from gui.settingsvisual import settingsvisual as gui_settingsvisual
from gui.makepytemp import makepytemp as gui_makepytemp
from gui.execpycode import execpycode as gui_execpycode
#
from gui.about import about as gui_about

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


__all__ = ['gui_main']


class mainwindow(object):

    projname = 'New project'
    projpath = ''
    survinfo = {}
    seisdata = {}
    psseisdata = {}
    pointdata = {}
    #
    settings = {}
    settings['General'] = core_set.General
    settings['Gui'] = core_set.GUI
    settings['Visual'] = core_set.Visual
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(900, 560)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/logo.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 50))
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.toolbarleft = QtWidgets.QToolBar(MainWindow)
        self.toolbarleft.setObjectName("toolbarleft")
        self.toolbarleft.setGeometry(QtCore.QRect(0, 75, 50, 425))
        self.toolbarright = QtWidgets.QToolBar(MainWindow)
        self.toolbarright.setObjectName("toolbarright")
        self.toolbarright.setGeometry(QtCore.QRect(850, 75, 50, 425))
        self.toolbartop = QtWidgets.QToolBar(MainWindow)
        self.toolbartop.setObjectName("toolbartop")
        self.toolbartop.setGeometry(QtCore.QRect(0, 25, 900, 50))
        self.toolbarbottom = QtWidgets.QToolBar(MainWindow)
        self.toolbarbottom.setObjectName("toolbarbottom")
        self.toolbarbottom.setGeometry(QtCore.QRect(0, 500, 900, 50))
        #
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        self.menumanage = QtWidgets.QMenu(self.menubar)
        self.menumanage.setObjectName("menumanage")
        self.menutool = QtWidgets.QMenu(self.menubar)
        self.menutool.setObjectName("menutool")
        self.menuvis = QtWidgets.QMenu(self.menubar)
        self.menuvis.setObjectName("menuvis")
        self.menuutil = QtWidgets.QMenu(self.menubar)
        self.menuutil.setObjectName("menuutil")
        self.menuhelp = QtWidgets.QMenu(self.menubar)
        self.menuhelp.setObjectName("menuhelp")
        #
        MainWindow.setMenuBar(self.menubar)
        MainWindow.setStatusBar(self.statusbar)
        #
        self.actionnewproject = QtWidgets.QAction(MainWindow)
        self.actionnewproject.setObjectName("actionnewproject")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/new.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionnewproject.setIcon(icon)
        self.actionopenproject = QtWidgets.QAction(MainWindow)
        self.actionopenproject.setObjectName("actionopenproject")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/folder.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionopenproject.setIcon(icon)
        self.actionsaveproject = QtWidgets.QAction(MainWindow)
        self.actionsaveproject.setObjectName("actionsaveproject")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/disk.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionsaveproject.setIcon(icon)
        self.actionsaveasproject = QtWidgets.QAction(MainWindow)
        self.actionsaveasproject.setObjectName("actionsaveasproject")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/diskwithpen.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionsaveasproject.setIcon(icon)
        self.menuimport = QtWidgets.QMenu(self.menufile)
        self.menuimport.setObjectName("menuimport")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/import.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuimport.setIcon(icon)
        self.menuimportsurvey = QtWidgets.QMenu(self.menuimport)
        self.menuimportsurvey.setObjectName("menuimportsurvey")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/survey.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuimportsurvey.setIcon(icon)
        self.actionimportsurveymanual = QtWidgets.QAction(MainWindow)
        self.actionimportsurveymanual.setObjectName("actionimportsurveymanual")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/supervised.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportsurveymanual.setIcon(icon)
        self.actionimportsurveynpy = QtWidgets.QAction(MainWindow)
        self.actionimportsurveynpy.setObjectName("actionimportsurveynpy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportsurveynpy.setIcon(icon)
        self.menuimportseis = QtWidgets.QMenu(self.menuimport)
        self.menuimportseis.setObjectName("menuimportseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuimportseis.setIcon(icon)
        self.actionimportseissegy = QtWidgets.QAction(MainWindow)
        self.actionimportseissegy.setObjectName("actionimportseissegy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportseissegy.setIcon(icon)
        self.actionimportseisnpy = QtWidgets.QAction(MainWindow)
        self.actionimportseisnpy.setObjectName("actionimportseisnpy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportseisnpy.setIcon(icon)
        self.actionimportseisimageset = QtWidgets.QAction(MainWindow)
        self.actionimportseisimageset.setObjectName("actionimportseisimageset")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/image.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportseisimageset.setIcon(icon)
        self.menuimportpsseis = QtWidgets.QMenu(self.menuimport)
        self.menuimportpsseis.setObjectName("menuimportpsseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/psseismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuimportpsseis.setIcon(icon)
        self.actionimportpsseisnpy = QtWidgets.QAction(MainWindow)
        self.actionimportpsseisnpy.setObjectName("actionimportpsseisnpy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportpsseisnpy.setIcon(icon)
        self.menuimportpointset = QtWidgets.QMenu(self.menuimport)
        self.menuimportpointset.setObjectName("menuimportpointset")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuimportpointset.setIcon(icon)
        self.actionimportpointsetfile = QtWidgets.QAction(MainWindow)
        self.actionimportpointsetfile.setObjectName("actionimportpointsetfile")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/copy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportpointsetfile.setIcon(icon)
        self.actionimportpointsetnpy = QtWidgets.QAction(MainWindow)
        self.actionimportpointsetnpy.setObjectName("actionimportpointsetnpy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionimportpointsetnpy.setIcon(icon)
        self.menuexport = QtWidgets.QMenu(self.menufile)
        self.menuexport.setObjectName("menuexport")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/export.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuexport.setIcon(icon)
        self.actionexportsurvey = QtWidgets.QAction(MainWindow)
        self.actionexportsurvey.setObjectName("actionexportsurvey")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/survey.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionexportsurvey.setIcon(icon)
        self.menuexportseis = QtWidgets.QMenu(self.menuexport)
        self.menuexportseis.setObjectName("menuexportseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuexportseis.setIcon(icon)
        self.actionexportseissegy = QtWidgets.QAction(MainWindow)
        self.actionexportseissegy.setObjectName("actionexportseissegy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionexportseissegy.setIcon(icon)
        self.actionexportseisnpy = QtWidgets.QAction(MainWindow)
        self.actionexportseisnpy.setObjectName("actionexportseisnpy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionexportseisnpy.setIcon(icon)
        self.actionexportseisimageset = QtWidgets.QAction(MainWindow)
        self.actionexportseisimageset.setObjectName("actionexportseisimageset")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/image.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionexportseisimageset.setIcon(icon)
        self.menuexportpsseis = QtWidgets.QMenu(self.menuexport)
        self.menuexportpsseis.setObjectName("menuexportpsseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/psseismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuexportpsseis.setIcon(icon)
        self.actionexportpsseisnpy = QtWidgets.QAction(MainWindow)
        self.actionexportpsseisnpy.setObjectName("actionexportpsseisnpy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionexportpsseisnpy.setIcon(icon)
        self.menuexportpointset = QtWidgets.QMenu(self.menuimport)
        self.menuexportpointset.setObjectName("menuexportpointset")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuexportpointset.setIcon(icon)
        self.actionexportpointsetnpy = QtWidgets.QAction(MainWindow)
        self.actionexportpointsetnpy.setObjectName("actionexportpointsetnpy")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionexportpointsetnpy.setIcon(icon)
        self.actionquit = QtWidgets.QAction(MainWindow)
        self.actionquit.setObjectName("actionquit")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/close.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionquit.setIcon(icon)
        # Shortcuts
        self.actionnewproject.setShortcut(QtGui.QKeySequence('Ctrl+N'))
        self.actionopenproject.setShortcut(QtGui.QKeySequence('Ctrl+O'))
        self.actionsaveproject.setShortcut(QtGui.QKeySequence('Ctrl+S'))
        self.actionimportseisnpy.setShortcut(QtGui.QKeySequence('Ctrl+M'))
        self.actionimportpsseisnpy.setShortcut(QtGui.QKeySequence('Ctrl+G'))
        self.actionimportpointsetnpy.setShortcut(QtGui.QKeySequence('Ctrl+P'))
        self.actionquit.setShortcut(QtGui.QKeySequence('Ctrl+Q'))
        #
        self.actionmanagesurvey = QtWidgets.QAction(MainWindow)
        self.actionmanagesurvey.setObjectName("actionmanagesurvey")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/survey.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionmanagesurvey.setIcon(icon)
        self.actionmanageseis = QtWidgets.QAction(MainWindow)
        self.actionmanageseis.setObjectName("actionmanageseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionmanageseis.setIcon(icon)
        self.actionmanagepsseis = QtWidgets.QAction(MainWindow)
        self.actionmanagepsseis.setObjectName("actionmanagepsseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/psseismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionmanagepsseis.setIcon(icon)
        self.actionmanagepointset = QtWidgets.QAction(MainWindow)
        self.actionmanagepointset.setObjectName("actionmanagepointset")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionmanagepointset.setIcon(icon)
        # Shortcuts
        self.actionmanagesurvey.setShortcut(QtGui.QKeySequence('Shift+V'))
        self.actionmanageseis.setShortcut(QtGui.QKeySequence('Shift+M'))
        self.actionmanagepsseis.setShortcut(QtGui.QKeySequence('Shift+G'))
        self.actionmanagepointset.setShortcut(QtGui.QKeySequence('Shift+P'))
        #
        self.menudataconversion = QtWidgets.QMenu(self.menutool)
        self.menudataconversion.setObjectName("menudataconversion")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/exchange.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menudataconversion.setIcon(icon)
        self.actionconvertseis2pointset = QtWidgets.QAction(MainWindow)
        self.actionconvertseis2pointset.setObjectName("actionconvertseis2pointset")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionconvertseis2pointset.setIcon(icon)
        self.actionconvertpointset2seis = QtWidgets.QAction(MainWindow)
        self.actionconvertpointset2seis.setObjectName("actionconvertpointset2seis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionconvertpointset2seis.setIcon(icon)
        self.actionconvertpsseis2seis = QtWidgets.QAction(MainWindow)
        self.actionconvertpsseis2seis.setObjectName("actionconvertpsseis2seis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/psseismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionconvertpsseis2seis.setIcon(icon)
        self.menuattribengine = QtWidgets.QMenu(self.menutool)
        self.menuattribengine.setObjectName("menuattribengine")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/attribute.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menuattribengine.setIcon(icon)
        self.menumathattrib = QtWidgets.QMenu(self.menuattribengine)
        self.menumathattrib.setObjectName("menumathattrib")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/math.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menumathattrib.setIcon(icon)
        self.actioncalcmathattribsingle = QtWidgets.QAction(MainWindow)
        self.actioncalcmathattribsingle.setObjectName("actioncalcmathattribsingle")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/file.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actioncalcmathattribsingle.setIcon(icon)
        self.actioncalcmathattribmultiple = QtWidgets.QAction(MainWindow)
        self.actioncalcmathattribmultiple.setObjectName("actioncalcmathattribmultiple")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/copy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actioncalcmathattribmultiple.setIcon(icon)
        # Shortcut
        self.actionconvertseis2pointset.setShortcut(QtGui.QKeySequence('Alt+M'))
        self.actionconvertpointset2seis.setShortcut(QtGui.QKeySequence('Alt+P'))
        self.actionconvertpsseis2seis.setShortcut(QtGui.QKeySequence('Alt+G'))
        #
        self.menu1dwindow = QtWidgets.QMenu(self.menuvis)
        self.menu1dwindow.setObjectName("menu1dwindow")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/vis1d.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menu1dwindow.setIcon(icon)
        self.menu1dwindowseis = QtWidgets.QMenu(self.menu1dwindow)
        self.menu1dwindowseis.setObjectName("menu1dwindowseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menu1dwindowseis.setIcon(icon)
        self.actionplot1dseisz = QtWidgets.QAction(MainWindow)
        self.actionplot1dseisz.setObjectName("actionplot1dseisz")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/waveform.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionplot1dseisz.setIcon(icon)
        self.menu2dwindow = QtWidgets.QMenu(self.menuvis)
        self.menu2dwindow.setObjectName("menu2dwindow")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/vis2d.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menu2dwindow.setIcon(icon)
        self.menu2dwindowseis = QtWidgets.QMenu(self.menu2dwindow)
        self.menu2dwindowseis.setObjectName("menu2dwindowseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menu2dwindowseis.setIcon(icon)
        self.actionplot2dseisinl = QtWidgets.QAction(MainWindow)
        self.actionplot2dseisinl.setObjectName("actionplot2dseisinl")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/visinl.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionplot2dseisinl.setIcon(icon)
        self.actionplot2dseisxl = QtWidgets.QAction(MainWindow)
        self.actionplot2dseisxl.setObjectName("actionplot2dseisxl")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/visxl.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionplot2dseisxl.setIcon(icon)
        self.actionplot2dseisz = QtWidgets.QAction(MainWindow)
        self.actionplot2dseisz.setObjectName("actionplot2dseisz")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/visz.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionplot2dseisz.setIcon(icon)
        self.menu2dwindowpsseis = QtWidgets.QMenu(self.menu2dwindow)
        self.menu2dwindowpsseis.setObjectName("menu2dwindowpsseis")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/psseismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menu2dwindowpsseis.setIcon(icon)
        self.actionplot2dpsseisshot = QtWidgets.QAction(MainWindow)
        self.actionplot2dpsseisshot.setObjectName("actionplot2dpsseisshot")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/gather.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionplot2dpsseisshot.setIcon(icon)
        self.menu2dwindowpointset = QtWidgets.QMenu(self.menu2dwindow)
        self.menu2dwindowpointset.setObjectName("menu2dwindowpointset")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menu2dwindowpointset.setIcon(icon)
        self.actionplot2dpointsetcrossplt = QtWidgets.QAction(MainWindow)
        self.actionplot2dpointsetcrossplt.setObjectName("actionplot2dpointsetcrossplt")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/plotpoint.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionplot2dpointsetcrossplt.setIcon(icon)
        self.menu3dwindow = QtWidgets.QMenu(self.menuvis)
        self.menu3dwindow.setObjectName("menu3dwindow")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/vis3d.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menu3dwindow.setIcon(icon)
        self.actionplot3dslice = QtWidgets.QAction(MainWindow)
        self.actionplot3dslice.setObjectName("actionplot3dslice")
        # Shortcut
        self.actionplot1dseisz.setShortcut(QtGui.QKeySequence('Alt+W'))
        self.actionplot2dseisinl.setShortcut(QtGui.QKeySequence('Alt+I'))
        self.actionplot2dseisxl.setShortcut(QtGui.QKeySequence('Alt+X'))
        self.actionplot2dseisz.setShortcut(QtGui.QKeySequence('Alt+Z'))
        self.actionplot2dpsseisshot.setShortcut(QtGui.QKeySequence('Alt+T'))
        self.actionplot2dpointsetcrossplt.setShortcut(QtGui.QKeySequence('Alt+C'))
        #
        self.menusettings = QtWidgets.QMenu(self.menuutil)
        self.menusettings.setObjectName("menusettings")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/settings.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menusettings.setIcon(icon)
        self.actionsettingsgui = QtWidgets.QAction(MainWindow)
        self.actionsettingsgui.setObjectName("actionsettingsgui")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/logo.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionsettingsgui.setIcon(icon)
        self.actionsettingsgeneral = QtWidgets.QAction(MainWindow)
        self.actionsettingsgeneral.setObjectName("actionsettingsgeneral")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/settings.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionsettingsgeneral.setIcon(icon)
        self.actionsettingsvisual = QtWidgets.QAction(MainWindow)
        self.actionsettingsvisual.setObjectName("actionsettingsvisual")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/image.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionsettingsvisual.setIcon(icon)
        self.menupycompiler = QtWidgets.QMenu(self.menuutil)
        self.menupycompiler.setObjectName("menupycompiler")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/python.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.menupycompiler.setIcon(icon)
        self.actionmakepytemp = QtWidgets.QAction(MainWindow)
        self.actionmakepytemp.setObjectName("actionmakepytemp")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/new.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionmakepytemp.setIcon(icon)
        self.actionexecpycode = QtWidgets.QAction(MainWindow)
        self.actionexecpycode.setObjectName("actionexecpycode")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/apply.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionexecpycode.setIcon(icon)
        # Shortcut
        self.actionsettingsgui.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F8))
        self.actionsettingsgeneral.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F9))
        self.actionsettingsvisual.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F10))
        #
        self.actionmanual = QtWidgets.QAction(MainWindow)
        self.actionmanual.setObjectName("actionmanual")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/manual.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionmanual.setIcon(icon)
        self.actionsupport = QtWidgets.QAction(MainWindow)
        self.actionsupport.setObjectName("actionsupport")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/support.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionsupport.setIcon(icon)
        self.actionabout = QtWidgets.QAction(MainWindow)
        self.actionabout.setObjectName("actionabout")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/about.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.actionabout.setIcon(icon)
        # Shortcut
        self.actionmanual.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F1))
        #
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menumanage.menuAction())
        self.menubar.addAction(self.menutool.menuAction())
        self.menubar.addAction(self.menuvis.menuAction())
        self.menubar.addAction(self.menuutil.menuAction())
        self.menubar.addAction(self.menuhelp.menuAction())
        #
        self.menufile.addAction(self.actionnewproject)
        self.menufile.addAction(self.actionopenproject)
        self.menufile.addAction(self.actionsaveproject)
        self.menufile.addAction(self.actionsaveasproject)
        self.menufile.addSeparator()
        self.menufile.addAction(self.menuimport.menuAction())
        self.menuimport.addAction(self.menuimportsurvey.menuAction())
        self.menuimportsurvey.addAction(self.actionimportsurveymanual)
        self.menuimportsurvey.addAction(self.actionimportsurveynpy)
        self.menuimport.addSeparator()
        self.menuimport.addAction(self.menuimportseis.menuAction())
        self.menuimportseis.addAction(self.actionimportseissegy)
        self.menuimportseis.addAction(self.actionimportseisnpy)
        self.menuimportseis.addAction(self.actionimportseisimageset)
        self.menuimport.addAction(self.menuimportpsseis.menuAction())
        self.menuimportpsseis.addAction(self.actionimportpsseisnpy)
        self.menuimport.addAction(self.menuimportpointset.menuAction())
        self.menuimportpointset.addAction(self.actionimportpointsetfile)
        self.menuimportpointset.addAction(self.actionimportpointsetnpy)
        self.menufile.addAction(self.menuexport.menuAction())
        self.menuexport.addAction(self.actionexportsurvey)
        self.menuexport.addSeparator()
        self.menuexport.addAction(self.menuexportseis.menuAction())
        self.menuexportseis.addAction(self.actionexportseissegy)
        self.menuexportseis.addAction(self.actionexportseisnpy)
        self.menuexportseis.addAction(self.actionexportseisimageset)
        self.menuexport.addAction(self.menuexportpsseis.menuAction())
        self.menuexportpsseis.addAction(self.actionexportpsseisnpy)
        self.menuexport.addAction(self.menuexportpointset.menuAction())
        self.menuexportpointset.addAction(self.actionexportpointsetnpy)
        self.menufile.addSeparator()
        self.menufile.addAction(self.actionquit)
        #
        self.menumanage.addAction(self.actionmanagesurvey)
        self.menumanage.addSeparator()
        self.menumanage.addAction(self.actionmanageseis)
        self.menumanage.addAction(self.actionmanagepsseis)
        self.menumanage.addAction(self.actionmanagepointset)
        #
        self.menutool.addAction(self.menudataconversion.menuAction())
        self.menudataconversion.addAction(self.actionconvertseis2pointset)
        self.menudataconversion.addAction(self.actionconvertpointset2seis)
        self.menudataconversion.addSeparator()
        self.menudataconversion.addAction(self.actionconvertpsseis2seis)
        self.menutool.addSeparator()
        self.menutool.addAction(self.menuattribengine.menuAction())
        self.menuattribengine.addAction(self.menumathattrib.menuAction())
        self.menumathattrib.addAction(self.actioncalcmathattribsingle)
        self.menumathattrib.addAction(self.actioncalcmathattribmultiple)
        #
        self.menuvis.addAction(self.menu1dwindow.menuAction())
        self.menuvis.addSeparator()
        self.menuvis.addAction(self.menu2dwindow.menuAction())
        self.menuvis.addSeparator()
        self.menuvis.addAction(self.menu3dwindow.menuAction())
        self.menu1dwindow.addAction(self.menu1dwindowseis.menuAction())
        self.menu1dwindowseis.addAction(self.actionplot1dseisz)
        self.menu2dwindow.addAction(self.menu2dwindowseis.menuAction())
        self.menu2dwindowseis.addAction(self.actionplot2dseisinl)
        self.menu2dwindowseis.addAction(self.actionplot2dseisxl)
        self.menu2dwindowseis.addAction(self.actionplot2dseisz)
        self.menu2dwindow.addAction(self.menu2dwindowpsseis.menuAction())
        self.menu2dwindowpsseis.addAction(self.actionplot2dpsseisshot)
        self.menu2dwindow.addAction(self.menu2dwindowpointset.menuAction())
        self.menu2dwindowpointset.addAction(self.actionplot2dpointsetcrossplt)
        self.menu3dwindow.addAction(self.actionplot3dslice)
        #
        self.menuutil.addAction(self.menusettings.menuAction())
        self.menusettings.addAction(self.actionsettingsgui)
        self.menusettings.addAction(self.actionsettingsgeneral)
        self.menusettings.addAction(self.actionsettingsvisual)
        self.menuutil.addAction(self.menupycompiler.menuAction())
        self.menupycompiler.addAction(self.actionmakepytemp)
        self.menupycompiler.addAction(self.actionexecpycode)
        #
        self.menuhelp.addAction(self.actionmanual)
        self.menuhelp.addAction(self.actionsupport)
        self.menuhelp.addSeparator()
        self.menuhelp.addAction(self.actionabout)
        #
        self.toolbarleft.setOrientation(QtCore.Qt.Vertical)
        self.toolbarleft.addAction(self.menuimport.menuAction())
        self.toolbarleft.addSeparator()
        self.toolbarleft.addAction(self.menuexport.menuAction())
        self.toolbarleft.setVisible(self.settings['Gui']['Toolbar']['Left'])
        #
        self.toolbarright.setOrientation(QtCore.Qt.Vertical)
        self.toolbarright.addAction(self.menudataconversion.menuAction())
        self.toolbarright.addSeparator()
        self.toolbarright.addAction(self.menuattribengine.menuAction())
        self.toolbarright.setVisible(self.settings['Gui']['Toolbar']['Right'])
        #
        self.toolbartop.addAction(self.actionmanagesurvey)
        self.toolbartop.addSeparator()
        self.toolbartop.addAction(self.actionmanageseis)
        self.toolbartop.addAction(self.actionmanagepsseis)
        self.toolbartop.addAction(self.actionmanagepointset)
        self.toolbartop.setVisible(self.settings['Gui']['Toolbar']['Top'])
        #
        self.toolbarbottom.addAction(self.actionplot1dseisz)
        self.toolbarbottom.addAction(self.actionplot2dseisinl)
        self.toolbarbottom.addAction(self.actionplot2dseisxl)
        self.toolbarbottom.addAction(self.actionplot2dseisz)
        self.toolbarbottom.addSeparator()
        self.toolbarbottom.addAction(self.actionplot2dpsseisshot)
        self.toolbarbottom.addSeparator()
        self.toolbarbottom.addAction(self.actionplot2dpointsetcrossplt)
        self.toolbarbottom.setVisible(self.settings['Gui']['Toolbar']['Bottom'])
        #
        self.msgbox = QtWidgets.QMessageBox(MainWindow)
        self.msgbox.setObjectName("msgbox")
        _center_x = MainWindow.geometry().center().x()
        _center_y = MainWindow.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x-150, _center_y-50, 300, 100))
        #
        # Background image
        self.bkimage = QtWidgets.QLabel(MainWindow)
        self.bkimage.setObjectName("bkimage")
        self.bkimage.setGeometry(QtCore.QRect(200, 50, 500, 500))

        self.retranslateGUI(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateGUI(self, MainWindow):
        self.dialog = MainWindow
        #
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GeoPy V2019"+" <"+self.projname+">"))
        self.menufile.setTitle(_translate("MainWindow", "&File"))
        self.menumanage.setTitle(_translate("MainWindow", "&Manage"))
        self.menutool.setTitle(_translate("MainWindow", "&Toolbox"))
        self.menuvis.setTitle(_translate("MainWindow", "&Visualization"))
        self.menuutil.setTitle(_translate("MainWindow", "&Utilities"))
        self.menuhelp.setTitle(_translate("MainWindow", "&Help"))
        #
        self.actionnewproject.setText(_translate("MainWindow", "New Project"))
        self.actionopenproject.setText(_translate("MainWindow", "Open Project"))
        self.actionsaveproject.setText(_translate("MainWindow", "Save Project"))
        self.actionsaveasproject.setText(_translate("MainWindow", "Save Project as"))
        self.menuimport.setTitle(_translate("MainWindow", "Import"))
        self.menuimportsurvey.setTitle(_translate("MainWindow", "Survey"))
        self.actionimportsurveymanual.setText(_translate("MainWindow", "Create"))
        self.actionimportsurveynpy.setText(_translate("MainWindow", "NumPy"))
        self.menuimportseis.setTitle(_translate("MainWindow", "Seismic"))
        self.actionimportseissegy.setText(_translate("MainWindow", "SEG-Y"))
        self.actionimportseisnpy.setText(_translate("MainWindow", "NumPy"))
        self.actionimportseisnpy.setToolTip("Import Seismic from NumPy")
        self.actionimportseisimageset.setText(_translate("MainWindow", "ImageSet"))
        self.menuimportpsseis.setTitle(_translate("MainWindow", "Pre-stack Seismic"))
        self.actionimportpsseisnpy.setText(_translate("MainWindow", "NumPy"))
        self.menuimportpointset.setTitle(_translate("MainWindow", "PointSet"))
        self.actionimportpointsetfile.setText(_translate("MainWindow", "Ascii File"))
        self.actionimportpointsetnpy.setText(_translate("MainWindow", "NumPy"))
        self.menuexport.setTitle(_translate("MainWindow", "Export"))
        self.actionexportsurvey.setText(_translate("MainWindow", "Survey"))
        self.menuexportseis.setTitle(_translate("MainWindow", "Seismic"))
        self.actionexportseissegy.setText(_translate("MainWindow", "SEG-Y"))
        self.actionexportseisnpy.setText(_translate("MainWindow", "NumPy"))
        self.actionexportseisimageset.setText(_translate("MainWindow", "ImageSet"))
        self.menuexportpsseis.setTitle(_translate("MainWindow", "Pre-stack Seismic"))
        self.actionexportpsseisnpy.setText(_translate("MainWindow", "NumPy"))
        self.menuexportpointset.setTitle(_translate("MainWindow", "PointSet"))
        self.actionexportpointsetnpy.setText(_translate("MainWindow", "NumPy"))
        self.actionquit.setText(_translate("MainWindow", "Quit"))
        #
        self.actionmanagesurvey.setText(_translate("MainWindow", "Survey"))
        self.actionmanagesurvey.setToolTip("Manage Seismic Survey")
        self.actionmanageseis.setText(_translate("MainWindow", "Seismic"))
        self.actionmanageseis.setToolTip("Manage Seismic")
        self.actionmanagepsseis.setText(_translate("MainWindow", "Pre-stack Seismic"))
        self.actionmanagepsseis.setToolTip("Manage Pre-stack Seismic")
        self.actionmanagepointset.setText(_translate("MainWindow", "PointSet"))
        self.actionmanagepointset.setToolTip("Manage PointSets")
        #
        self.menudataconversion.setTitle(_translate("MainWindow", "Data conversion"))
        self.actionconvertseis2pointset.setText(_translate("MainWindow", "Seismic --> PointSet"))
        self.actionconvertpointset2seis.setText(_translate("MainWindow", "PointSet --> Seismic"))
        self.actionconvertpsseis2seis.setText(_translate("MainWindow", "Pre-stack --> Seismic"))
        self.menuattribengine.setTitle(_translate("MainWindow", "Seismic attribute"))
        self.menumathattrib.setTitle(_translate("MainWindow", "Mathematical"))
        self.actioncalcmathattribsingle.setText(_translate("MainWindow", "from Single property"))
        self.actioncalcmathattribmultiple.setText(_translate("MainWindow", "between Multiple properties"))
        #
        self.menu1dwindow.setTitle(_translate("MainWindow", "1D window"))
        self.menu1dwindowseis.setTitle(_translate("MainWindow", "Seismic"))
        self.actionplot1dseisz.setText(_translate("MainWindow", "Waveform"))
        self.actionplot1dseisz.setToolTip("1D Window: Seismic Waveform")
        self.menu2dwindow.setTitle(_translate("MainWindow", "2D window"))
        self.menu2dwindowseis.setTitle(_translate("MainWindow", "Seismic"))
        self.actionplot2dseisinl.setText(_translate("MainWindow", "Inline"))
        self.actionplot2dseisinl.setToolTip("2D Window: Seismic Inline")
        self.actionplot2dseisxl.setText(_translate("MainWindow", "Crossline"))
        self.actionplot2dseisxl.setToolTip("2D Window: Seismic Crossline")
        self.actionplot2dseisz.setText(_translate("MainWindow", "Time/depth"))
        self.actionplot2dseisz.setToolTip("2D Window: Seismic Time/depth")
        self.menu2dwindowpsseis.setTitle(_translate("MainWindow", "Pre-stack Seismic"))
        self.actionplot2dpsseisshot.setText(_translate("MainWindow", "Gather"))
        self.actionplot2dpsseisshot.setToolTip("2D Window: Pre-stack Gather")
        self.menu2dwindowpointset.setTitle(_translate("MainWindow", "PointSet"))
        self.actionplot2dpointsetcrossplt.setText(_translate("MainWindow", "Cross-plot"))
        self.actionplot2dpointsetcrossplt.setToolTip("2D Window: PointSet Cross-plot")
        self.menu3dwindow.setTitle(_translate("MainWindow", "3D window"))
        self.actionplot3dslice.setText(_translate("MainWindow", "IL/XL/Z"))
        #
        self.menusettings.setTitle(_translate("MainWindow", 'Settings'))
        self.actionsettingsgui.setText(_translate("MainWindow", "GeoPy"))
        self.actionsettingsgeneral.setText(_translate("MainWindow", "General"))
        self.actionsettingsvisual.setText(_translate("MainWindow", "Visual"))
        self.menupycompiler.setTitle(_translate("MainWindow", 'Python compiler'))
        self.actionmakepytemp.setText(_translate("MainWindow", "Create template"))
        self.actionexecpycode.setText(_translate("MainWindow", "Execute"))
        #
        self.actionmanual.setText(_translate("MainWindow", "Manual"))
        self.actionsupport.setText(_translate("MainWindow", "Online support"))
        self.actionabout.setText(_translate("MainWindow", "About"))
        #
        self.actionnewproject.triggered.connect(self.doNewProject)
        self.actionopenproject.triggered.connect(self.doOpenProject)
        self.actionsaveproject.triggered.connect(self.doSaveProject)
        self.actionsaveasproject.triggered.connect(self.doSaveasProject)
        self.actionimportsurveymanual.triggered.connect(self.doImportSurveyManual)
        self.actionimportsurveynpy.triggered.connect(self.doImportSurveyNpy)
        self.actionimportseissegy.triggered.connect(self.doImportSeisSegy)
        self.actionimportseisnpy.triggered.connect(self.doImportSeisNpy)
        self.actionimportseisimageset.triggered.connect(self.doImportSeisImageSet)
        self.actionimportpsseisnpy.triggered.connect(self.doImportPsSeisNpy)
        self.actionimportpointsetfile.triggered.connect(self.doImportPointSetFile)
        self.actionimportpointsetnpy.triggered.connect(self.doImportPointSetNpy)
        self.actionexportsurvey.triggered.connect(self.doExportSurvey)
        self.actionexportseissegy.triggered.connect(self.doExportSeisSegy)
        self.actionexportseisnpy.triggered.connect(self.doExportSeisNpy)
        self.actionexportseisimageset.triggered.connect(self.doExportSeisImageSet)
        self.actionexportpsseisnpy.triggered.connect(self.doExportPsSeisNpy)
        self.actionexportpointsetnpy.triggered.connect(self.doExportPointSetNpy)
        self.actionquit.triggered.connect(self.doQuit)
        #
        self.actionmanagesurvey.triggered.connect(self.doManageSurvey)
        self.actionmanageseis.triggered.connect(self.doManageSeis)
        self.actionmanagepsseis.triggered.connect(self.doManagePsSeis)
        self.actionmanagepointset.triggered.connect(self.doManagePointSet)
        #
        self.actionconvertseis2pointset.triggered.connect(self.doConvertSeis2PointSet)
        self.actionconvertpointset2seis.triggered.connect(self.doConvertPointSet2Seis)
        self.actionconvertpsseis2seis.triggered.connect(self.doConvertPsSeis2Seis)
        #
        self.actioncalcmathattribsingle.triggered.connect(self.doCalcMathAttribSingle)
        self.actioncalcmathattribmultiple.triggered.connect(self.doCalcMathAttribMultiple)
        #
        self.actionplot1dseisz.triggered.connect(self.doPlot1DSeisZ)
        self.actionplot2dseisinl.triggered.connect(self.doPlot2DSeisInl)
        self.actionplot2dseisxl.triggered.connect(self.doPlot2DSeisXl)
        self.actionplot2dseisz.triggered.connect(self.doPlot2DSeisZ)
        self.actionplot3dslice.triggered.connect(self.doPlot3DSlice)
        self.actionplot2dpsseisshot.triggered.connect(self.doPlot2DPsSeisShot)
        self.actionplot2dpointsetcrossplt.triggered.connect(self.doPlot2DPointSetCrossplt)
        #
        self.actionsettingsgui.triggered.connect(self.doSettingsGUI)
        self.actionsettingsgeneral.triggered.connect(self.doSettingsGeneral)
        self.actionsettingsvisual.triggered.connect(self.doSettingsVisual)
        self.actionmakepytemp.triggered.connect(self.doMakePyTemp)
        self.actionexecpycode.triggered.connect(self.doExecPyCode)
        #
        self.actionmanual.triggered.connect(self.doManual)
        self.actionsupport.triggered.connect(self.doSupport)
        self.actionabout.triggered.connect(self.doAbout)
        #
        self.bkimage.setPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/background.png")).scaled(400, 400, QtCore.Qt.KeepAspectRatio))
        self.bkimage.setAlignment(QtCore.Qt.AlignCenter)


    def doNewProject(self):
        self.projname = 'New project'
        self.projpath = ''
        self.survinfo = {}
        self.seisdata = {}
        self.psseisdata = {}
        self.pointdata = {}
        #
        self.settings = {}
        self.settings['Gui'] = core_set.GUI
        self.settings['General'] = core_set.General
        self.settings['Visual'] = core_set.Visual
        #
        self.dialog.setWindowTitle("GeoPy V2019" + " <" + self.projname + ">")
        #
        self.setSettings(self.settings)


    def doOpenProject(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select Project NumPy', self.settings['General']['RootPath'],
                                        filter="Project Numpy files (*.proj.npy);; All files (*.*)")
        #
        self.projpath = os.path.split(_file[0])[0]
        _projname = os.path.basename(_file[0])
        self.projname = _projname.replace('.proj.npy', '')
        if os.path.exists(os.path.join(self.projpath, self.projname+'.proj.npy')) is False \
                or os.path.exists(os.path.join(self.projpath, self.projname+'.proj.data')) is False:
            print("doOpenProj: No Project selected")
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No Project NumPy')
            return
        print("doOpenProj: Import Project: " + os.path.join(self.projpath, self.projname+'proj.npy'))
        #
        try:
            _proj = np.load(os.path.join(self.projpath, self.projname+'.proj.npy')).item()
        except ValueError:
            print("doOpenProj: Non-dictionary Project NumPy selected")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Open Project',
                                           'Non-dictionary Project NumPy selected')
            return
        # Survey
        if 'survinfo' in _proj.keys():
            _survinfo = _proj['survinfo']
            if os.path.exists(os.path.join(self.projpath,
                                           self.projname + '.proj.data/Survey/' + 'survey' + '.npy')):
                try:
                    _survinfo = np.load(os.path.join(self.projpath,
                                                     self.projname + '.proj.data/Survey/' + 'survey' + '.npy')).item()
                except ValueError:
                    _survinfo = {}
            if checkSurvInfo(_survinfo):
                self.survinfo = _survinfo
        else:
            self.survinfo = {}
        # Seismic
        if 'survinfo' in _proj.keys() and 'seisdata' in _proj.keys():
            _seisdata = {}
            for key in _proj['seisdata'].keys():
                if os.path.exists(os.path.join(self.projpath,
                                               self.projname+'.proj.data/Seismic/'+key+'.npy')):
                    try:
                        _seisdata[key] = np.load(os.path.join(self.projpath,
                                                              self.projname + '.proj.data/Seismic/' + key + '.npy'))
                    except ValueError:
                        _seisdata[key] = []
            if checkSeisData(_seisdata, self.survinfo):
                self.seisdata = _seisdata
            else:
                self.seisdata = {}
        else:
            self.seisdata = {}
        # Pre-stack seismic
        if 'psseisdata' in _proj.keys():
            _psseisdata = {}
            for key in _proj['psseisdata'].keys():
                if os.path.exists(os.path.join(self.projpath,
                                               self.projname + '.proj.data/PsSeismic/' + key + '.npy')):
                    try:
                        _psseisdata[key] = np.load(os.path.join(self.projpath,
                                                                self.projname + '.proj.data/PsSeismic/' + key + '.npy')).item()
                    except ValueError:
                        _psseisdata[key] = {}
            if checkPsSeisData(_psseisdata):
                self.psseisdata = _psseisdata
            else:
                self.psseisdata = _psseisdata
        else:
            self.psseisdata = {}
        # PointSet
        if 'pointdata' in _proj.keys():
            _pointdata = {}
            for key in _proj['pointdata'].keys():
                if os.path.exists(os.path.join(self.projpath,
                                               self.projname+'.proj.data/PointSet/'+key+'.npy')):
                    try:
                        _pointdata[key] = np.load(os.path.join(self.projpath,
                                                               self.projname + '.proj.data/PointSet/' + key + '.npy')).item()
                    except ValueError:
                        _pointdata[key] = {}
            if checkPointData(_pointdata):
                self.pointdata = _pointdata
            else:
                self.pointdata = {}
        else:
            self.pointdata = {}
        # Settings
        if 'settings' in _proj.keys():
            _settings = _proj['settings']
            if os.path.exists(os.path.join(self.projpath,
                                           self.projname + '.proj.data/Settings/' + 'settings' + '.npy')):
                try:
                    _settings = np.load(os.path.join(self.projpath,
                                                     self.projname + '.proj.data/Settings/' + 'settings' + '.npy')).item()
                except ValueError:
                    _settings = {}
            if checkSettings(_settings):
                self.settings = _settings
            # else:
            #     self.settings = {}
        # else:
        #     self.settings = {}
        #
        self.dialog.setWindowTitle("GeoPy V2019" + " <" + self.projname + ">")
        self.settings['General']['RootPath'] = self.projpath
        #
        self.setSettings(self.settings)
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Open Project",
                                          "Project " + self.projname + " loaded successfully")


    def doSaveProject(self):
        self.refreshMsgBox()
        #
        if len(self.projpath) > 1:
            saveProject(survinfo=self.survinfo, seisdata=self.seisdata,
                        psseisdata=self.psseisdata,
                        pointdata=self.pointdata,
                        settings=self.settings,
                        savepath=self.projpath, savename=self.projname)
            #
            QtWidgets.QMessageBox.information(self.msgbox,
                                              "Save Project",
                                              "Project " + self.projname + " saved successfully")
        else:
            self.doSaveasProject()


    def doSaveasProject(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Select Project NumPy', self.settings['General']['RootPath'],
                                        filter="Project NumPy files (*.proj.npy);; All files (*.*)")
        if len(_file[0]) > 0:
            self.projpath = os.path.split(_file[0])[0]
            _name = os.path.split(_file[0])[1]
            self.projname = _name.replace('.proj.npy', '')
            #
            self.dialog.setWindowTitle("GeoPy V2019" + " <" + self.projname + ">")
            self.settings['General']['RootPath'] = self.projpath
            #
            saveProject(survinfo=self.survinfo, seisdata=self.seisdata,
                        psseisdata=self.psseisdata,
                        pointdata=self.pointdata,
                        settings=self.settings,
                        savepath=self.projpath, savename=self.projname)
            #
            QtWidgets.QMessageBox.information(self.msgbox,
                                              "Save Project",
                                              "Project " + self.projname + " saved successfully")


    def doImportSurveyManual(self):
        _importsurvey = QtWidgets.QDialog()
        _gui = gui_importsurveymanual()
        _gui.survinfo = self.survinfo
        _gui.setupGUI(_importsurvey)
        _importsurvey.exec_()
        self.survinfo = _gui.survinfo
        _importsurvey.show()


    def doImportSurveyNpy(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select Survey NumPy', self.settings['General']['RootPath'],
                                        filter="Survey Numpy files (*.srv.npy);; All files (*.*)")
        if os.path.exists(_file[0]) is False:
            print("ImportSurveyNpy: No NumPy selected for import")
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No NumPy selected for import')
            return
        print("ImportSurveyNpy: Import Survey Numpy: " + _file[0])
        try:
            _survinfo = np.load(_file[0]).item()
            #
            if checkSurvInfo(_survinfo) is False:
                print("ImportSurveyNpy: No survey NumPy selected for import")
                QtWidgets.QMessageBox.critical(self.msgbox,
                                               'Import NumPy',
                                               'No NumPy selected for import')
                return
            #
            self.survinfo = _survinfo
        except ValueError:
            print("ImportSurveyNpy: Numpy dictionary expected")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import NumPy',
                                           'Numpy dictionary expected')
            return
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Survey NumPy",
                                          "Survey imported successfully")
        #
        self.checkSurvInfo()
        #
        return


    def doImportSeisSegy(self):
        _importsegy = QtWidgets.QDialog()
        _gui = gui_importseissegy()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_importsegy)
        _importsegy.exec_()
        self.survinfo = _gui.survinfo
        self.seisdata = _gui.seisdata
        _importsegy.show()


    def doImportSeisNpy(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select Seismic NumPy', self.settings['General']['RootPath'],
                                        filter="Seismic NumPy files (*.seis.npy);; All files (*.*)")
        if os.path.exists(_file[0]) is False:
            print("ImportSeisNpy: No NumPy selected for import")
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No NumPy selected for import')
            return
        print("ImportSeisNpy: Import Seismic Numpy: " + _file[0])
        try:
            _seisdata = np.load(_file[0]).item()
            if 'Inline' not in _seisdata.keys() \
                or 'Crossline' not in _seisdata.keys() \
                or 'Z' not in _seisdata.keys():
                print("ImportSeisNpy: NumPy dictionary contains no Inline, Crossline, Z keys")
                QtWidgets.QMessageBox.critical(self.msgbox,
                                               'Import Seismic NumPy',
                                               'NumPy dictionary contains no Inline, Crossline, Z keys')
                return
            _survinfo = seis_ays.getSeisInfoFrom2DMat(basic_mdt.exportMatDict(_seisdata, ['Inline', 'Crossline', 'Z']))
            _seisdata.pop('Inline')
            _seisdata.pop('Crossline')
            _seisdata.pop('Z')
        except ValueError:
            _npydata = np.load(_file[0])
            _filename = (os.path.basename(_file[0])).replace('.seis.npy', '')
            #
            if np.ndim(_npydata)<=1 or np.ndim(_npydata)>=4:
                print("ImportSeisNpy: NumPy matrix shall be 2D or 3D")
                QtWidgets.QMessageBox.critical(self.msgbox,
                                               'Import Seismic NumPy',
                                               'NumPy matrix shall be 2D or 3D')
                return
            if np.ndim(_npydata) == 2:
                if np.shape(_npydata)[1] < 4:
                    print("ImportSeisNpy: 2D NumPy matrix shall contain at least 4 columns")
                    QtWidgets.QMessageBox.critical(self.msgbox,
                                                   'Import Seismic NumPy',
                                                   '2D NumPy matrix shall contain at least 4 columns')
                    return
                _survinfo = seis_ays.getSeisInfoFrom2DMat(_npydata)
                _npydata = _npydata[:, 3:]
            if np.ndim(_npydata) == 3:
                if checkSurvInfo(self.survinfo) \
                    and self.survinfo['ZNum'] == np.shape(_npydata)[0] \
                    and self.survinfo['XLNum'] == np.shape(_npydata)[1] \
                    and self.survinfo['ILNum'] == np.shape(_npydata)[2]:
                    _survinfo = self.survinfo
                else:
                    _survinfo = seis_ays.createSeisInfoFrom3DMat(_npydata)
                _npydata = np.reshape(np.transpose(_npydata, [2, 1, 0]), [-1, 1])

            _seisdata = {}
            _seisdata[_filename] = _npydata
        #
        # add new data to seisdata
        if checkSurvInfo(self.survinfo) is False:
            self.seisdata = _seisdata
            self.survinfo = _survinfo
        else:
            if checkSurvInfo(_survinfo) \
                    and np.array_equal(self.survinfo['ILRange'], _survinfo['ILRange']) \
                    and np.array_equal(self.survinfo['XLRange'], _survinfo['XLRange']) \
                    and np.array_equal(self.survinfo['ZRange'], _survinfo['ZRange']):
                for key in _seisdata.keys():
                    if key in self.seisdata.keys():
                        reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Seismic NumPy',
                                                               key + ' already exists. Overwrite?',
                                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                               QtWidgets.QMessageBox.No)
                        if reply == QtWidgets.QMessageBox.No:
                            return
                    self.seisdata[key] = _seisdata[key]
            else:
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Seismic NumPy',
                                                       'Survey does not match with imported seismic. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
                self.seisdata = _seisdata
                self.survinfo = _survinfo
        #
        self.checkSurvInfo()
        self.checkSeisData()
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Seismic NumPy",
                                          "NumPy imported successfully")
        #
        return


    def doImportSeisImageSet(self):
        _importimage = QtWidgets.QDialog()
        _gui = gui_importseisimageset()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_importimage)
        _importimage.exec_()
        self.seisdata = _gui.seisdata
        self.survinfo = _gui.survinfo
        _importimage.show()


    def doImportPsSeisNpy(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select Pre-stack Seismic NumPy', self.settings['General']['RootPath'],
                                        filter="Pre-stack Seismic NumPy files (*.psseis.npy);; All files (*.*)")
        if os.path.exists(_file[0]) is False:
            print("doImportPsSeisNpy: No NumPy selected for import")
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No NumPy selected for import')
            return
        print("doImportPsSeisNpy: Import Numpy: " + _file[0])
        try:
            _psseisdata = np.load(_file[0]).item()
        except ValueError:
            _npydata = np.load(_file[0])
            if np.ndim(_npydata) == 2:
                _npydata = np.expand_dims(_npydata, axis=2)
            #
            _psseisdata = {}
            _filename = (os.path.basename(_file[0])).replace('.psseis.npy', '')
            _psseisdata[_filename] = {}
            for _i in range(np.shape(_npydata)[2]):
                _psseisdata[_filename][str(_i)] = {}
                _psseisdata[_filename][str(_i)]['ShotData'] = _npydata[:, :, _i]
                _psseisdata[_filename][str(_i)]['ShotInfo'] = psseis_ays.createShotInfo(_npydata[:, :, _i])
        #
        # add new data to pointdata
        if checkPsSeisData(self.psseisdata) is False:
            self.psseisdata = _psseisdata
        else:
            for key in _psseisdata.keys():
                if key in self.psseisdata.keys():
                    reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Pre-stack Seismic NumPy',
                                                           key + ' already exists. Overwrite?',
                                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                           QtWidgets.QMessageBox.No)
                    if reply == QtWidgets.QMessageBox.No:
                        return
                self.psseisdata[key] = _psseisdata[key]
        #
        self.checkPsSeisData()
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Pre-stack Seismic NumPy",
                                          "NumPy imported successfully")
        #
        return


    def doImportPointSetFile(self):
        _importpoint = QtWidgets.QDialog()
        _gui = gui_importpointsetfile()
        _gui.pointdata = self.pointdata.copy()
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_importpoint)
        _importpoint.exec()
        self.pointdata = _gui.pointdata.copy()
        _importpoint.show()


    def doImportPointSetNpy(self):
        self.refreshMsgBox()
        #
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select PointSet NumPy', self.settings['General']['RootPath'],
                                        filter="PointSet NumPy files (*.pts.npy);; All files (*.*)")
        if os.path.exists(_file[0]) is False:
            print("ImportPointSetNpy: No NumPy selected for import")
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Import NumPy',
            #                                'No NumPy selected for import')
            return
        print("ImportPointSetNpy: Import Numpy: " + _file[0])
        try:
            _pointdata = np.load(_file[0]).item()
        except ValueError:
            _npydata = np.load(_file[0])
            if np.ndim(_npydata) != 2:
                print("ImportPointSetNpy: NumPy matrix shall be 2D")
                QtWidgets.QMessageBox.critical(self.msgbox,
                                               'Import PointSet NumPy',
                                               'NumPy matrix shall be 2D')
                return
            _ncol = np.shape(_npydata)[1]
            if _ncol < 3:
                print("ImportPointSetNpy: 2D NumPy matrix shall contain at least 3 columns")
                QtWidgets.QMessageBox.critical(self.msgbox,
                                               'Import PointSet NumPy',
                                               '2D NumPy matrix shall contain at least 3 columns')
                return
            _pointdata = {}
            _filename = (os.path.basename(_file[0])).replace('.pts.npy', '')
            _pointdata[_filename] = {}
            _pointdata[_filename]['Inline'] = _npydata[:, 0:1]
            _pointdata[_filename]['Crossline'] = _npydata[:, 1:2]
            _pointdata[_filename]['Z'] = _npydata[:, 2:3]
            for _i in range(_ncol-3):
                _pointdata[_filename]['property_'+str(_i+1)] = _npydata[:, _i+3:_i+4]
        #
        # add new data to pointdata
        if checkPointData(self.pointdata) is False:
            self.pointdata = _pointdata
        else:
            for key in _pointdata.keys():
                if key in self.pointdata.keys():
                    reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import PointSet NumPy',
                                                           key + ' already exists. Overwrite?',
                                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                           QtWidgets.QMessageBox.No)
                    if reply == QtWidgets.QMessageBox.No:
                        return
                self.pointdata[key] = _pointdata[key]
        #
        self.checkPointData()
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import PointSet NumPy",
                                          "NumPy imported successfully")
        #
        return


    def doExportSurvey(self):
        _exportsurvey = QtWidgets.QDialog()
        _gui = gui_exportsurvey()
        _gui.survinfo = self.survinfo
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportsurvey)
        _exportsurvey.exec_()
        _exportsurvey.show()


    def doExportSeisSegy(self):
        _exportsegy = QtWidgets.QDialog()
        _gui = gui_exportseissegy()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportsegy)
        _exportsegy.exec_()
        _exportsegy.show()


    def doExportSeisNpy(self):
        _exportnpy = QtWidgets.QDialog()
        _gui = gui_exportseisnpy()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportnpy)
        _exportnpy.exec_()
        _exportnpy.show()


    def doExportSeisImageSet(self):
        _exportimage = QtWidgets.QDialog()
        _gui = gui_exportseisimageset()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportimage)
        _exportimage.exec_()
        _exportimage.show()


    def doExportPsSeisNpy(self):
        _exportnpy = QtWidgets.QDialog()
        _gui = gui_exportpsseisnpy()
        _gui.psseisdata = self.psseisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportnpy)
        _exportnpy.exec_()
        _exportnpy.show()


    def doExportPointSetNpy(self):
        _exportnpy = QtWidgets.QDialog()
        _gui = gui_exportpointsetnpy()
        _gui.pointdata = self.pointdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportnpy)
        _exportnpy.exec_()
        _exportnpy.show()


    def doQuit(self):
        self.refreshMsgBox()
        reply = QtWidgets.QMessageBox.question(self.msgbox, 'GeoPy', 'Are you sure to quit GeoPy?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            return


    def doManageSurvey(self):
        _managesurvey = QtWidgets.QDialog()
        _gui = gui_managesurvey()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.setupGUI(_managesurvey)
        _managesurvey.exec()
        self.survinfo = _gui.survinfo
        self.seisdata = _gui.seisdata
        _managesurvey.show()


    def doManageSeis(self):
        _manageseis = QtWidgets.QDialog()
        _gui = gui_manageseis()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_manageseis)
        _manageseis.exec()
        self.seisdata = _gui.seisdata
        self.survinfo = _gui.survinfo
        _manageseis.show()


    def doManagePsSeis(self):
        _managepsseis = QtWidgets.QDialog()
        _gui = gui_managepsseis()
        _gui.psseisdata = self.psseisdata
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_managepsseis)
        _managepsseis.exec()
        self.psseisdata = _gui.psseisdata
        _managepsseis.show()


    def doManagePointSet(self):
        _managepoint = QtWidgets.QDialog()
        _gui = gui_managepointset()
        _gui.pointdata = self.pointdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.linestyle = self.settings['Visual']['Line']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_managepoint)
        _managepoint.exec()
        self.pointdata = _gui.pointdata
        _managepoint.show()


    def doConvertSeis2PointSet(self):
        _convert = QtWidgets.QDialog()
        _gui = gui_convertseis2pointset()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.pointdata = self.pointdata
        _gui.setupGUI(_convert)
        _convert.exec()
        self.pointdata = _gui.pointdata
        _convert.show()


    def doConvertPointSet2Seis(self):
        _convert = QtWidgets.QDialog()
        _gui = gui_convertpointset2seis()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.pointdata = self.pointdata
        _gui.setupGUI(_convert)
        _convert.exec()
        self.seisdata = _gui.seisdata
        _convert.show()


    def doConvertPsSeis2Seis(self):
        _convert = QtWidgets.QDialog()
        _gui = gui_convertpsseis2seis()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.psseisdata = self.psseisdata
        _gui.setupGUI(_convert)
        _convert.exec()
        self.survinfo = _gui.survinfo
        self.seisdata = _gui.seisdata
        _convert.show()


    def doCalcMathAttribSingle(self):
        _attrib = QtWidgets.QDialog()
        _gui = gui_calcmathattribsingle()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_attrib)
        _attrib.exec()
        self.seisdata = _gui.seisdata
        _attrib.show()


    def doCalcMathAttribMultiple(self):
        _attrib = QtWidgets.QDialog()
        _gui = gui_calcmathattribmultiple()
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_attrib)
        _attrib.exec()
        self.seisdata = _gui.seisdata
        _attrib.show()


    def doPlot1DSeisZ(self):
        _plot1dz = QtWidgets.QDialog()
        _gui = gui_plot1dseisz()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.linestyle = self.settings['Visual']['Line']
        _gui.playerconfiginl = self.settings['Visual']['Player']
        _gui.playerconfigxl = {}
        _gui.playerconfigxl['First'] = 'G'
        _gui.playerconfigxl['Previous'] = 'H'
        _gui.playerconfigxl['Backward'] = 'B'
        _gui.playerconfigxl['Pause'] = 'N'
        _gui.playerconfigxl['Forward'] = 'M'
        _gui.playerconfigxl['Next'] = 'J'
        _gui.playerconfigxl['Last'] = 'K'
        _gui.playerconfigxl['Interval'] = _gui.playerconfiginl['Interval']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot1dz)
        _plot1dz.exec()
        _plot1dz.show()


    def doPlot2DSeisInl(self):
        _plot2dinl = QtWidgets.QDialog()
        _gui = gui_plot2dseisinl()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.playerconfig = self.settings['Visual']['Player']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot2dinl)
        _plot2dinl.exec()
        _plot2dinl.show()


    def doPlot2DSeisXl(self):
        _plot2dxl = QtWidgets.QDialog()
        _gui = gui_plot2dseisxl()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.playerconfig = self.settings['Visual']['Player']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot2dxl)
        _plot2dxl.exec()
        _plot2dxl.show()


    def doPlot2DSeisZ(self):
        _plot2dz = QtWidgets.QDialog()
        _gui = gui_plot2dseisz()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.playerconfig = self.settings['Visual']['Player']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot2dz)
        _plot2dz.exec()
        _plot2dz.show()


    def doPlot2DPsSeisShot(self):
        _plot2d = QtWidgets.QDialog()
        _gui = gui_plot2dpsseisshot()
        _gui.psseisdata = self.psseisdata
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.playerconfig = self.settings['Visual']['Player']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot2d)
        _plot2d.exec()
        _plot2d.show()


    def doPlot2DPointSetCrossplt(self):
        _cplt = QtWidgets.QDialog()
        _gui = gui_plot2dpointsetcrossplt()
        _gui.pointdata = self.pointdata
        _gui.linestyle = self.settings['Visual']['Line']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_cplt)
        _cplt.exec()
        _cplt.show()


    def doPlot3DSlice(self):
        self.refreshMsgBox()
        QtWidgets.QMessageBox.about(self.msgbox, "Plot 3D Seismic", "Coming soon ...")


    def doSettingsGUI(self):
        _settings = QtWidgets.QDialog()
        _gui = gui_settingsgui()
        _gui.mainwindow = self
        _gui.settings = self.settings['Gui']
        _gui.setupGUI(_settings)
        _settings.exec()
        self.settings['Gui'] = _gui.settings
        _settings.show()


    def doSettingsGeneral(self):
        _settings = QtWidgets.QDialog()
        _gui = gui_settingsgeneral()
        _gui.settings = self.settings['General']
        _gui.setupGUI(_settings)
        _settings.exec()
        self.settings['General'] = _gui.settings
        _settings.show()


    def doSettingsVisual(self):
        _settings = QtWidgets.QDialog()
        _gui = gui_settingsvisual()
        _gui.settings = self.settings['Visual']
        _gui.setupGUI(_settings)
        _settings.exec()
        self.settings['Visual'] = _gui.settings
        _settings.show()


    def doMakePyTemp(self):
        _pycode = QtWidgets.QDialog()
        _gui = gui_makepytemp()
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_pycode)
        _pycode.exec()
        _pycode.show()


    def doExecPyCode(self):
        _pycode = QtWidgets.QDialog()
        _gui = gui_execpycode()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.pointdata = self.pointdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_pycode)
        _pycode.exec()
        self.survinfo = _gui.survinfo
        self.seisdata = _gui.seisdata
        self.pointdata = _gui.pointdata
        _pycode.show()


    def doManual(self):
        self.refreshMsgBox()
        webbrowser.open("https://geopyinfo.wixsite.com/geopy/manual")
        # QtWidgets.QMessageBox.about(self.msgbox, "Manual", "Coming soon ...")


    def doSupport(self):
        webbrowser.open("https://geopyinfo.wixsite.com/geopy/support")


    def doAbout(self):
        _about = QtWidgets.QDialog()
        _gui = gui_about()
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_about)
        _about.exec()
        _about.show()


    def setSettings(self, settings):
        _dialog = QtWidgets.QDialog()
        #
        _gui = gui_settingsgui()
        _gui.mainwindow = self
        _gui.settings = settings['Gui']
        _gui.setupGUI(_dialog)
        #
        _gui = gui_settingsgeneral()
        _gui.settings = settings['General']
        _gui.setupGUI(_dialog)
        #
        _gui = gui_settingsvisual()
        _gui.settings = settings['Visual']
        _gui.setupGUI(_dialog)


    def checkSurvInfo(self):
        self.refreshMsgBox()
        #
        if checkSurvInfo(self.survinfo) is False:
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'GeoPy',
                                           'No survey found')
            return


    def checkSeisData(self):
        self.refreshMsgBox()
        #
        if checkSeisData(self.seisdata, self.survinfo) is False:
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'GeoPy',
                                            'Seismic & survey not match')
            return


    def checkPsSeisData(self):
        self.refreshMsgBox()
        #
        if checkPsSeisData(self.psseisdata) is False:
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'GeoPy',
                                           'No Pre-stack seismic found')
            return


    def checkPointData(self):
        self.refreshMsgBox()
        #
        if checkPointData(self.pointdata) is False:
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'GeoPy',
                                            'No pointset found')
            return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


class qt_mainwindow(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'GeoPy', 'Are you sure to quit GeoPy?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            event.ignore()


def gui_main(survinfo={}, seisdata={}, pointdata={},
             rootpath=os.path.dirname(__file__)[:-8],
             settings={}):
    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    MainWindow = qt_mainwindow()
    gui = mainwindow()
    if checkSurvInfo(survinfo):
        gui.survinfo = survinfo
    if checkSeisData(survinfo, seisdata):
        gui.seisdata = seisdata
    if checkPointData(pointdata):
        gui.pointdata = pointdata
    if checkSettings(settings):
        gui.settings = settings
    gui.settings['General']['RootPath'] = rootpath
    gui.setupGUI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


def checkSurvInfo(survinfo):
    return seis_ays.checkSeisInfo(survinfo)


def checkSeisData(seisdata, survinfo={}):
    if seis_ays.checkSeisInfo(survinfo) is False:
        return False
    if seisdata is None:
        return False
    for f in seisdata.keys():
        if np.shape(seisdata[f])[0] != survinfo['SampleNum']:
            return False
    return True


def checkPsSeisData(psseisdata):
    if psseisdata is None or len(psseisdata.keys()) < 1:
        return False
    for p in psseisdata.keys():
        if psseis_ays.checkPsSeis(psseisdata[p]) is False:
            return False
    return True


def checkPointData(pointdata):
    if pointdata is None or len(pointdata.keys()) < 1:
        return False
    for p in pointdata.keys():
        if pointdata[p] is None:
            return False
        if point_ays.checkPoint(pointdata[p]) is False:
            return False
    return True


def checkSettings(setting):
    if len(setting.keys()) < 1:
        return False
    if 'Gui' not in setting.keys() or 'General' not in setting.keys() or 'Visual' not in setting.keys():
        return False
    if core_set.checkSettings(gui=setting['Gui'], general=setting['General'], visual=setting['Visual']) is False:
        return False
    #
    return True


def saveProject(survinfo={}, seisdata={}, psseisdata={}, pointdata={}, settings={},
                savepath='', savename='gpy'):
    _proj = {}
    _proj['survinfo'] = survinfo
    _proj['seisdata'] = {}
    _proj['psseisdata'] = {}
    _proj['pointdata'] = {}
    _proj['settings'] = settings
    #
    if os.path.exists(os.path.join(savepath, savename + '.proj.data')) is False:
        os.mkdir(os.path.join(savepath, savename + '.proj.data'))
    # save survey
    if os.path.exists(os.path.join(savepath, savename + '.proj.data/Survey')) is False:
        os.mkdir(os.path.join(savepath, savename + '.proj.data/Survey'))
    np.save(os.path.join(savepath, savename + '.proj.data/Survey/' + 'survey' + '.npy'), survinfo)
    # save seismic data
    if os.path.exists(os.path.join(savepath, savename + '.proj.data/Seismic')) is False:
        os.mkdir(os.path.join(savepath, savename + '.proj.data/Seismic'))
    for f in os.listdir(os.path.join(savepath, savename + '.proj.data/Seismic')):
        os.remove(os.path.join(savepath, savename + '.proj.data/Seismic/' + f))
    for key in seisdata.keys():
        _proj['seisdata'][key] = {}
        np.save(os.path.join(savepath, savename + '.proj.data/Seismic/' + key + '.npy'), seisdata[key])
    # save psseismic data
    if os.path.exists(os.path.join(savepath, savename + '.proj.data/PsSeismic')) is False:
        os.mkdir(os.path.join(savepath, savename + '.proj.data/PsSeismic'))
    for f in os.listdir(os.path.join(savepath, savename + '.proj.data/PsSeismic')):
        os.remove(os.path.join(savepath, savename + '.proj.data/PsSeismic/' + f))
    for key in psseisdata.keys():
        _proj['psseisdata'][key] = {}
        np.save(os.path.join(savepath, savename + '.proj.data/PsSeismic/' + key + '.npy'), psseisdata[key])
    # save pointset data
    if os.path.exists(os.path.join(savepath, savename + '.proj.data/PointSet')) is False:
        os.mkdir(os.path.join(savepath, savename + '.proj.data/PointSet'))
    for f in os.listdir(os.path.join(savepath, savename + '.proj.data/PointSet')):
        os.remove(os.path.join(savepath, savename + '.proj.data/PointSet/' + f))
    for key in pointdata.keys():
        _proj['pointdata'][key] = {}
        np.save(os.path.join(savepath, savename + '.proj.data/PointSet/' + key + '.npy'), pointdata[key])
    # save settings
    if os.path.exists(os.path.join(savepath, savename + '.proj.data/Settings')) is False:
        os.mkdir(os.path.join(savepath, savename + '.proj.data/Settings'))
    np.save(os.path.join(savepath, savename + '.proj.data/Settings/' + 'settings' + '.npy'), settings)
    #
    np.save(os.path.join(savepath, savename + '.proj.npy'), _proj)


if __name__ == "__main__":
    gui_main()
    # app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # gui = gui_mainwindow()
    # gui.setupGUI(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())


