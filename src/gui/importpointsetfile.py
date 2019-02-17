#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     August 2018                                                                     #
#                                                                                           #
#############################################################################################

# Create a window for import points from a file


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4])
from pointset.inputoutput import inputoutput as point_io


QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class importpointsetfile(object):

    pointdata = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None
    #
    filelist = []

    def setupGUI(self, ImportPointSetFile):
        ImportPointSetFile.setObjectName("ImportPointSetFile")
        ImportPointSetFile.setFixedSize(400, 320)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/copy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ImportPointSetFile.setWindowIcon(icon)
        self.lblfile = QtWidgets.QLabel(ImportPointSetFile)
        self.lblfile.setObjectName("lblfile")
        self.lblfile.setGeometry(QtCore.QRect(10, 10, 110, 30))
        self.ldtfile = QtWidgets.QLineEdit(ImportPointSetFile)
        self.ldtfile.setObjectName("ldtfile")
        self.ldtfile.setGeometry(QtCore.QRect(130, 10, 190, 30))
        self.btnfile = QtWidgets.QPushButton(ImportPointSetFile)
        self.btnfile.setObjectName("btnfile")
        self.btnfile.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lbltype = QtWidgets.QLabel(ImportPointSetFile)
        self.lbltype.setObjectName("lbltype")
        self.lbltype.setGeometry(QtCore.QRect(30, 50, 100, 30))
        self.cbbtype = QtWidgets.QComboBox(ImportPointSetFile)
        self.cbbtype.setObjectName("cbbtype")
        self.cbbtype.setGeometry(QtCore.QRect(130, 50, 260, 30))
        #
        self.lblpara = QtWidgets.QLabel(ImportPointSetFile)
        self.lblpara.setObjectName("lblpara")
        self.lblpara.setGeometry(QtCore.QRect(10, 100, 110, 30))
        self.lblinl = QtWidgets.QLabel(ImportPointSetFile)
        self.lblinl.setObjectName("lblinl")
        self.lblinl.setGeometry(QtCore.QRect(20, 140, 100, 30))
        self.cbbinl = QtWidgets.QComboBox(ImportPointSetFile)
        self.cbbinl.setObjectName("cbbinl")
        self.cbbinl.setGeometry(QtCore.QRect(130, 140, 60, 30))
        self.lblxl = QtWidgets.QLabel(ImportPointSetFile)
        self.lblxl.setObjectName("lblxl")
        self.lblxl.setGeometry(QtCore.QRect(20, 180, 100, 30))
        self.cbbxl = QtWidgets.QComboBox(ImportPointSetFile)
        self.cbbxl.setObjectName("cbbxl")
        self.cbbxl.setGeometry(QtCore.QRect(130, 180, 60, 30))
        self.lblz = QtWidgets.QLabel(ImportPointSetFile)
        self.lblz.setObjectName("lbz")
        self.lblz.setGeometry(QtCore.QRect(20, 220, 100, 30))
        self.cbbz = QtWidgets.QComboBox(ImportPointSetFile)
        self.cbbz.setObjectName("cbbz")
        self.cbbz.setGeometry(QtCore.QRect(130, 220, 60, 30))
        self.lblcomment = QtWidgets.QLabel(ImportPointSetFile)
        self.lblcomment.setObjectName("lblcomment")
        self.lblcomment.setGeometry(QtCore.QRect(220, 140, 100, 30))
        self.cbbcomment = QtWidgets.QComboBox(ImportPointSetFile)
        self.cbbcomment.setObjectName("cbbcomment")
        self.cbbcomment.setGeometry(QtCore.QRect(330, 140, 60, 30))
        #
        self.btnimport = QtWidgets.QPushButton(ImportPointSetFile)
        self.btnimport.setObjectName("btnimport")
        self.btnimport.setGeometry(QtCore.QRect(120, 270, 160, 30))
        self.btnimport.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ImportPointSetFile)
        self.msgbox.setObjectName("msgbox")
        _center_x = ImportPointSetFile.geometry().center().x()
        _center_y = ImportPointSetFile.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ImportPointSetFile)
        QtCore.QMetaObject.connectSlotsByName(ImportPointSetFile)


    def retranslateGUI(self, ImportPointSetFile):
        self.dialog = ImportPointSetFile
        #
        _translate = QtCore.QCoreApplication.translate
        ImportPointSetFile.setWindowTitle(_translate("ImportPointSetFile", "Import PointSet from File"))
        self.lblfile.setText(_translate("ImportPointSetFile", "Select pointset files:"))
        self.lblfile.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtfile.setText(_translate("ImportPointSetFile", os.path.abspath(self.rootpath)))
        self.btnfile.setText(_translate("ImportPointSetFile", "Browse"))
        self.btnfile.clicked.connect(self.clickBtnFile)
        self.lbltype.setText(_translate("ImportPointSetFile", "\t    Type:"))
        self.cbbtype.addItems(['Kingdom 3D interpretation lines (ASCII) (*.*)',
                               'Seisworks 3D interpretation (ASCII) (*.*)',
                               'Customized (ASCII) (*.*)'])
        self.cbbtype.currentIndexChanged.connect(self.changeCbbType)
        #
        self.lblpara.setText(_translate("ImportPointSetFile", "Settings:"))
        self.lblinl.setText(_translate("ImportPointSetFile", "Inline column"))
        self.lblinl.setAlignment(QtCore.Qt.AlignRight)
        self.cbbinl.addItems([str(i+1) for i in range(10)])
        self.cbbinl.setCurrentIndex(2)
        self.cbbinl.setEnabled(False)
        self.lblxl.setText(_translate("ImportPointSetFile", "Crossline column:"))
        self.lblxl.setAlignment(QtCore.Qt.AlignRight)
        self.cbbxl.addItems([str(i + 1) for i in range(10)])
        self.cbbxl.setCurrentIndex(3)
        self.cbbxl.setEnabled(False)
        self.lblz.setText(_translate("ImportPointSetFile", "Time/depth column:"))
        self.lblz.setAlignment(QtCore.Qt.AlignRight)
        self.cbbz.addItems([str(i + 1) for i in range(10)])
        self.cbbz.setCurrentIndex(4)
        self.cbbz.setEnabled(False)
        self.lblcomment.setText(_translate("ImportPointSetFile", "Header with "))
        self.lblcomment.setAlignment(QtCore.Qt.AlignRight)
        self.cbbcomment.addItems(['None', '#', '!'])
        self.cbbcomment.setCurrentIndex(0)
        self.cbbcomment.setEnabled(False)
        #
        self.btnimport.setText(_translate("ImportPointSetFile", "Import PointSet"))
        self.btnimport.clicked.connect(self.clickBtnImportPointSetFile)


    def clickBtnFile(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileNames(None, 'Select Point File(s)', self.rootpath,
                                         filter="All files (*.*)")
        if len(_file[0]) > 0:
            self.filelist = _file[0]
            self.ldtfile.setText(str(_file[0]))


    def changeCbbType(self):
        if self.cbbtype.currentIndex() == 0:
            self.cbbinl.setCurrentIndex(2)
            self.cbbinl.setEnabled(False)
            self.cbbxl.setCurrentIndex(3)
            self.cbbxl.setEnabled(False)
            self.cbbz.setCurrentIndex(4)
            self.cbbz.setEnabled(False)
            self.cbbcomment.setCurrentIndex(0)
            self.cbbcomment.setEnabled(False)
        if self.cbbtype.currentIndex() == 1:
            self.cbbinl.setCurrentIndex(0)
            self.cbbinl.setEnabled(False)
            self.cbbxl.setCurrentIndex(1)
            self.cbbxl.setEnabled(False)
            self.cbbz.setCurrentIndex(4)
            self.cbbz.setEnabled(False)
            self.cbbcomment.setCurrentIndex(0)
            self.cbbcomment.setEnabled(False)
        if self.cbbtype.currentIndex() == 2:
            self.cbbinl.setCurrentIndex(4)
            self.cbbinl.setEnabled(True)
            self.cbbxl.setCurrentIndex(3)
            self.cbbxl.setEnabled(True)
            self.cbbz.setCurrentIndex(2)
            self.cbbz.setEnabled(True)
            self.cbbcomment.setCurrentIndex(1)
            self.cbbcomment.setEnabled(True)


    def clickBtnImportPointSetFile(self):
        self.refreshMsgBox()
        #
        _nfile = len(self.filelist)
        if _nfile <= 0:
            print("ImagePointSetFile: No file selected for import")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import PointSet from File',
                                           'No file selected for import')
            return
        #
        # Progress dialog
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Import ' + str(_nfile) + ' PointSet files')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        _pgsdlg.setMaximum(_nfile)
        #
        _pointdata = {}
        #
        for i in range(_nfile):
            #
            QtCore.QCoreApplication.instance().processEvents()
            #
            _filename = self.filelist[i]
            print("ImportPointSetFile: Import %d of %d pointset files: %s" % (i + 1, _nfile, _filename))
            #
            _comment = None
            if self.cbbcomment.currentIndex() == 0:
                _comment = None
            if self.cbbcomment.currentIndex() == 1:
                _comment = '#'
            if self.cbbcomment.currentIndex() == 2:
                _comment = '!'
            #
            _filenamemain = os.path.splitext(os.path.basename(_filename))[0]
            _pointdata[_filenamemain] = {}
            #
            # _data = np.loadtxt(_filename, comments=_comment)
            # #
            # if self.cbbinl.currentIndex() < np.shape(_data)[1]:
            #     _pointdata[_filenamemain]['Inline'] = \
            #         _data[:, self.cbbinl.currentIndex():self.cbbinl.currentIndex() + 1]
            # if self.cbbxl.currentIndex() < np.shape(_data)[1]:
            #     _pointdata[_filenamemain]['Crossline'] = \
            #         _data[:, self.cbbxl.currentIndex():self.cbbxl.currentIndex() + 1]
            # if self.cbbz.currentIndex() < np.shape(_data)[1]:
            #     _pointdata[_filenamemain]['Z'] = \
            #         _data[:, self.cbbz.currentIndex():self.cbbz.currentIndex() + 1]
            # _idx = 1
            # for _i in range(np.shape(_data)[1]):
            #     if _i != self.cbbinl.currentIndex() \
            #         and _i != self.cbbxl.currentIndex() \
            #         and _i != self.cbbz.currentIndex():
            #         _propname = 'property_' + str(_idx)
            #         _idx = _idx + 1
            #         _pointdata[_filenamemain][_propname] = _data[:, _i:_i+1]
            _data = point_io.readPointFromAscii(_filename, comment=_comment,
                                                inlcol=self.cbbinl.currentIndex(),
                                                xlcol=self.cbbxl.currentIndex(),
                                                zcol=self.cbbz.currentIndex())
            _pointdata[_filenamemain]['Inline'] = _data[:, 0:1]
            _pointdata[_filenamemain]['Crossline'] = _data[:, 1:2]
            _pointdata[_filenamemain]['Z'] = _data[:, 2:3]
            for _i in range(np.shape(_data)[1]-3):
                _propname = 'property_' + str(_i+1)
                _pointdata[_filenamemain][_propname] = _data[:, _i+3:_i+4]
            #
            if 'Z' in _pointdata[_filenamemain].keys() and np.min(_pointdata[_filenamemain]['Z']) >= 0:
                _pointdata[_filenamemain]['Z'] = - _pointdata[_filenamemain]['Z']
            #
            _pgsdlg.setValue(i + 1)
            #
        #
        # add new data to seisdata
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
                                          "Import PointSet from File",
                                          str(_nfile) + " file(s) imported successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkPointData(self):
        if checkPointData(self.pointdata) is False:
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import PointSet from File',
                                           'No point found')
            return


def checkPointData(pointdata):
    if pointdata is None:
        return False
    for p in pointdata.keys():
        if pointdata[p] is None:
            return False
        if 'Inline' not in pointdata[p].keys():
            return False
        if 'Crossline' not in pointdata[p].keys():
            return False
        if 'Z' not in pointdata[p].keys():
            return False
    return True


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ImportPointSetFile = QtWidgets.QWidget()
    gui = importpointsetfile()
    gui.setupGUI(ImportPointSetFile)
    ImportPointSetFile.show()
    sys.exit(app.exec_())