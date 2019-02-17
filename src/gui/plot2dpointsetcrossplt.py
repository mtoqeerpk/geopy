#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     January 2019                                                                    #
#                                                                                           #
#############################################################################################

# Create a window for pointset crossplot


from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
import numpy as np
#
sys.path.append(os.path.dirname(__file__)[:-4])
from basic.data import data as basic_data
from basic.matdict import matdict as basic_mdt
from core.settings import settings as core_set
from pointset.visualization import visualization as point_vis
from gui.configlineplotting import configlineplotting as gui_configlineplotting

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class plot2dpointsetcrossplt(object):

    pointdata = {}
    linestyle = core_set.Visual['Line']
    fontstyle = core_set.Visual['Font']
    #
    iconpath = os.path.dirname(__file__)
    dialog = None
    #
    featurelist = []
    lineplottingconfig = {}

    def setupGUI(self, Plot2DPointSetCrossplt):
        Plot2DPointSetCrossplt.setObjectName("Plot2DPointSetCrossplt")
        Plot2DPointSetCrossplt.setFixedSize(420, 390)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/plotpoint.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        Plot2DPointSetCrossplt.setWindowIcon(icon)
        #
        self.lblpoint = QtWidgets.QLabel(Plot2DPointSetCrossplt)
        self.lblpoint.setObjectName("lblpoint")
        self.lblpoint.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.twgpoint = QtWidgets.QTableWidget(Plot2DPointSetCrossplt)
        self.twgpoint.setObjectName("twgpoint")
        self.twgpoint.setGeometry(QtCore.QRect(10, 50, 240, 270))
        self.twgpoint.setColumnCount(2)
        self.twgpoint.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.twgpoint.verticalHeader().hide()
        #
        self.btnconfigline = QtWidgets.QPushButton(Plot2DPointSetCrossplt)
        self.btnconfigline.setObjectName("btnconfigline")
        self.btnconfigline.setGeometry(QtCore.QRect(380, 10, 30, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/settings.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnconfigline.setIcon(icon)
        #
        self.lblxaxis = QtWidgets.QLabel(Plot2DPointSetCrossplt)
        self.lblxaxis.setObjectName("lblxaxis")
        self.lblxaxis.setGeometry(QtCore.QRect(270, 50, 40, 30))
        self.cbbxfeature = QtWidgets.QComboBox(Plot2DPointSetCrossplt)
        self.cbbxfeature.setObjectName("cbbxfeature")
        self.cbbxfeature.setGeometry(QtCore.QRect(270, 80, 140, 30))
        self.ldtxmin = QtWidgets.QLineEdit(Plot2DPointSetCrossplt)
        self.ldtxmin.setObjectName("ldtxmin")
        self.ldtxmin.setGeometry(QtCore.QRect(270, 120, 60, 30))
        self.ldtxmin.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxmax = QtWidgets.QLineEdit(Plot2DPointSetCrossplt)
        self.ldtxmax.setObjectName("ldtxmax")
        self.ldtxmax.setGeometry(QtCore.QRect(350, 120, 60, 30))
        self.ldtxmax.setAlignment(QtCore.Qt.AlignCenter)
        self.lblxrangeto = QtWidgets.QLabel(Plot2DPointSetCrossplt)
        self.lblxrangeto.setObjectName("lblxrangeto")
        self.lblxrangeto.setGeometry(QtCore.QRect(330, 120, 20, 30))
        self.lblxrangeto.setAlignment(QtCore.Qt.AlignCenter)
        self.lblyaxis = QtWidgets.QLabel(Plot2DPointSetCrossplt)
        self.lblyaxis.setObjectName("lblyaxis")
        self.lblyaxis.setGeometry(QtCore.QRect(270, 170, 40, 30))
        self.cbbyfeature = QtWidgets.QComboBox(Plot2DPointSetCrossplt)
        self.cbbyfeature.setObjectName("cbbyfeature")
        self.cbbyfeature.setGeometry(QtCore.QRect(270, 200, 140, 30))
        self.ldtymin = QtWidgets.QLineEdit(Plot2DPointSetCrossplt)
        self.ldtymin.setObjectName("ldtymin")
        self.ldtymin.setGeometry(QtCore.QRect(270, 240, 60, 30))
        self.ldtymin.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtymax = QtWidgets.QLineEdit(Plot2DPointSetCrossplt)
        self.ldtymax.setObjectName("ldtymax")
        self.ldtymax.setGeometry(QtCore.QRect(350, 240, 60, 30))
        self.ldtymax.setAlignment(QtCore.Qt.AlignCenter)
        self.lblyrangeto = QtWidgets.QLabel(Plot2DPointSetCrossplt)
        self.lblyrangeto.setObjectName("lblyrangeto")
        self.lblyrangeto.setGeometry(QtCore.QRect(330, 240, 20, 30))
        self.lblyrangeto.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllegend = QtWidgets.QLabel(Plot2DPointSetCrossplt)
        self.lbllegend.setObjectName("lbllegend")
        self.lbllegend.setGeometry(QtCore.QRect(270, 290, 60, 30))
        self.cbblegend = QtWidgets.QComboBox(Plot2DPointSetCrossplt)
        self.cbblegend.setObjectName("cbblegend")
        self.cbblegend.setGeometry(QtCore.QRect(330, 290, 80, 30))
        #
        self.btnplot = QtWidgets.QPushButton(Plot2DPointSetCrossplt)
        self.btnplot.setObjectName("btnplot")
        self.btnplot.setGeometry(QtCore.QRect(160, 340, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/plotpoint.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnplot.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(Plot2DPointSetCrossplt)
        self.msgbox.setObjectName("msgbox")
        _center_x = Plot2DPointSetCrossplt.geometry().center().x()
        _center_y = Plot2DPointSetCrossplt.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(Plot2DPointSetCrossplt)
        QtCore.QMetaObject.connectSlotsByName(Plot2DPointSetCrossplt)


    def retranslateGUI(self, Plot2DPointSetCrossplt):
        self.dialog = Plot2DPointSetCrossplt
        #
        _translate = QtCore.QCoreApplication.translate
        Plot2DPointSetCrossplt.setWindowTitle(_translate("Plot2DPointSetCrossplt", "2D Window: PointSet Cross-plot"))
        self.lblpoint.setText(_translate("Plot2DPointSetCrossplt", "Select pointsets:"))
        #
        self.twgpoint.setHorizontalHeaderLabels(["Name", "Length"])
        if len(self.pointdata.keys()) > 0:
            _idx = 0
            self.twgpoint.setRowCount(len(self.pointdata.keys()))
            for i in sorted(self.pointdata.keys()):
                item = QtWidgets.QTableWidgetItem()
                item.setText(i)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.twgpoint.setItem(_idx, 0, item)
                #
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(basic_mdt.maxDictConstantRow(self.pointdata[i])))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgpoint.setItem(_idx, 1, item)
                #
                _idx = _idx + 1
            self.twgpoint.setRowCount(_idx)
        self.twgpoint.itemSelectionChanged.connect(self.changeTwgPoint)
        #
        self.btnconfigline.setText(_translate("Plot2DPointSetCrossplt", ""))
        self.btnconfigline.clicked.connect(self.clickBtnConfigLine)
        for _item in self.twgpoint.selectedItems():
            _idx = _item.row()
            _name = self.twgpoint.item(_idx, 0).text()
            _config = self.linestyle
            self.lineplottingconfig[_name] = _config
        #
        self.lblxaxis.setText(_translate("Plot2DPointSetCrossplt", "X-axis:"))
        self.cbbxfeature.currentIndexChanged.connect(self.changeCbbXFeature)
        self.lblxrangeto.setText(_translate("Plot2DPointSetCrossplt", "~~"))
        self.lblyaxis.setText(_translate("Plot2DPointSetCrossplt", "Y-axis:"))
        self.lblyrangeto.setText(_translate("Plot2DPointSetCrossplt", "~~"))
        self.cbbyfeature.currentIndexChanged.connect(self.changeCbbYFeature)
        #
        self.lbllegend.setText(_translate("Plot2DPointSetCrossplt", "Legend:"))
        self.cbblegend.addItems(['On', 'Off'])
        #
        self.btnplot.setText(_translate("Plot2DPointSetCrossplt", "Cross-Plot"))
        self.btnplot.setDefault(True)
        self.btnplot.clicked.connect(self.clickBtnPlot)


    def changeTwgPoint(self):
        self.cbbxfeature.clear()
        self.cbbyfeature.clear()
        #
        _featurelist = []
        if len(self.twgpoint.selectedItems()) > 0:
            _featurelist = self.twgpoint.selectedItems()[0].row()
            _featurelist = self.twgpoint.item(_featurelist, 0).text()
            _featurelist = self.pointdata[_featurelist].keys()
        #
        for _item in self.twgpoint.selectedItems():
            _idx = _item.row()
            _name = self.twgpoint.item(_idx, 0).text()
            _featurelist = list(set(_featurelist) & set(self.pointdata[_name].keys()))
        #
        self.featurelist = _featurelist
        self.cbbxfeature.addItems(self.featurelist)
        self.cbbyfeature.addItems(self.featurelist)
        #
        _config = {}
        for _item in self.twgpoint.selectedItems():
            _idx = _item.row()
            _name = self.twgpoint.item(_idx, 0).text()
            if _name in self.lineplottingconfig.keys():
                _config[_name] = self.lineplottingconfig[_name]
            else:
                _config[_name] = self.linestyle
        self.lineplottingconfig = _config


    def clickBtnConfigLine(self):
        _config = QtWidgets.QDialog()
        _gui = gui_configlineplotting()
        _gui.lineplottingconfig = self.lineplottingconfig
        _gui.setupGUI(_config)
        _config.exec()
        self.lineplottingconfig = _gui.lineplottingconfig
        _config.show()


    def changeCbbXFeature(self):
        if self.cbbxfeature.currentIndex() < 0:
            self.ldtxmin.setText('')
            self.ldtxmax.setText('')
        else:
            _min = 1e+9
            _max = -1e+9
            _f = self.featurelist[self.cbbxfeature.currentIndex()]
            for _point in self.twgpoint.selectedItems():
                _idx = _point.row()
                _name = self.twgpoint.item(_idx, 0).text()
                if _min > np.min(self.pointdata[_name][_f]):
                    _min = np.min(self.pointdata[_name][_f])
                if _max < np.max(self.pointdata[_name][_f]):
                    _max = np.max(self.pointdata[_name][_f])
            self.ldtxmin.setText(str(_min))
            self.ldtxmax.setText(str(_max))


    def changeCbbYFeature(self):
        if self.cbbyfeature.currentIndex() < 0:
            self.ldtymin.setText('')
            self.ldtymax.setText('')
        else:
            _min = 1e+9
            _max = -1e+9
            _f = self.featurelist[self.cbbyfeature.currentIndex()]
            for _point in self.twgpoint.selectedItems():
                _idx = _point.row()
                _name = self.twgpoint.item(_idx, 0).text()
                if _min > np.min(self.pointdata[_name][_f]):
                    _min = np.min(self.pointdata[_name][_f])
                if _max < np.max(self.pointdata[_name][_f]):
                    _max = np.max(self.pointdata[_name][_f])
            self.ldtymin.setText(str(_min))
            self.ldtymax.setText(str(_max))


    def clickBtnPlot(self):
        self.refreshMsgBox()
        #
        _npoint = len(self.twgpoint.selectedItems())
        if _npoint < 1:
            print("Plot2DPointSetCrossplt: No pointset selected")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           '2D Window: PointSet Cross-plot',
                                           'No pointset selected')
            return
        #
        _xfeature = self.featurelist[self.cbbxfeature.currentIndex()]
        _yfeature = self.featurelist[self.cbbyfeature.currentIndex()]
        _xmin = basic_data.str2float(self.ldtxmin.text())
        _xmax = basic_data.str2float(self.ldtxmax.text())
        _ymin = basic_data.str2float(self.ldtymin.text())
        _ymax = basic_data.str2float(self.ldtymax.text())
        if _xmin is False or _xmax is False or _ymin is False or _ymax is False:
            print("Plot2DPointSetCrossplt: Non-float range specified for plot")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           '2D Window: PointSet Cross-plot',
                                           'on-float range specified for plot')
            return
        #
        _legendon = False
        if self.cbblegend.currentIndex() == 0:
            _legendon = True
        #
        _pointdict = {}
        _markerstylelist = []
        _markersizelist = []
        _colorlist = []
        _linestylelist = []
        _linewidthlist = []
        for _item in self.twgpoint.selectedItems():
            _idx = _item.row()
            _name = self.twgpoint.item(_idx, 0).text()

            #
            if _xfeature not in self.pointdata[_name].keys():
                print("Plot2DPointSetCrossplt: X-feature not found in " + _name)
                QtWidgets.QMessageBox.critical(self.msgbox,
                                               '2-D Cross-plot',
                                               'X-feature not found in ' + _name)
                return
            if _yfeature not in self.pointdata[_name].keys():
                print("Plot2DPointSetCrossplt: Y-feature not found in " + _name)
                QtWidgets.QMessageBox.critical(self.msgbox,
                                               '2-D Cross-plot',
                                               'Y-feature not found in ' + _name)
                return
            #
            _data = {}
            _data[_xfeature] = self.pointdata[_name][_xfeature]
            _data[_yfeature] = self.pointdata[_name][_yfeature]
            _pointdict[_name] = _data
            #
            _markerstylelist.append(self.lineplottingconfig[_name]['MarkerStyle'])
            _markersizelist.append(self.lineplottingconfig[_name]['MarkerSize'])
            _colorlist.append(self.lineplottingconfig[_name]['Color'].lower())
            _linestylelist.append(self.lineplottingconfig[_name]['Style'].lower())
            _linewidthlist.append(self.lineplottingconfig[_name]['Width'])
        #
        point_vis.crossplot2D(_pointdict,
                              colorlist=_colorlist, linestylelist=_linestylelist,
                              linewidthlist=_linewidthlist,
                              markerstylelist=_markerstylelist,
                              markersizelist=_markersizelist,
                              xfeature=_xfeature, yfeature=_yfeature,
                              xlim=[_xmin, _xmax], ylim=[_ymin, _ymax],
                              xlabel=_xfeature, ylabel=_yfeature, legendon=_legendon,
                              fontstyle=self.fontstyle,
                              qicon=QtGui.QIcon(os.path.join(self.iconpath, "icons/logo.png")))


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Plot2DPointSetCrossplt = QtWidgets.QWidget()
    gui = plot2dpointsetcrossplt()
    gui.setupGUI(Plot2DPointSetCrossplt)
    Plot2DPointSetCrossplt.show()
    sys.exit(app.exec_())