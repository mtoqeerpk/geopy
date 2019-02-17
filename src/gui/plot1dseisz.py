#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     Movember 2018                                                                   #
#                                                                                           #
#############################################################################################

# Create a window for plot seismic traces


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4])
from basic.data import data as basic_data
from core.settings import settings as core_set
from seismic.analysis import analysis as seis_ays
from seismic.visualization import visualization as seis_vis
from gui.configlineplotting import configlineplotting as gui_configlineplotting
from gui.configplayer import configplayer as gui_configplayer

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class plot1dseisz(object):

    survinfo = {}
    seisdata = {}
    linestyle = core_set.Visual['Line']
    playerconfiginl = core_set.Visual['Player']
    playerconfigxl = core_set.Visual['Player']
    fontstyle = core_set.Visual['Font']
    #
    iconpath = os.path.dirname(__file__)
    dialog = None
    #
    lineplottingconfig = {}


    def setupGUI(self, Plot1DSeisZ):
        Plot1DSeisZ.setObjectName("Plot1DSeisZ")
        Plot1DSeisZ.setFixedSize(400, 490)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/waveform.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        Plot1DSeisZ.setWindowIcon(icon)
        #
        self.lblattrib = QtWidgets.QLabel(Plot1DSeisZ)
        self.lblattrib.setObjectName("lblattrib")
        self.lblattrib.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwgattrib = QtWidgets.QListWidget(Plot1DSeisZ)
        self.lwgattrib.setObjectName("lwgattrib")
        self.lwgattrib.setGeometry(QtCore.QRect(160, 10, 230, 200))
        self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblinl = QtWidgets.QLabel(Plot1DSeisZ)
        self.lblinl.setObjectName("lblinl")
        self.lblinl.setGeometry(QtCore.QRect(10, 230, 150, 30))
        self.slbinl = QtWidgets.QScrollBar(Plot1DSeisZ)
        self.slbinl.setObjectName("slbinl")
        self.slbinl.setOrientation(QtCore.Qt.Horizontal)
        self.slbinl.setGeometry(QtCore.QRect(160, 230, 170, 30))
        self.ldtinl = QtWidgets.QLineEdit(Plot1DSeisZ)
        self.ldtinl.setObjectName("ldtinl")
        self.ldtinl.setGeometry(QtCore.QRect(340, 230, 50, 30))
        self.ldtinl.setAlignment(QtCore.Qt.AlignCenter)
        self.lblxl = QtWidgets.QLabel(Plot1DSeisZ)
        self.lblxl.setObjectName("lblxl")
        self.lblxl.setGeometry(QtCore.QRect(10, 270, 150, 30))
        self.slbxl = QtWidgets.QScrollBar(Plot1DSeisZ)
        self.slbxl.setObjectName("slbxl")
        self.slbxl.setOrientation(QtCore.Qt.Horizontal)
        self.slbxl.setGeometry(QtCore.QRect(160, 270, 170, 30))
        self.ldtxl = QtWidgets.QLineEdit(Plot1DSeisZ)
        self.ldtxl.setObjectName("ldtxl")
        self.ldtxl.setGeometry(QtCore.QRect(340, 270, 50, 30))
        self.ldtxl.setAlignment(QtCore.Qt.AlignCenter)
        self.lblrange = QtWidgets.QLabel(Plot1DSeisZ)
        self.lblrange.setObjectName("lblrange")
        self.lblrange.setGeometry(QtCore.QRect(10, 310, 150, 30))
        self.ldtmin = QtWidgets.QLineEdit(Plot1DSeisZ)
        self.ldtmin.setObjectName("ldtmin")
        self.ldtmin.setGeometry(QtCore.QRect(160, 310, 90, 30))
        self.ldtmin.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmax = QtWidgets.QLineEdit(Plot1DSeisZ)
        self.ldtmax.setObjectName("ldtmax")
        self.ldtmax.setGeometry(QtCore.QRect(300, 310, 90, 30))
        self.ldtmax.setAlignment(QtCore.Qt.AlignCenter)
        self.lblrangeto = QtWidgets.QLabel(Plot1DSeisZ)
        self.lblrangeto.setObjectName("lblrangeto")
        self.lblrangeto.setGeometry(QtCore.QRect(250, 310, 50, 30))
        self.lblrangeto.setAlignment(QtCore.Qt.AlignCenter)
        #
        self.btnconfigline = QtWidgets.QPushButton(Plot1DSeisZ)
        self.btnconfigline.setObjectName("btnconfigline")
        self.btnconfigline.setGeometry(QtCore.QRect(230, 350, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/plotcurve.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnconfigline.setIcon(icon)
        #
        self.btnconfigplayer = QtWidgets.QPushButton(Plot1DSeisZ)
        self.btnconfigplayer.setObjectName("btnconfigplayer")
        self.btnconfigplayer.setGeometry(QtCore.QRect(230, 390, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/video.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnconfigplayer.setIcon(icon)
        #
        self.btnplot = QtWidgets.QPushButton(Plot1DSeisZ)
        self.btnplot.setObjectName("btnplot")
        self.btnplot.setGeometry(QtCore.QRect(120, 440, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/waveform.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnplot.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(Plot1DSeisZ)
        self.msgbox.setObjectName("msgbox")
        _center_x = Plot1DSeisZ.geometry().center().x()
        _center_y = Plot1DSeisZ.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(Plot1DSeisZ)
        QtCore.QMetaObject.connectSlotsByName(Plot1DSeisZ)



    def retranslateGUI(self, Plot1DSeisZ):
        self.dialog = Plot1DSeisZ
        #
        _translate = QtCore.QCoreApplication.translate
        Plot1DSeisZ.setWindowTitle(_translate("Plot1DSeisZ", "1D Window: Seismic Waveform"))
        self.lblattrib.setText(_translate("Plot1DSeisZ", "Select target properties:"))
        if (self.checkSurvInfo() is True) and (self.checkSeisData() is True):
            _firstattrib = None
            for i in sorted(self.seisdata.keys()):
                item = QtWidgets.QListWidgetItem(self.lwgattrib)
                item.setText(_translate("Plot1DSeisZ", i))
                self.lwgattrib.addItem(item)
                if _firstattrib is None:
                    _firstattrib = item
            self.lwgattrib.setCurrentItem(_firstattrib)
        self.lwgattrib.itemSelectionChanged.connect(self.changeLwgAttrib)
        #
        self.lblinl.setText(_translate("Plot1DSeisZ", "Select inline No.:"))
        if (self.checkSurvInfo() is True):
            _slices = self.survinfo['ILRange'].astype(int)
            _slicemin = np.min(_slices)
            _slicemax = np.max(_slices)
        else:
            _slicemin = 0
            _slicemax = 0
        self.slbinl.setMinimum(_slicemin)
        self.slbinl.setMaximum(_slicemax)
        self.slbinl.setValue(_slicemin)
        if (self.checkSurvInfo() is True):
            self.ldtinl.setText(_translate("Plot1DSeisZ", str(_slicemin)))
        else:
            self.ldtinl.setText(_translate("Plot1DSeisZ", ''))
        self.slbinl.valueChanged.connect(self.changeSlbInl)
        self.ldtinl.textChanged.connect(self.changeLdtInl)
        #
        self.lblxl.setText(_translate("Plot1DSeisZ", "Select crossline No.:"))
        if (self.checkSurvInfo() is True):
            _slices = self.survinfo['XLRange'].astype(int)
            _slicemin = np.min(_slices)
            _slicemax = np.max(_slices)
        else:
            _slicemin = 0
            _slicemax = 0
        self.slbxl.setMinimum(_slicemin)
        self.slbxl.setMaximum(_slicemax)
        self.slbxl.setValue(_slicemin)
        if (self.checkSurvInfo() is True):
            self.ldtxl.setText(_translate("Plot1DSeisZ", str(_slicemin)))
        else:
            self.ldtxl.setText(_translate("Plot1DSeisZ", ''))
        self.slbxl.valueChanged.connect(self.changeSlbXl)
        self.ldtxl.textChanged.connect(self.changeLdtXl)
        #
        self.lblrange.setText(_translate("Plot1DSeisZ", "\t       Range:"))
        self.lblrangeto.setText(_translate("Plot1DSeisZ", "~~~"))
        if (self.checkSurvInfo() is True) \
                and (self.checkSeisData() is True) \
                and (self.lwgattrib.currentItem() is not None):
            _min, _max = self.getAttribRange(self.lwgattrib.currentItem().text())
            self.ldtmin.setText(_translate("Plot1DSeisZ", str(_min)))
            self.ldtmax.setText(_translate("Plot1DSeisZ", str(_max)))
        #
        self.btnconfigline.setText(_translate("Plot1DSeisZ", "Waveform Configuration"))
        self.btnconfigline.clicked.connect(self.clickBtnConfigLine)
        if (self.checkSurvInfo() is True) \
                and (self.checkSeisData() is True) \
                and (self.lwgattrib.currentItem() is not None):
            _config = self.linestyle
            self.lineplottingconfig[self.lwgattrib.currentItem().text()] = _config
        #
        self.btnconfigplayer.setText(_translate("Plot1DSeisZ", "Player Configuration"))
        self.btnconfigplayer.clicked.connect(self.clickBtnConfigPlayer)
        #
        self.btnplot.setText(_translate("Plot1DSeisZ", "Seismic Waveform Viewer"))
        self.btnplot.setDefault(True)
        self.btnplot.clicked.connect(self.clickBtnPlot)


    def changeLwgAttrib(self):
        if len(self.lwgattrib.selectedItems()) > 0:
            # if len(self.lwgattrib.selectedItems()) > 1:
            #     self.ldtmin.setEnabled(False)
            #     self.ldtmax.setEnabled(False)
            # else:
            #     self.ldtmin.setEnabled(True)
            #     self.ldtmax.setEnabled(True)
            _slices = self.survinfo['ILRange'].astype(int)
            _slicemin = np.min(_slices)
            _slicemax = np.max(_slices)
            self.slbinl.setMinimum(_slicemin)
            self.slbinl.setMaximum(_slicemax)
            self.ldtinl.setText(str(self.slbinl.value()))
            _slices = self.survinfo['XLRange'].astype(int)
            _slicemin = np.min(_slices)
            _slicemax = np.max(_slices)
            self.slbxl.setMinimum(_slicemin)
            self.slbxl.setMaximum(_slicemax)
            self.ldtxl.setText(str(self.slbxl.value()))
            _min, _max = self.getAttribRange(self.lwgattrib.selectedItems()[0].text())
            self.ldtmin.setText(str(_min))
            self.ldtmax.setText(str(_max))
            #
            _config = {}
            for _attrib in self.lwgattrib.selectedItems():
                if _attrib.text() in self.lineplottingconfig.keys():
                    _config[_attrib.text()] = self.lineplottingconfig[_attrib.text()]
                else:
                    _config[_attrib.text()] = self.linestyle
            self.lineplottingconfig = _config
        else:
            self.slbinl.setMinimum(0)
            self.slbinl.setMaximum(0)
            self.ldtinl.setText('')
            self.slbxl.setMinimum(0)
            self.slbxl.setMaximum(0)
            self.ldtxl.setText('')
            self.ldtmin.setText('')
            self.ldtmax.setText('')
            self.lineplottingconfig = {}


    def changeSlbInl(self):
        self.ldtinl.setText(str(self.slbinl.value()))


    def changeLdtInl(self):
        if len(self.ldtinl.text()) > 0:
            _val = basic_data.str2int(self.ldtinl.text())
            if _val >= self.slbinl.minimum() and _val <= self.slbinl.maximum():
                self.slbinl.setValue(_val)


    def changeSlbXl(self):
        self.ldtxl.setText(str(self.slbxl.value()))


    def changeLdtXl(self):
        if len(self.ldtxl.text()) > 0:
            _val = basic_data.str2int(self.ldtxl.text())
            if _val >= self.slbxl.minimum() and _val <= self.slbxl.maximum():
                self.slbxl.setValue(_val)


    def clickBtnConfigLine(self):
        _config = QtWidgets.QDialog()
        _gui = gui_configlineplotting()
        _gui.lineplottingconfig = self.lineplottingconfig
        _gui.setupGUI(_config)
        _config.exec()
        self.lineplottingconfig = _gui.lineplottingconfig
        _config.show()


    def clickBtnConfigPlayer(self):
        _config = QtWidgets.QDialog()
        _gui = gui_configplayer()
        _gui.playerconfig = {}
        _gui.playerconfig['Inline'] = self.playerconfiginl
        _gui.playerconfig['Crossline'] = self.playerconfigxl
        _gui.setupGUI(_config)
        _config.exec()
        self.playerconfiginl = _gui.playerconfig['Inline']
        self.playerconfigxl = _gui.playerconfig['Crossline']
        _config.show()


    def clickBtnPlot(self):
        self.refreshMsgBox()
        #
        _attriblist = self.lwgattrib.selectedItems()
        if len(_attriblist) < 1:
            print("Plot1DSeisZ: No property selected for plot")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           '1D Window: Seismic Waveform',
                                           'No property selected for plot')
            return
        #
        _inls = self.slbinl.value()
        _xls = self.slbxl.value()
        _min = basic_data.str2float(self.ldtmin.text())
        _max = basic_data.str2float(self.ldtmax.text())
        if _min is False or _max is False:
            print("Plot1DSeisZ: Non-float range specified for plot")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           '1D Window: Seismic Waveform',
                                           'Non-float range specified for plot')
            return

        for i in range(len(_attriblist)):
            print("Plot1DSeisZ: Plot %d of %d properties: %s" % (i + 1, len(_attriblist), _attriblist[i].text()))
            _data = self.seisdata[_attriblist[i].text()]
            _data = np.reshape(_data, [_data.shape[0], -1])
            _data = np.mean(_data, axis=1)
            _data = np.reshape(_data, [len(_data), 1])
            _data = np.transpose(np.reshape(_data, [self.survinfo['ILNum'], self.survinfo['XLNum'], self.survinfo['ZNum']]),
                                 [2, 1, 0])
            # if len(_attriblist) > 1:
            #     _min, _max = self.getAttribRange(_attriblist[i].text())
            #
            _color = self.lineplottingconfig[_attriblist[i].text()]['Color'].lower()
            _linewidth = self.lineplottingconfig[_attriblist[i].text()]['Width']
            _linestyle = self.lineplottingconfig[_attriblist[i].text()]['Style'].lower()
            _markerstyle = self.lineplottingconfig[_attriblist[i].text()]['MarkerStyle']
            _markersize = self.lineplottingconfig[_attriblist[i].text()]['MarkerSize']
            #
            seis_vis.plotSeisZTracePlayerFrom3DMat(_data, initinltc=_inls, initxltc=_xls, seisinfo=self.survinfo,
                                                   titlesurf=_attriblist[i].text() + ' at ',
                                                   valuemin=_min, valuemax=_max,
                                                   color=_color, markerstyle=_markerstyle, markersize=_markersize,
                                                   linewidth=_linewidth, linestyle=_linestyle,
                                                   playerconfiginl=self.playerconfiginl,
                                                   playerconfigxl=self.playerconfigxl,
                                                   fontstyle=self.fontstyle,
                                                   qicon=QtGui.QIcon(os.path.join(self.iconpath, "icons/logo.png")))
        #
        # QtWidgets.QMessageBox.information(self.msgbox,
        #                                   "Plot Inline",
        #                                   str(len(_attriblist)) + " properties plotted successfully")
        # self.dialog.close()
        return


    def getAttribRange(self, f):
        _min = -1
        _max = 1
        if (self.checkSurvInfo() is True) \
                and (self.checkSeisData() is True)\
                and (f in self.seisdata.keys()):
            _min = np.min(self.seisdata[f])
            _max = np.max(self.seisdata[f])
        return _min, _max


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkSurvInfo(self):
        self.refreshMsgBox()
        #
        if seis_ays.checkSeisInfo(self.survinfo) is False:
            # print("Plot1DSeisZ: Survey not found")
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Plot Seismic Waveform',
            #                                'Survey not found')
            return False
        return True


    def checkSeisData(self):
        self.refreshMsgBox()
        #
        for f in self.seisdata.keys():
            if np.shape(self.seisdata[f])[0] != self.survinfo['SampleNum']:
                # print("Plot1DSeisZ: Seismic & survey not match")
                # QtWidgets.QMessageBox.critical(self.msgbox,
                #                                'Plot Seismic Waveform',
                #                                'Seismic & survey not match')
                return False
        return True


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Plot1DSeisZ = QtWidgets.QWidget()
    gui = plot1dseisz()
    gui.setupGUI(Plot1DSeisZ)
    Plot1DSeisZ.show()
    sys.exit(app.exec_())