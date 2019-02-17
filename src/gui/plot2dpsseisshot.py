#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# Create a window for plot pre-stack seismic shots


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4])
from basic.data import data as basic_data
from core.settings import settings as core_set
from psseismic.analysis import analysis as psseis_ays
from psseismic.visualization import visualization as psseis_vis
from vis.colormap import colormap as vis_cmap
from gui.configplayer import configplayer as gui_configplayer

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class plot2dpsseisshot(object):

    psseisdata = {}
    plotstyle = core_set.Visual['Image']
    playerconfig = core_set.Visual['Player']
    fontstyle = core_set.Visual['Font']
    #
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, Plot2DPsSeisShot):
        Plot2DPsSeisShot.setObjectName("Plot2DPsSeisShot")
        Plot2DPsSeisShot.setFixedSize(400, 450)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/gather.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        Plot2DPsSeisShot.setWindowIcon(icon)
        #
        self.lblpsseis = QtWidgets.QLabel(Plot2DPsSeisShot)
        self.lblpsseis.setObjectName("lblpsseis")
        self.lblpsseis.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwgpsseis = QtWidgets.QListWidget(Plot2DPsSeisShot)
        self.lwgpsseis.setObjectName("lwgpsseis")
        self.lwgpsseis.setGeometry(QtCore.QRect(160, 10, 230, 200))
        self.lwgpsseis.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblpsshot = QtWidgets.QLabel(Plot2DPsSeisShot)
        self.lblpsshot.setObjectName("lblpsshot")
        self.lblpsshot.setGeometry(QtCore.QRect(10, 230, 150, 30))
        self.slbpsshot = QtWidgets.QScrollBar(Plot2DPsSeisShot)
        self.slbpsshot.setObjectName("slbpsshot")
        self.slbpsshot.setOrientation(QtCore.Qt.Horizontal)
        self.slbpsshot.setGeometry(QtCore.QRect(160, 230, 170, 30))
        self.ldtpsshot = QtWidgets.QLineEdit(Plot2DPsSeisShot)
        self.ldtpsshot.setObjectName("ldtpsshot")
        self.ldtpsshot.setGeometry(QtCore.QRect(340, 230, 50, 30))
        self.ldtpsshot.setAlignment(QtCore.Qt.AlignCenter)
        self.lblcmap = QtWidgets.QLabel(Plot2DPsSeisShot)
        self.lblcmap.setObjectName("lblcmap")
        self.lblcmap.setGeometry(QtCore.QRect(10, 270, 150, 30))
        self.cbbcmap = QtWidgets.QComboBox(Plot2DPsSeisShot)
        self.cbbcmap.setObjectName("cbbcmap")
        self.cbbcmap.setGeometry(QtCore.QRect(160, 270, 170, 30))
        self.cbxflip = QtWidgets.QCheckBox(Plot2DPsSeisShot)
        self.cbxflip.setObjectName("cbxflip")
        self.cbxflip.setGeometry(QtCore.QRect(340, 270, 50, 30))
        self.lblrange = QtWidgets.QLabel(Plot2DPsSeisShot)
        self.lblrange.setObjectName("lblrange")
        self.lblrange.setGeometry(QtCore.QRect(10, 310, 150, 30))
        self.ldtmin = QtWidgets.QLineEdit(Plot2DPsSeisShot)
        self.ldtmin.setObjectName("ldtmin")
        self.ldtmin.setGeometry(QtCore.QRect(160, 310, 90, 30))
        self.ldtmin.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmax = QtWidgets.QLineEdit(Plot2DPsSeisShot)
        self.ldtmax.setObjectName("ldtmax")
        self.ldtmax.setGeometry(QtCore.QRect(300, 310, 90, 30))
        self.ldtmax.setAlignment(QtCore.Qt.AlignCenter)
        self.lblrangeto = QtWidgets.QLabel(Plot2DPsSeisShot)
        self.lblrangeto.setObjectName("lblrangeto")
        self.lblrangeto.setGeometry(QtCore.QRect(250, 310, 50, 30))
        self.lblrangeto.setAlignment(QtCore.Qt.AlignCenter)
        #
        self.btnconfigplayer = QtWidgets.QPushButton(Plot2DPsSeisShot)
        self.btnconfigplayer.setObjectName("btnconfigplayer")
        self.btnconfigplayer.setGeometry(QtCore.QRect(230, 350, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/video.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnconfigplayer.setIcon(icon)
        #
        self.btnplotshot = QtWidgets.QPushButton(Plot2DPsSeisShot)
        self.btnplotshot.setObjectName("btnplotshot")
        self.btnplotshot.setGeometry(QtCore.QRect(120, 400, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/gather.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnplotshot.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(Plot2DPsSeisShot)
        self.msgbox.setObjectName("msgbox")
        _center_x = Plot2DPsSeisShot.geometry().center().x()
        _center_y = Plot2DPsSeisShot.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(Plot2DPsSeisShot)
        QtCore.QMetaObject.connectSlotsByName(Plot2DPsSeisShot)



    def retranslateGUI(self, Plot2DPsSeisShot):
        self.dialog = Plot2DPsSeisShot
        #
        _translate = QtCore.QCoreApplication.translate
        Plot2DPsSeisShot.setWindowTitle(_translate("Plot2DPsSeisShot", "2D Window: Pre-stack Gather"))
        self.lblpsseis.setText(_translate("Plot2DPsSeisShot", "Select target pre-stack:"))
        if self.checkPsSeisData():
            _firstpsseis = None
            for i in sorted(self.psseisdata.keys()):
                item = QtWidgets.QListWidgetItem(self.lwgpsseis)
                item.setText(_translate("Plot2DPsSeisShot", i))
                self.lwgpsseis.addItem(item)
                if _firstpsseis is None:
                    _firstpsseis = item
            self.lwgpsseis.setCurrentItem(_firstpsseis)
        self.lwgpsseis.itemSelectionChanged.connect(self.changeLwgPsseis)
        #
        self.lblpsshot.setText(_translate("Plot2DPsSeisShot", "Select pre-stack gather:"))
        self.ldtpsshot.setEnabled(False)
        if (self.lwgpsseis.currentItem() is not None) \
                and (self.lwgpsseis.currentItem().text() in self.psseisdata.keys()):
            _shotlist = list(sorted(self.psseisdata[_firstpsseis.text()].keys()))
            _slicemin = 0
            _slicemax = len(_shotlist) - 1
        else:
            _shotlist = []
            _slicemin = 0
            _slicemax = 0
        self.slbpsshot.setMinimum(_slicemin)
        self.slbpsshot.setMaximum(_slicemax)
        self.slbpsshot.setValue(_slicemin)
        if len(_shotlist) > _slicemin:
            self.ldtpsshot.setText(_translate("Plot2DPsSeisShot", _shotlist[_slicemin]))
        else:
            self.ldtpsshot.setText(_translate("Plot2DPsSeisShot", ''))
        self.slbpsshot.valueChanged.connect(self.changeSlbPsshot)
        #
        self.lblcmap.setText(_translate("Plot2DXlSlice", "\t  Color map:"))
        self.cbbcmap.addItems(vis_cmap.ColorMapList)
        for _i in range(len(vis_cmap.ColorMapList)):
            self.cbbcmap.setItemIcon(_i, QtGui.QIcon(
                QtGui.QPixmap(os.path.join(self.iconpath, "icons/cmap_" + vis_cmap.ColorMapList[_i] + ".png")).scaled(80, 30)))
        self.cbbcmap.setCurrentIndex(list.index(vis_cmap.ColorMapList, self.plotstyle['Colormap']))
        #
        self.cbxflip.setText(_translate("Plot2DPsSeisShot", ""))
        self.cbxflip.setIcon(QtGui.QIcon(
            QtGui.QPixmap(os.path.join(self.iconpath, "icons/flip.png")).scaled(80, 80)))
        #
        self.lblrange.setText(_translate("Plot2DPsSeisShot", "\t       Range:"))
        self.lblrangeto.setText(_translate("Plot2DPsSeisShot", "~~~"))
        if (self.lwgpsseis.currentItem() is not None) \
                and (self.lwgpsseis.currentItem().text() in self.psseisdata.keys()):
            _min, _max = self.getShotRange(self.lwgpsseis.currentItem().text())
            self.ldtmin.setText(_translate("Plot2DPsSeisShot", str(_min)))
            self.ldtmax.setText(_translate("Plot2DPsSeisShot", str(_max)))
        #
        self.btnconfigplayer.setText(_translate("Plot2DPsSeisShot", "Player Configuration"))
        self.btnconfigplayer.clicked.connect(self.clickBtnConfigPlayer)
        #
        self.btnplotshot.setText(_translate("Plot2DPsSeisShot", "Pre-stack Gather Viewer"))
        self.btnplotshot.setDefault(True)
        self.btnplotshot.clicked.connect(self.clickBtnPlotShot)


    def changeLwgPsseis(self):
        if len(self.lwgpsseis.selectedItems()) > 0:
            if (self.lwgpsseis.currentItem() is not None) \
                and (self.lwgpsseis.currentItem().text() in self.psseisdata.keys()):
                _shotlist = list(sorted(self.psseisdata[self.lwgpsseis.currentItem().text()].keys()))
                self.slbpsshot.setMinimum(0)
                self.slbpsshot.setMaximum(len(_shotlist) - 1)
                self.slbpsshot.setValue(0)
                self.ldtpsshot.setText(_shotlist[0])
                _min, _max = self.getShotRange(self.lwgpsseis.currentItem().text())
                self.ldtmin.setText(str(_min))
                self.ldtmax.setText(str(_max))
        else:
            self.slbpsshot.setMinimum(0)
            self.slbpsshot.setMaximum(0)
            self.ldtpsshot.setText('')
            self.ldtmin.setText('')
            self.ldtmax.setText('')


    def changeSlbPsshot(self):
        _shotlist = list(sorted(self.psseisdata[self.lwgpsseis.currentItem().text()].keys()))
        self.ldtpsshot.setText(_shotlist[self.slbpsshot.value()])


    def clickBtnConfigPlayer(self):
        _config = QtWidgets.QDialog()
        _gui = gui_configplayer()
        _gui.playerconfig = {}
        _gui.playerconfig['Gather'] = self.playerconfig
        _gui.setupGUI(_config)
        _config.exec()
        self.playerconfig = _gui.playerconfig['Gather']
        _config.show()


    def clickBtnPlotShot(self):
        self.refreshMsgBox()
        #
        _psseislist = self.lwgpsseis.selectedItems()
        if len(_psseislist) < 1:
            print("Plot2DPsSeisShot: No pre-stack selected for plot")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           '2D Window: Pre-stack Gather',
                                           'No pre-stack selected for plot')
            return
        #
        _cmap = self.cbbcmap.currentIndex()
        _flip = self.cbxflip.isChecked()
        _min = basic_data.str2float(self.ldtmin.text())
        _max = basic_data.str2float(self.ldtmax.text())
        if _min is False or _max is False:
            print("Plot2DPsSeisShot: Non-float range specified for plot")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           '2D Window: Pre-stack Gather',
                                           'Non-float range specified for plot')
            return
        #
        for i in range(len(_psseislist)):
            print("Plot2DPsSeisShot: Plot %d of %d pre-stack: %s" % (i + 1, len(_psseislist), _psseislist[i].text()))
            _data = self.psseisdata[_psseislist[i].text()]
            #
            _shotlist = list(sorted(self.psseisdata[_psseislist[i].text()].keys()))
            if self.slbpsshot.value() >= len(_shotlist):
                _sls = _shotlist[0]
            else:
                _sls = _shotlist[self.slbpsshot.value()]
            psseis_vis.plotPsSeisShotPlayer(_data, initshot=_sls,
                                            titlesurf=' in ' + _psseislist[i].text(),
                                            valuemin=_min,
                                            valuemax=_max,
                                            colormap=vis_cmap.ColorMapList[_cmap],
                                            flipcmap=_flip, colorbaron=True,
                                            interpolation=self.plotstyle['Interpolation'].lower(),
                                            playerconfig=self.playerconfig,
                                            fontstyle=self.fontstyle,
                                            qicon=QtGui.QIcon(os.path.join(self.iconpath, "icons/logo.png"))
                                            )
        return


    def getShotRange(self, f):
        _min = -1
        _max = 1
        if f in self.psseisdata.keys() and psseis_ays.checkPsSeis(self.psseisdata[f]):
            for k in self.psseisdata[f].keys():
                _vmin = np.min(self.psseisdata[f][k]['ShotData'])
                _vmax = np.max(self.psseisdata[f][k]['ShotData'])
                if _vmin < _min:
                    _min = _vmin
                if _vmax > _max:
                    _max = _vmax
        return _min, _max


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkPsSeisData(self):
        self.refreshMsgBox()
        #
        for f in self.psseisdata.keys():
            if psseis_ays.checkPsSeis(self.psseisdata[f]) is False:
                return False
        return True


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Plot2DPsSeisShot = QtWidgets.QWidget()
    gui = plot2dpsseisshot()
    gui.setupGUI(Plot2DPsSeisShot)
    Plot2DPsSeisShot.show()
    sys.exit(app.exec_())
