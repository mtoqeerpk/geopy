#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for import seismic segys


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4])
from seismic.inputoutput import inputoutput as seis_io
from seismic.analysis import analysis as seis_ays
from gui.viewsegytextualheader import viewsegytextualheader as gui_viewsegytextualheader
from gui.viewsegybinaryheader import viewsegybinaryheader as gui_viewsegybinaryheader
from gui.viewsegytraceheader import viewsegytraceheader as gui_viewsegytraceheader

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class importseissegy(object):

    survinfo = {}
    seisdata = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None
    #
    segylist = []

    def setupGUI(self, ImportSeisSegy):
        ImportSeisSegy.setObjectName("ImportSeisSegy")
        ImportSeisSegy.setFixedSize(480, 320)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ImportSeisSegy.setWindowIcon(icon)
        self.lblsegy = QtWidgets.QLabel(ImportSeisSegy)
        self.lblsegy.setObjectName("lblsegy")
        self.lblsegy.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtsegy = QtWidgets.QLineEdit(ImportSeisSegy)
        self.ldtsegy.setObjectName("ldtisegy")
        self.ldtsegy.setGeometry(QtCore.QRect(110, 10, 290, 30))
        self.btnsegy = QtWidgets.QPushButton(ImportSeisSegy)
        self.btnsegy.setObjectName("btnsegy")
        self.btnsegy.setGeometry(QtCore.QRect(410, 10, 60, 30))
        #
        self.lblview = QtWidgets.QLabel(ImportSeisSegy)
        self.lblview.setObjectName("lblview")
        self.lblview.setGeometry(QtCore.QRect(10, 50, 100, 30))
        self.btntextualheader = QtWidgets.QPushButton(ImportSeisSegy)
        self.btntextualheader.setObjectName("btntextualheader")
        self.btntextualheader.setGeometry(QtCore.QRect(30, 90, 140, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/view.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btntextualheader.setIcon(icon)
        self.btnbinaryheader = QtWidgets.QPushButton(ImportSeisSegy)
        self.btnbinaryheader.setObjectName("btnbinaryheader")
        self.btnbinaryheader.setGeometry(QtCore.QRect(180, 90, 140, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/view.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnbinaryheader.setIcon(icon)
        self.btntraceheader = QtWidgets.QPushButton(ImportSeisSegy)
        self.btntraceheader.setObjectName("btntraceheader")
        self.btntraceheader.setGeometry(QtCore.QRect(330, 90, 140, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/view.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btntraceheader.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(ImportSeisSegy)
        self.lblpara.setObjectName("lbltraceheader")
        self.lblpara.setGeometry(QtCore.QRect(10, 140, 100, 30))
        self.lblx = QtWidgets.QLabel(ImportSeisSegy)
        self.lblx.setObjectName("lblx")
        self.lblx.setGeometry(QtCore.QRect(30, 180, 150, 30))
        self.cbbx = QtWidgets.QComboBox(ImportSeisSegy)
        self.cbbx.setObjectName("cbbx")
        self.cbbx.setGeometry(QtCore.QRect(180, 180, 60, 30))
        self.lbly = QtWidgets.QLabel(ImportSeisSegy)
        self.lbly.setObjectName("lbly")
        self.lbly.setGeometry(QtCore.QRect(260, 180, 150, 30))
        self.cbby = QtWidgets.QComboBox(ImportSeisSegy)
        self.cbby.setObjectName("cbby")
        self.cbby.setGeometry(QtCore.QRect(410, 180, 60, 30))
        self.lblinl = QtWidgets.QLabel(ImportSeisSegy)
        self.lblinl.setObjectName("lblinl")
        self.lblinl.setGeometry(QtCore.QRect(30, 220, 150, 30))
        self.cbbinl = QtWidgets.QComboBox(ImportSeisSegy)
        self.cbbinl.setObjectName("cbbinl")
        self.cbbinl.setGeometry(QtCore.QRect(180, 220, 60, 30))
        self.lblxl = QtWidgets.QLabel(ImportSeisSegy)
        self.lblxl.setObjectName("lblxl")
        self.lblxl.setGeometry(QtCore.QRect(260, 220, 150, 30))
        self.cbbxl = QtWidgets.QComboBox(ImportSeisSegy)
        self.cbbxl.setObjectName("cbbxl")
        self.cbbxl.setGeometry(QtCore.QRect(410, 220, 60, 30))
        #
        self.btnimport = QtWidgets.QPushButton(ImportSeisSegy)
        self.btnimport.setObjectName("btnimport")
        self.btnimport.setGeometry(QtCore.QRect(160, 270, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnimport.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ImportSeisSegy)
        self.msgbox.setObjectName("msgbox")
        _center_x = ImportSeisSegy.geometry().center().x()
        _center_y = ImportSeisSegy.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ImportSeisSegy)
        QtCore.QMetaObject.connectSlotsByName(ImportSeisSegy)


    def retranslateGUI(self, ImportSeisSegy):
        self.dialog = ImportSeisSegy
        #
        _translate = QtCore.QCoreApplication.translate
        ImportSeisSegy.setWindowTitle(_translate("ImportSeisSegy", "Import Seismic SEG-Y"))
        self.lblsegy.setText(_translate("ImportSeisSegy", "Select SEG-Y(s):"))
        self.ldtsegy.setText(_translate("ImportSeisSegy", os.path.abspath(self.rootpath)))
        self.btnsegy.setText(_translate("ImportSeisSegy", "Browse"))
        self.btnsegy.clicked.connect(self.clickBtnSegy)
        #
        self.lblview.setText(_translate("ImportSeisSegy", "View 1st SEG-Y:"))
        self.btntextualheader.setText(_translate("ImportSeisSegy", "Textual Header"))
        self.btntextualheader.clicked.connect(self.clickBtnTextualHeader)
        self.btnbinaryheader.setText(_translate("ImportSeisSegy", "Binary Header"))
        self.btnbinaryheader.clicked.connect(self.clickBtnBinaryHeader)
        self.btntraceheader.setText(_translate("ImportSeisSegy", "Trace Header"))
        self.btntraceheader.clicked.connect(self.clickBtnTraceHeader)
        self.lblpara.setText(_translate("ImportSeisSegy", "Import settings:"))
        self.lblx.setText(_translate("ImportSeisSegy", "X coordinate at byte"))
        self.cbbx.addItems([str(i+1) for i in range(240)])
        self.cbbx.setCurrentIndex(180)
        self.lbly.setText(_translate("ImportSeisSegy", "Y coordinate at byte"))
        self.cbby.addItems([str(i + 1) for i in range(240)])
        self.cbby.setCurrentIndex(184)
        self.lblinl.setText(_translate("ImportSeisSegy", "Inline number at byte"))
        self.cbbinl.addItems([str(i + 1) for i in range(240)])
        self.cbbinl.setCurrentIndex(188)
        self.lblxl.setText(_translate("ImportSeisSegy", "Crossline number at byte"))
        self.cbbxl.addItems([str(i + 1) for i in range(240)])
        self.cbbxl.setCurrentIndex(192)
        #
        self.btnimport.setText(_translate("ImportSeisSegy", "Import SEG-Y"))
        self.btnimport.setDefault(True)
        self.btnimport.clicked.connect(self.clickBtnImport)


    def clickBtnSegy(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileNames(None, 'Select Seismic SEG-Y(s)', self.rootpath,
                                         filter="SEG-Y files (*.segy; *.sgy);;All files (*.*)")
        if len(_file[0]) > 0:
            self.segylist = _file[0]
            self.ldtsegy.setText(str(_file[0]))


    def clickBtnTextualHeader(self):
        self.refreshMsgBox()
        #
        _nfile = len(self.segylist)
        if _nfile <= 0:
            print("ImportSeisSegy: No SEG-Y selected for viewing textual header")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import SEG-Y',
                                           'No SEG-Y selected for viewing textual header')
            return
        _viewheader = QtWidgets.QDialog()
        _gui = gui_viewsegytextualheader()
        _gui.segyfile = self.segylist[0]
        _gui.setupGUI(_viewheader)
        _viewheader.exec()
        _viewheader.show()


    def clickBtnBinaryHeader(self):
        self.refreshMsgBox()
        #
        _nfile = len(self.segylist)
        if _nfile <= 0:
            print("ImportSeisSegy: No SEG-Y selected for viewing binary header")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Seismic SEG-Y',
                                           'No SEG-Y selected for viewing binary header')
            return
        _viewheader = QtWidgets.QDialog()
        _gui = gui_viewsegybinaryheader()
        _gui.segyfile = self.segylist[0]
        _gui.setupGUI(_viewheader)
        _viewheader.exec()
        _viewheader.show()


    def clickBtnTraceHeader(self):
        self.refreshMsgBox()
        #
        _nfile = len(self.segylist)
        if _nfile <= 0:
            print("ImportSeisSegy: No SEG-Y selected for viewing trace header")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Seismic SEG-Y',
                                           'No SEG-Y selected for viewing trace header')
            return
        _viewheader = QtWidgets.QDialog()
        _gui = gui_viewsegytraceheader()
        _gui.segyfile = self.segylist[0]
        _gui.setupGUI(_viewheader)
        _viewheader.exec()
        _viewheader.show()


    def clickBtnImport(self):
        self.refreshMsgBox()
        #
        _nfile = len(self.segylist)
        if _nfile <= 0:
            print("ImportSeisSegy: No SEG-Y selected for import")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Seismic SEG-Y',
                                           'No SEG-Y selected for import')
            return
        # format trace header format
        _traceheaderformat = seis_io.defSegyTraceHeaderFormat(x_byte=self.cbbx.currentIndex()+1,
                                                              y_byte=self.cbby.currentIndex() + 1,
                                                              inl_byte=self.cbbinl.currentIndex()+1,
                                                              xl_byte=self.cbbxl.currentIndex()+1)
        #
        # Progress dialog
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Import ' + str(_nfile) + ' Seismic SEG-Y')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        #
        _seisdata = {}
        #
        _survinfo = seis_io.readSeisInfoFromSegy(self.segylist[0],
                                                 traceheaderformat=_traceheaderformat)
        print("SEG-Y survey information:")
        print("----- Dimension (inline x crossline x time/depth) : %d x %d x %d"
              % (_survinfo['ILNum'], _survinfo['XLNum'], _survinfo['ZNum']))
        print("----- Inline range (start, end, step): %d, %d, %d"
              % (_survinfo['ILStart'], _survinfo['ILEnd'], _survinfo['ILStep']))
        print("----- Crossline range (start, end, step): %d, %d, %d"
              % (_survinfo['XLStart'], _survinfo['XLEnd'], _survinfo['XLStep']))
        print("----- Time/depth range (start, end, step): %d, %d, %d"
              % (_survinfo['ZStart'], _survinfo['ZEnd'], _survinfo['ZStep']))
        #
        for i in range(_nfile):
            #
            _pgsdlg.setWindowTitle('Import ' + str(i + 1) + ' of ' + str(_nfile) + ' Seismic SEG-Y')
            #
            _filename = self.segylist[i]
            print("ImportSeisSegy: Import %d of %d SEG-Y: %s" % (i + 1, _nfile, _filename))
            _segydata = seis_io.readSeis3DMatFromSegyWithInfo(_filename, seisinfo=_survinfo,
                                                              traceheaderformat=_traceheaderformat,
                                                              qpgsdlg=_pgsdlg)
            _segydata = np.reshape(np.transpose(_segydata, [2, 1, 0]), [-1, 1])
            if checkSeisData(_segydata, _survinfo):
                _filenamemain = os.path.splitext(os.path.basename(_filename))[0]
                _seisdata[_filenamemain] = _segydata
            #
        # add new data to seisdata
        if checkSurvInfo(_survinfo):
            self.survinfo = _survinfo
        for key in _seisdata.keys():
            if key in self.seisdata.keys() and checkSeisData(self.seisdata[key], self.survinfo):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Seismic SEG-Y',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.seisdata[key] = _seisdata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Seismic SEG-Y",
                                          str(_nfile) + " SEG-Y imported successfully")
        #
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
    ImportSeisSegy = QtWidgets.QWidget()
    gui = importseissegy()
    gui.setupGUI(ImportSeisSegy)
    ImportSeisSegy.show()
    sys.exit(app.exec_())