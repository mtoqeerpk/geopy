#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for import seismic images


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4])
from basic.data import data as basic_data
from seismic.visualization import visualization as seis_vis
from seismic.analysis import analysis as seis_ays

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class importseisimageset(object):

    survinfo = {}
    seisdata = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None
    #
    imagelist = []

    def setupGUI(self, ImportSeisImageSet):
        ImportSeisImageSet.setObjectName("ImportSeisImageSet")
        ImportSeisImageSet.setFixedSize(400, 270)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/image.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ImportSeisImageSet.setWindowIcon(icon)
        self.lblimage = QtWidgets.QLabel(ImportSeisImageSet)
        self.lblimage.setObjectName("lblimage")
        self.lblimage.setGeometry(QtCore.QRect(10, 10, 110, 30))
        self.ldtimage = QtWidgets.QLineEdit(ImportSeisImageSet)
        self.ldtimage.setObjectName("ldtimage")
        self.ldtimage.setGeometry(QtCore.QRect(130, 10, 190, 30))
        self.btnimage = QtWidgets.QPushButton(ImportSeisImageSet)
        self.btnimage.setObjectName("btnimage")
        self.btnimage.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lbltype = QtWidgets.QLabel(ImportSeisImageSet)
        self.lbltype.setObjectName("lbltype")
        self.lbltype.setGeometry(QtCore.QRect(10, 60, 110, 30))
        self.cbbtype = QtWidgets.QComboBox(ImportSeisImageSet)
        self.cbbtype.setObjectName("cbbtype")
        self.cbbtype.setGeometry(QtCore.QRect(130, 60, 260, 30))
        self.lbldims = QtWidgets.QLabel(ImportSeisImageSet)
        self.lbldims.setObjectName("lbldims")
        self.lbldims.setGeometry(QtCore.QRect(10, 110, 110, 30))
        self.ldtdimsinl = QtWidgets.QLineEdit(ImportSeisImageSet)
        self.ldtdimsinl.setObjectName("ldtdimsinl")
        self.ldtdimsinl.setGeometry(QtCore.QRect(130, 110, 60, 30))
        self.ldtdimsxl = QtWidgets.QLineEdit(ImportSeisImageSet)
        self.ldtdimsxl.setObjectName("ldtdimsxl")
        self.ldtdimsxl.setGeometry(QtCore.QRect(230, 110, 60, 30))
        self.ldtdimsz = QtWidgets.QLineEdit(ImportSeisImageSet)
        self.ldtdimsz.setObjectName("ldtdimsz")
        self.ldtdimsz.setGeometry(QtCore.QRect(330, 110, 60, 30))
        self.lblsave = QtWidgets.QLabel(ImportSeisImageSet)
        self.lblsave.setObjectName("lblsave")
        self.lblsave.setGeometry(QtCore.QRect(10, 160, 110, 30))
        self.ldtsave = QtWidgets.QLineEdit(ImportSeisImageSet)
        self.ldtsave.setObjectName("ldtsave")
        self.ldtsave.setGeometry(QtCore.QRect(130, 160, 130, 30))
        self.btnimportimage = QtWidgets.QPushButton(ImportSeisImageSet)
        self.btnimportimage.setObjectName("btnimportimage")
        self.btnimportimage.setGeometry(QtCore.QRect(120, 210, 160, 30))
        self.btnimportimage.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ImportSeisImageSet)
        self.msgbox.setObjectName("msgbox")
        _center_x = ImportSeisImageSet.geometry().center().x()
        _center_y = ImportSeisImageSet.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ImportSeisImageSet)
        QtCore.QMetaObject.connectSlotsByName(ImportSeisImageSet)


    def retranslateGUI(self, ImportSeisImageSet):
        self.dialog = ImportSeisImageSet
        #
        _translate = QtCore.QCoreApplication.translate
        ImportSeisImageSet.setWindowTitle(_translate("ImportSeisImageSet", "Import Seismic ImageSet"))
        self.lblimage.setText(_translate("ImportSeisImageSet", "Select 2D images:"))
        self.lblimage.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtimage.setText(_translate("ImportSeisImageSet", os.path.abspath(self.rootpath)))
        self.btnimage.setText(_translate("ImportSeisImageSet", "Browse"))
        self.btnimage.clicked.connect(self.clickBtnImage)
        self.lbltype.setText(_translate("ImportSeisImageSet", "       Orientation:"))
        self.lbltype.setAlignment(QtCore.Qt.AlignCenter)
        self.cbbtype.addItems(['Inline', 'Crossline', 'Time/depth'])
        self.cbbtype.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, "icons/visinl.png")))
        self.cbbtype.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, "icons/visinl.png")))
        self.cbbtype.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, "icons/visz.png")))
        self.cbbtype.currentIndexChanged.connect(self.changeCbbType)
        self.lbldims.setText(_translate("ImportSeisImageSet", "Survey dimensions:"))
        self.lbldims.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtdimsinl.setEnabled(False)
        self.ldtdimsinl.setText(str(len(self.imagelist)))
        self.ldtdimsinl.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtdimsxl.setText(str(len(self.imagelist)))
        self.ldtdimsxl.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtdimsz.setText(str(len(self.imagelist)))
        self.ldtdimsz.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate("ImportSeisImageSet", "Output name:"))
        self.ldtsave.setText(_translate("ImportSeisImageSet", "image"))
        self.btnimportimage.setText(_translate("ImportSeisImageSet", "Import ImageSet"))
        self.btnimportimage.clicked.connect(self.clickBtnImportSeisImageSet)


    def clickBtnImage(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileNames(None, 'Select Seismic Image(s)', self.rootpath,
                                         filter="Image files (*.jpg; *.png);; All files (*.*)")
        if len(_file[0]) > 0:
            self.imagelist = _file[0]
            self.ldtimage.setText(str(_file[0]))
            if self.cbbtype.currentIndex() == 0:
                self.ldtdimsinl.setText(str(len(_file[0])))
            if self.cbbtype.currentIndex() == 1:
                self.ldtdimsxl.setText(str(len(_file[0])))
            if self.cbbtype.currentIndex() == 2:
                self.ldtdimsz.setText(str(len(_file[0])))


    def changeCbbType(self):
        if self.cbbtype.currentIndex() == 0:
            self.ldtdimsinl.setText(str(len(self.imagelist)))
            self.ldtdimsxl.setText("0")
            self.ldtdimsz.setText("0")
            self.ldtdimsinl.setEnabled(False)
            self.ldtdimsxl.setEnabled(True)
            self.ldtdimsz.setEnabled(True)
        if self.cbbtype.currentIndex() == 1:
            self.ldtdimsinl.setText("0")
            self.ldtdimsxl.setText(str(len(self.imagelist)))
            self.ldtdimsz.setText("0")
            self.ldtdimsinl.setEnabled(True)
            self.ldtdimsxl.setEnabled(False)
            self.ldtdimsz.setEnabled(True)
        if self.cbbtype.currentIndex() == 2:
            self.ldtdimsinl.setText("0")
            self.ldtdimsxl.setText("0")
            self.ldtdimsz.setText(str(len(self.imagelist)))
            self.ldtdimsinl.setEnabled(True)
            self.ldtdimsxl.setEnabled(True)
            self.ldtdimsz.setEnabled(False)


    def clickBtnImportSeisImageSet(self):
        self.refreshMsgBox()
        #
        _nimage = len(self.imagelist)
        if _nimage <= 0:
            print("ImageSeisImageSet: No image selected for import")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Seismic ImageSet',
                                           'No image selected for import')
            return
        #
        _ninl = basic_data.str2int(self.ldtdimsinl.text())
        _nxl = basic_data.str2int(self.ldtdimsxl.text())
        _nz = basic_data.str2int(self.ldtdimsz.text())
        if _ninl is False or _nxl is False or _nz is False:
            print("ImageSeisImageSet: Non-integer survey dimensions")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Seismic ImageSet',
                                           'Non-integer dimensions')
            return
        if _ninl <= 0 or _nxl <= 0 or _nz <= 0:
            print("ImageSeisImageSet: Zero survey dimensions")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Seismic ImageSet',
                                           'Zero survey dimensions')
            return
        #
        # Progress dialog
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/image.png")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Import Seismic ImageSet')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        #
        if self.cbbtype.currentIndex() == 0:
            # _pgsdlg.setWindowTitle('Import ' + str(_ninl) + ' Seismic ImageSet')
            _imagedata = seis_vis.loadSeisILSliceTo3DMat(self.imagelist,
                                                         inlsls=np.linspace(0, _ninl - 1, _ninl, dtype=int),
                                                         ispref=False,
                                                         xlnum=_nxl,
                                                         znum=_nz,
                                                         qpgsdlg=_pgsdlg
                                                         )
        if self.cbbtype.currentIndex() == 1:
            # _pgsdlg.setWindowTitle('Import ' + str(_nxl) + ' Seismic Image')
            _imagedata = seis_vis.loadSeisXLSliceTo3DMat(self.imagelist, xlsls=np.linspace(0, _nxl - 1, _nxl, dtype=int),
                                                         ispref=False,
                                                         inlnum=_ninl,
                                                         znum=_nz,
                                                         qpgsdlg=_pgsdlg
                                                         )
        if self.cbbtype.currentIndex() == 2:
            # _pgsdlg.setWindowTitle('Import ' + str(_nz) + ' Seismic Image')
            _imagedata = seis_vis.loadSeisZSliceTo3DMat(self.imagelist,
                                                        zsls=np.linspace(0, -_nz + 1, _nz, dtype=int),
                                                        ispref=False,
                                                        inlnum=_ninl,
                                                        xlnum=_nxl,
                                                        qpgsdlg=_pgsdlg
                                                        )
        _seisdata = {}
        _survinfo = seis_ays.createSeisInfoFrom3DMat(_imagedata)
        _imagedata = np.reshape(np.transpose(_imagedata, [2, 1, 0]), [-1, 1])
        if checkSeisData(_imagedata, _survinfo):
            _seisdata[self.ldtsave.text()] = _imagedata
        #
        # add new data to seisdata
        if checkSurvInfo(_survinfo):
            self.survinfo = _survinfo
        for key in _seisdata.keys():
            if key in self.seisdata.keys() and checkSeisData(self.seisdata[key], self.survinfo):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Seismic ImageSet',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.seisdata[key] = _seisdata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Seismic ImageSet",
                                          str(_nimage) + " image(s) imported as Seismic successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


def checkSurvInfo(survinfo):
    return seis_ays.checkSeisInfo(survinfo)


def checkSeisData(seisdata, survinfo):
    return seis_ays.isSeis2DMatConsistentWithSeisInfo(seisdata, survinfo)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ImportSeisImageSet = QtWidgets.QWidget()
    gui = importseisimageset()
    gui.setupGUI(ImportSeisImageSet)
    ImportSeisImageSet.show()
    sys.exit(app.exec_())