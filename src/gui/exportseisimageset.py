#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for exporting seismic images


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from basic.data import data as basic_data
from seismic.analysis import analysis as seis_ays
from seismic.visualization import visualization as seis_vis

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class exportseisimageset(object):

    survinfo = {}
    seisdata = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None

    cmapsname = ['Seismic', 'Phase', 'Frequency', 'Red-White-Blue', 'Gray-Scale',
                 'Black-White-Red', 'Black-White-Green', 'Black-White-Blue',
                 'White-Red-Black', 'White-Green-Black', 'White-Blue-Black',
                 'Black-Red', 'Black-Green', 'Black-Blue']
    cmaps = ['seismic', 'phase', 'frequency', 'red_white_blue', 'white_gray_black',
             'black_white_red', 'black_white_green', 'black_white_blue',
             'white_red_black', 'white_green_black', 'white_blue_black',
             'black_red', 'black_green', 'black_blue']

    def setupGUI(self, ExportSeisImageSet):
        ExportSeisImageSet.setObjectName("ExportSeisImageSet")
        ExportSeisImageSet.setFixedSize(400, 550)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/image.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ExportSeisImageSet.setWindowIcon(icon)
        #
        self.lblattrib = QtWidgets.QLabel(ExportSeisImageSet)
        self.lblattrib.setObjectName("lblattrib")
        self.lblattrib.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwgattrib = QtWidgets.QListWidget(ExportSeisImageSet)
        self.lwgattrib.setObjectName("lwgattrib")
        self.lwgattrib.setGeometry(QtCore.QRect(160, 10, 230, 200))
        self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lbltype = QtWidgets.QLabel(ExportSeisImageSet)
        self.lbltype.setObjectName("lbltype")
        self.lbltype.setGeometry(QtCore.QRect(10, 230, 150, 30))
        self.cbbtype = QtWidgets.QComboBox(ExportSeisImageSet)
        self.cbbtype.setObjectName("cbbtype")
        self.cbbtype.setGeometry(QtCore.QRect(160, 230, 230, 30))
        self.lblslice = QtWidgets.QLabel(ExportSeisImageSet)
        self.lblslice.setObjectName("lblslice")
        self.lblslice.setGeometry(QtCore.QRect(10, 280, 150, 30))
        self.rdbsliceall = QtWidgets.QRadioButton(ExportSeisImageSet)
        self.rdbsliceall.setObjectName("rdbsliceall")
        self.rdbsliceall.setGeometry(QtCore.QRect(160, 280, 230, 30))
        self.rdbslicedef = QtWidgets.QRadioButton(ExportSeisImageSet)
        self.rdbslicedef.setObjectName("rdbslicedef")
        self.rdbslicedef.setGeometry(QtCore.QRect(160, 320, 230, 30))
        self.ldtslicedef = QtWidgets.QLineEdit(ExportSeisImageSet)
        self.ldtslicedef.setObjectName("ldtslicedef")
        self.ldtslicedef.setGeometry(QtCore.QRect(160, 360, 230, 30))
        self.lblcmap = QtWidgets.QLabel(ExportSeisImageSet)
        self.lblcmap.setObjectName("lblcmap")
        self.lblcmap.setGeometry(QtCore.QRect(10, 400, 150, 30))
        self.cbbcmap = QtWidgets.QComboBox(ExportSeisImageSet)
        self.cbbcmap.setObjectName("cbbcmap")
        self.cbbcmap.setGeometry(QtCore.QRect(160, 400, 170, 30))
        self.cbxflip = QtWidgets.QCheckBox(ExportSeisImageSet)
        self.cbxflip.setObjectName("cbxflip")
        self.cbxflip.setGeometry(QtCore.QRect(340, 400, 50, 30))
        self.lblsave = QtWidgets.QLabel(ExportSeisImageSet)
        self.lblsave.setObjectName("lblsave")
        self.lblsave.setGeometry(QtCore.QRect(10, 440, 50, 30))
        self.ldtsave = QtWidgets.QLineEdit(ExportSeisImageSet)
        self.ldtsave.setObjectName("ldtsave")
        self.ldtsave.setGeometry(QtCore.QRect(70, 440, 250, 30))
        self.btnsave = QtWidgets.QPushButton(ExportSeisImageSet)
        self.btnsave.setObjectName("btnsave")
        self.btnsave.setGeometry(QtCore.QRect(330, 440, 60, 30))
        self.btnexportimage = QtWidgets.QPushButton(ExportSeisImageSet)
        self.btnexportimage.setObjectName("btnexportimage")
        self.btnexportimage.setGeometry(QtCore.QRect(120, 490, 160, 30))
        self.btnexportimage.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ExportSeisImageSet)
        self.msgbox.setObjectName("msgbox")
        _center_x = ExportSeisImageSet.geometry().center().x()
        _center_y = ExportSeisImageSet.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ExportSeisImageSet)
        QtCore.QMetaObject.connectSlotsByName(ExportSeisImageSet)


    def retranslateGUI(self, ExportSeisImageSet):
        self.dialog = ExportSeisImageSet
        #
        _translate = QtCore.QCoreApplication.translate
        ExportSeisImageSet.setWindowTitle(_translate("ExportSeisImageSet", "Export Seismic ImageSet"))
        self.lblattrib.setText(_translate("ExportSeisImageSet", "Select output properties:"))
        if self.checkSurvInfo() is True:
            _firstattrib = None
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i):
                    item = QtWidgets.QListWidgetItem(self.lwgattrib)
                    item.setText(_translate("ExportSeisImageSet", i))
                    self.lwgattrib.addItem(item)
                    if _firstattrib is None:
                        _firstattrib = item
            self.lwgattrib.setCurrentItem(_firstattrib)
        self.lbltype.setText(_translate("ExportSeisImageSet", "Select orientation:"))
        self.cbbtype.addItems(['Inline', 'Crossline', 'Time/depth'])
        self.cbbtype.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, "icons/visinl.png")))
        self.cbbtype.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, "icons/visinl.png")))
        self.cbbtype.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, "icons/visz.png")))
        self.lblslice.setText(_translate("ExportSeisImageSet", "Sepcify output slices:"))
        self.rdbsliceall.setText(_translate("ExportSeisImageSet", "All within input dimensions"))
        self.rdbsliceall.setChecked(True)
        self.rdbsliceall.clicked.connect(self.clickRdbSliceAll)
        self.rdbslicedef.setText(_translate("ExportSeisImageSet", "User-defined (separated by ',')"))
        self.rdbslicedef.setChecked(False)
        self.rdbslicedef.clicked.connect(self.clickRdbSliceDef)
        self.ldtslicedef.setText(_translate("ExportSeisImageSet", "0"))
        self.ldtslicedef.setEnabled(False)
        self.lblcmap.setText(_translate("Plot2DXlSlice", "\t    Color map:"))
        self.cbbcmap.addItems(self.cmapsname)
        for _i in range(len(self.cmaps)):
            self.cbbcmap.setItemIcon(_i, QtGui.QIcon(
                QtGui.QPixmap(os.path.join(self.iconpath, "icons/cmap_" + self.cmaps[_i] + ".png")).scaled(80, 30)))
        self.cbxflip.setText(_translate("ExportSeisImageSet", "Flip"))
        self.lblsave.setText(_translate("ExportSeisImageSet", "Save to:"))
        self.ldtsave.setText(_translate("ExportSeisImageSet", os.path.abspath(self.rootpath)))
        self.btnsave.setText(_translate("ExportSeisImageSet", "Browse"))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnexportimage.setText(_translate("ExportSeisImageSet", "Export Seismic ImageSet"))
        self.btnexportimage.clicked.connect(self.clickBtnExportSeisImageSet)


    def clickRdbSliceAll(self):
        if self.rdbsliceall.isChecked():
            self.rdbsliceall.setChecked(True)
            self.rdbslicedef.setChecked(False)
            self.ldtslicedef.setText("0")
            self.ldtslicedef.setEnabled(False)


    def clickRdbSliceDef(self):
        if self.rdbslicedef.isChecked():
            self.rdbslicedef.setChecked(True)
            self.rdbsliceall.setChecked(False)
            self.ldtslicedef.setEnabled(True)


    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getExistingDirectory(None, 'Select Export Folder', self.rootpath,
                                             options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if len(_file) > 0:
            self.ldtsave.setText(_file)


    def clickBtnExportSeisImageSet(self):
        self.refreshMsgBox()
        #
        _attriblist = self.lwgattrib.selectedItems()
        if len(_attriblist) < 1:
            print("ExportSeisImageSet: No property selected for export")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Export Seismic ImageSet',
                                           'No property selected for export')
            return
        if self.rdbslicedef.isChecked():
            for s in self.ldtslicedef.text().split(','):
                if basic_data.str2int(s) is False:
                    print("ExportSeisImageSet: Non-integer slice selection")
                    QtWidgets.QMessageBox.critical(self.msgbox,
                                                   'Export Seismic ImageSet',
                                                   'Non-integer slice selection')
                    return
        #
        # Progress dialog
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/image.png")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Export ' + str(len(_attriblist)) + ' Seismic Image')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        # _pgsdlg.setMaximum(len(_attriblist))
        #
        _cmap = self.cbbcmap.currentIndex()
        _flip = self.cbxflip.isChecked()
        for i in range(len(_attriblist)):
            #
            # QtCore.QCoreApplication.instance().processEvents()
            # _pgsdlg.setValue(i)
            _pgsdlg.setWindowTitle('Export '+str(i+1)+' of '+str(len(_attriblist))+' Seismic ImageSet')
            #
            _sls = None
            if self.rdbslicedef.isChecked():
                _sls = [basic_data.str2int(s) for s in self.ldtslicedef.text().split(',')]
            _imagefile = os.path.join(self.ldtsave.text(),
                                      _attriblist[i].text() + '_')
            _data = self.seisdata[_attriblist[i].text()]
            _data = np.reshape(_data, [_data.shape[0], -1])
            _data = np.mean(_data, axis=1)
            _data = np.reshape(_data, [len(_data), 1])
            _data = np.transpose(np.reshape(_data, [self.survinfo['ILNum'], self.survinfo['XLNum'], self.survinfo['ZNum']]),
                                 [2, 1, 0])
            print("ExportSeisImageSet: Export %d of %d ImageSet: %s" % (i + 1, len(_attriblist), _attriblist[i].text()))
            if self.cbbtype.currentIndex() == 0:
                seis_vis.saveSeisILSliceFrom3DMat(_data, _imagefile, inlsls=_sls, seisinfo=self.survinfo,
                                                  valuemin=np.min(_data),
                                                  valuemax=np.max(_data),
                                                  colormap=self.cmaps[_cmap],
                                                  flipcmap=_flip,
                                                  verbose=False
                                                  )
            if self.cbbtype.currentIndex() == 1:
                seis_vis.saveSeisXLSliceFrom3DMat(_data, _imagefile, xlsls=_sls, seisinfo=self.survinfo,
                                                 valuemin=np.min(_data),
                                                 valuemax=np.max(_data),
                                                 colormap=self.cmaps[_cmap],
                                                 flipcmap=_flip,
                                                 verbose=False, qpgsdlg=_pgsdlg)
            if self.cbbtype.currentIndex() == 2:
                seis_vis.saveSeisZSliceFrom3DMat(_data, _imagefile, zsls=_sls, seisinfo=self.survinfo,
                                                valuemin=np.min(_data),
                                                valuemax=np.max(_data),
                                                colormap=self.cmaps[_cmap],
                                                flipcmap=_flip,
                                                verbose=False)
            #
        # _pgsdlg.setValue(len(_attriblist))
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Export Seismic ImageSet",
                                          str(len(_attriblist)) + " properties exported as ImageSet successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkSurvInfo(self):
        self.refreshMsgBox()
        #
        if seis_ays.checkSeisInfo(self.survinfo) is False:
            # print("ExportSeisImageSet: Survey not found")
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Export Seismic ImageSet',
            #                                'Survey not found')
            return False
        return True


    def checkSeisData(self, f):
        self.refreshMsgBox()
        #
        return seis_ays.isSeis2DMatConsistentWithSeisInfo(self.seisdata[f], self.survinfo)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ExportSeisImageSet = QtWidgets.QWidget()
    gui = exportseisimageset()
    gui.setupGUI(ExportSeisImageSet)
    ExportSeisImageSet.show()
    sys.exit(app.exec_())