#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for import pre-stack seismic images


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4])
from basic.data import data as basic_data
from psseismic.visualization import visualization as psseis_vis
from psseismic.analysis import analysis as psseis_ays

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class importpsseisimageset(object):

    psseisdata = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None
    #
    imagelist = []

    def setupGUI(self, ImportPsSeisImageSet):
        ImportPsSeisImageSet.setObjectName("ImportPsSeisImageSet")
        ImportPsSeisImageSet.setFixedSize(400, 270)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/image.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ImportPsSeisImageSet.setWindowIcon(icon)
        self.lblimage = QtWidgets.QLabel(ImportPsSeisImageSet)
        self.lblimage.setObjectName("lblimage")
        self.lblimage.setGeometry(QtCore.QRect(10, 10, 110, 30))
        self.ldtimage = QtWidgets.QLineEdit(ImportPsSeisImageSet)
        self.ldtimage.setObjectName("ldtimage")
        self.ldtimage.setGeometry(QtCore.QRect(130, 10, 190, 30))
        self.btnimage = QtWidgets.QPushButton(ImportPsSeisImageSet)
        self.btnimage.setObjectName("btnimage")
        self.btnimage.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lbltype = QtWidgets.QLabel(ImportPsSeisImageSet)
        self.lbltype.setObjectName("lbltype")
        self.lbltype.setGeometry(QtCore.QRect(10, 60, 110, 30))
        self.cbbtype = QtWidgets.QComboBox(ImportPsSeisImageSet)
        self.cbbtype.setObjectName("cbbtype")
        self.cbbtype.setGeometry(QtCore.QRect(130, 60, 260, 30))
        self.lbldims = QtWidgets.QLabel(ImportPsSeisImageSet)
        self.lbldims.setObjectName("lbldims")
        self.lbldims.setGeometry(QtCore.QRect(10, 110, 110, 30))
        self.ldtdimsinl = QtWidgets.QLineEdit(ImportPsSeisImageSet)
        self.ldtdimsinl.setObjectName("ldtdimsinl")
        self.ldtdimsinl.setGeometry(QtCore.QRect(130, 110, 60, 30))
        self.ldtdimsxl = QtWidgets.QLineEdit(ImportPsSeisImageSet)
        self.ldtdimsxl.setObjectName("ldtdimsxl")
        self.ldtdimsxl.setGeometry(QtCore.QRect(230, 110, 60, 30))
        self.ldtdimsz = QtWidgets.QLineEdit(ImportPsSeisImageSet)
        self.ldtdimsz.setObjectName("ldtdimsz")
        self.ldtdimsz.setGeometry(QtCore.QRect(330, 110, 60, 30))
        self.lblsave = QtWidgets.QLabel(ImportPsSeisImageSet)
        self.lblsave.setObjectName("lblsave")
        self.lblsave.setGeometry(QtCore.QRect(10, 160, 110, 30))
        self.ldtsave = QtWidgets.QLineEdit(ImportPsSeisImageSet)
        self.ldtsave.setObjectName("ldtsave")
        self.ldtsave.setGeometry(QtCore.QRect(130, 160, 130, 30))
        self.btnimportimage = QtWidgets.QPushButton(ImportPsSeisImageSet)
        self.btnimportimage.setObjectName("btnimportimage")
        self.btnimportimage.setGeometry(QtCore.QRect(120, 210, 160, 30))
        self.btnimportimage.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ImportPsSeisImageSet)
        self.msgbox.setObjectName("msgbox")
        _center_x = ImportPsSeisImageSet.geometry().center().x()
        _center_y = ImportPsSeisImageSet.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ImportPsSeisImageSet)
        QtCore.QMetaObject.connectSlotsByName(ImportPsSeisImageSet)


    def retranslateGUI(self, ImportPsSeisImageSet):
        self.dialog = ImportPsSeisImageSet
        #
        _translate = QtCore.QCoreApplication.translate
        ImportPsSeisImageSet.setWindowTitle(_translate("ImportPsSeisImageSet", "Import Pre-stack Seismic ImageSet"))
        self.lblimage.setText(_translate("ImportPsSeisImageSet", "Select 2D images:"))
        self.lblimage.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtimage.setText(_translate("ImportPsSeisImageSet", os.path.abspath(self.rootpath)))
        self.btnimage.setText(_translate("ImportPsSeisImageSet", "Browse"))
        self.btnimage.clicked.connect(self.clickBtnImage)
        self.lbltype.setText(_translate("ImportPsSeisImageSet", "       Orientation:"))
        self.lbltype.setAlignment(QtCore.Qt.AlignCenter)
        self.cbbtype.addItems(['Shot'])
        self.cbbtype.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, "icons/gather.png")))
        self.cbbtype.currentIndexChanged.connect(self.changeCbbType)
        self.lbldims.setText(_translate("ImportPsSeisImageSet", "Survey dimensions:"))
        self.lbldims.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtdimsinl.setText('')
        self.ldtdimsinl.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtdimsxl.setText('')
        self.ldtdimsxl.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtdimsz.setText('')
        self.ldtdimsz.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate("ImportPsSeisImageSet", "Output name:"))
        self.ldtsave.setText(_translate("ImportPsSeisImageSet", "image"))
        self.btnimportimage.setText(_translate("ImportPsSeisImageSet", "Import ImageSet"))
        self.btnimportimage.clicked.connect(self.clickBtnImportPsSeisImageSet)


    def clickBtnImage(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileNames(None, 'Select Pre-stack Seismic Image(s)', self.rootpath,
                                         filter="Image files (*.jpg; *.png);; All files (*.*)")
        if len(_file[0]) > 0:
            self.imagelist = _file[0]
            self.ldtimage.setText(str(_file[0]))


    def changeCbbType(self):
        if self.cbbtype.currentIndex() == 0:
            self.ldtdimsinl.setEnabled(True)
            self.ldtdimsxl.setEnabled(True)
            self.ldtdimsz.setEnabled(True)


    def clickBtnImportPsSeisImageSet(self):
        self.refreshMsgBox()
        #
        _nimage = len(self.imagelist)
        if _nimage <= 0:
            print("ImportPsSeisImageSet: No image selected for import")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Pre-stack Seismic ImageSet',
                                           'No image selected for import')
            return
        #
        _ninl = basic_data.str2int(self.ldtdimsinl.text())
        _nxl = basic_data.str2int(self.ldtdimsxl.text())
        _nz = basic_data.str2int(self.ldtdimsz.text())
        if _ninl is False or _nxl is False or _nz is False:
            print("ImportPsSeisImageSet: Non-integer survey dimensions")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Pre-stack Seismic ImageSet',
                                           'Non-integer dimensions')
            return
        if _ninl <= 0 or _nxl <= 0 or _nz <= 0:
            print("ImportPsSeisImageSet: Zero survey dimensions")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Pre-stack Seismic ImageSet',
                                           'Zero survey dimensions')
            return
        #
        # Progress dialog
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/image.png")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Import Pre-stack Seismic ImageSet')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        #
        if self.cbbtype.currentIndex() == 0:
            _shots = np.linspace(0, len(self.imagelist)-1, len(self.imagelist), dtype=int)
            # _pgsdlg.setWindowTitle('Import ' + str(len(_shots)) + ' Pre-stack Seismic ImageSet')
            _imagedata = psseis_vis.loadPsSeisShot(self.imagelist, _shots,
                                                   ispref=False,
                                                   inlnum=_ninl, inlstart=0, inlstep=1,
                                                   xlnum=_nxl, xlstart=0, xlstep=1,
                                                   znum=_nz, zstart=0, zstep=-1,
                                                   qpgsdlg=_pgsdlg
                                                   )
        _psseisdata = {}
        if checkPsSeisData(_imagedata):
            _psseisdata[self.ldtsave.text()] = _imagedata
        #
        # add new data to psseisdata
        for key in _psseisdata.keys():
            if key in self.psseisdata.keys() and checkPsSeisData(self.psseisdata[key]):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Pre-stack Seismic ImageSet',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.psseisdata[key] = _psseisdata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Pre-stack Seismic ImageSet",
                                          str(_nimage) + " image(s) imported as Pre-stack Seismic successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


def checkPsSeisData(psseisdata):
    return psseis_ays.checkPsSeis(psseisdata)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ImportPsSeisImageSet = QtWidgets.QWidget()
    gui = importpsseisimageset()
    gui.setupGUI(ImportPsSeisImageSet)
    ImportPsSeisImageSet.show()
    sys.exit(app.exec_())