#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for import pre-stack seismic segys


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4])
from psseismic.inputoutput import inputoutput as psseis_io
from psseismic.analysis import analysis as psseis_ays
from gui.viewsegytextualheader import viewsegytextualheader as gui_viewsegytextualheader
from gui.viewsegybinaryheader import viewsegybinaryheader as gui_viewsegybinaryheader
from gui.viewsegytraceheader import viewsegytraceheader as gui_viewsegytraceheader

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class importpsseissegy(object):

    psseisdata = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None
    #
    segylist = []

    def setupGUI(self, ImportPsSeisSegy):
        ImportPsSeisSegy.setObjectName("ImportPsSeisSegy")
        ImportPsSeisSegy.setFixedSize(480, 280)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ImportPsSeisSegy.setWindowIcon(icon)
        self.lblsegy = QtWidgets.QLabel(ImportPsSeisSegy)
        self.lblsegy.setObjectName("lblsegy")
        self.lblsegy.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtsegy = QtWidgets.QLineEdit(ImportPsSeisSegy)
        self.ldtsegy.setObjectName("ldtisegy")
        self.ldtsegy.setGeometry(QtCore.QRect(110, 10, 290, 30))
        self.btnsegy = QtWidgets.QPushButton(ImportPsSeisSegy)
        self.btnsegy.setObjectName("btnsegy")
        self.btnsegy.setGeometry(QtCore.QRect(410, 10, 60, 30))
        #
        self.lblview = QtWidgets.QLabel(ImportPsSeisSegy)
        self.lblview.setObjectName("lblview")
        self.lblview.setGeometry(QtCore.QRect(10, 50, 100, 30))
        self.btntextualheader = QtWidgets.QPushButton(ImportPsSeisSegy)
        self.btntextualheader.setObjectName("btntextualheader")
        self.btntextualheader.setGeometry(QtCore.QRect(30, 90, 140, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/view.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btntextualheader.setIcon(icon)
        self.btnbinaryheader = QtWidgets.QPushButton(ImportPsSeisSegy)
        self.btnbinaryheader.setObjectName("btnbinaryheader")
        self.btnbinaryheader.setGeometry(QtCore.QRect(180, 90, 140, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/view.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnbinaryheader.setIcon(icon)
        self.btntraceheader = QtWidgets.QPushButton(ImportPsSeisSegy)
        self.btntraceheader.setObjectName("btntraceheader")
        self.btntraceheader.setGeometry(QtCore.QRect(330, 90, 140, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/view.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btntraceheader.setIcon(icon)
        #
        self.lblpara = QtWidgets.QLabel(ImportPsSeisSegy)
        self.lblpara.setObjectName("lbltraceheader")
        self.lblpara.setGeometry(QtCore.QRect(10, 140, 100, 30))
        self.lblrecord = QtWidgets.QLabel(ImportPsSeisSegy)
        self.lblrecord.setObjectName("lblrecord")
        self.lblrecord.setGeometry(QtCore.QRect(30, 180, 150, 30))
        self.cbbrecord = QtWidgets.QComboBox(ImportPsSeisSegy)
        self.cbbrecord.setObjectName("cbbrecord")
        self.cbbrecord.setGeometry(QtCore.QRect(180, 180, 60, 30))
        self.lbltrace = QtWidgets.QLabel(ImportPsSeisSegy)
        self.lbltrace.setObjectName("lbltrace")
        self.lbltrace.setGeometry(QtCore.QRect(260, 180, 150, 30))
        self.cbbtrace = QtWidgets.QComboBox(ImportPsSeisSegy)
        self.cbbtrace.setObjectName("cbbtrace")
        self.cbbtrace.setGeometry(QtCore.QRect(410, 180, 60, 30))
        #
        self.btnimport = QtWidgets.QPushButton(ImportPsSeisSegy)
        self.btnimport.setObjectName("btnimport")
        self.btnimport.setGeometry(QtCore.QRect(160, 230, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnimport.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ImportPsSeisSegy)
        self.msgbox.setObjectName("msgbox")
        _center_x = ImportPsSeisSegy.geometry().center().x()
        _center_y = ImportPsSeisSegy.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ImportPsSeisSegy)
        QtCore.QMetaObject.connectSlotsByName(ImportPsSeisSegy)


    def retranslateGUI(self, ImportPsSeisSegy):
        self.dialog = ImportPsSeisSegy
        #
        _translate = QtCore.QCoreApplication.translate
        ImportPsSeisSegy.setWindowTitle(_translate("ImportPsSeisSegy", "Import Pre-stack Seismic SEG-Y"))
        self.lblsegy.setText(_translate("ImportPsSeisSegy", "Select SEG-Y(s):"))
        self.ldtsegy.setText(_translate("ImportPsSeisSegy", os.path.abspath(self.rootpath)))
        self.btnsegy.setText(_translate("ImportPsSeisSegy", "Browse"))
        self.btnsegy.clicked.connect(self.clickBtnSegy)
        #
        self.lblview.setText(_translate("ImportPsSeisSegy", "View 1st SEG-Y:"))
        self.btntextualheader.setText(_translate("ImportPsSeisSegy", "Textual Header"))
        self.btntextualheader.clicked.connect(self.clickBtnTextualHeader)
        self.btnbinaryheader.setText(_translate("ImportPsSeisSegy", "Binary Header"))
        self.btnbinaryheader.clicked.connect(self.clickBtnBinaryHeader)
        self.btntraceheader.setText(_translate("ImportPsSeisSegy", "Trace Header"))
        self.btntraceheader.clicked.connect(self.clickBtnTraceHeader)
        #
        self.lblpara.setText(_translate("ImportPsSeisSegy", "Import settings:"))
        self.lblrecord.setText(_translate("ImportPsSeisSegy", "Record number at byte"))
        self.cbbrecord.addItems([str(i + 1) for i in range(240)])
        self.cbbrecord.setCurrentIndex(8)
        self.lbltrace.setText(_translate("ImportPsSeisSegy", "Trace number at byte"))
        self.cbbtrace.addItems([str(i + 1) for i in range(240)])
        self.cbbtrace.setCurrentIndex(12)
        #
        self.btnimport.setText(_translate("ImportPsSeisSegy", "Import SEG-Y"))
        self.btnimport.clicked.connect(self.clickBtnImport)


    def clickBtnSegy(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileNames(None, 'Select Pre-stack Seismic SEG-Y(s)', self.rootpath,
                                         filter="SEG-Y files (*.segy; *.sgy);;All files (*.*)")
        if len(_file[0]) > 0:
            self.segylist = _file[0]
            self.ldtsegy.setText(str(_file[0]))


    def clickBtnTextualHeader(self):
        self.refreshMsgBox()
        #
        _nfile = len(self.segylist)
        if _nfile <= 0:
            print("ImportPsSeisSegy: No SEG-Y selected for viewing textual header")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Pre-stack Seismic SEG-Y',
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
            print("ImportPsSeisSegy: No SEG-Y selected for viewing binary header")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Pre-stack Seismic SEG-Y',
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
            print("ImportPsSeisSegy: No SEG-Y selected for viewing trace header")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import SEG-Y',
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
            print("ImportPsSeisSegy: No SEG-Y selected for import")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Pre-stack Seismic SEG-Y',
                                           'No SEG-Y selected for import')
            return
        # format trace header format
        _traceheaderformat = psseis_io.defSegyTraceHeaderFormat(record_byte=self.cbbrecord.currentIndex() + 1,
                                                                trace_byte=self.cbbtrace.currentIndex() + 1)
        #
        # Progress dialog
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Import ' + str(_nfile) + ' Pre-stack Seismic SEG-Y')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        #
        _psseisdata = {}
        #
        for i in range(_nfile):
            #
            _pgsdlg.setWindowTitle('Import ' + str(i + 1) + ' of ' + str(_nfile) + ' Pre-stack Seismic SEG-Y')
            #
            _filename = self.segylist[i]
            print("ImportPsSeisSegy: Import %d of %d SEG-Y: %s" % (i + 1, _nfile, _filename))
            _filenamemain = os.path.splitext(os.path.basename(_filename))[0]
            _psseisdata[_filenamemain] = psseis_io.readPsSeisFromSegy(_filename,
                                                                      traceheaderformat=_traceheaderformat,
                                                                      qpgsdlg=_pgsdlg)
            #
        # add new data to psseisdata
        for key in _psseisdata.keys():
            if key in self.psseisdata.keys()and checkPsSeisData(self.psseisdata[key]):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Pre-stack Seismic SEG-Y',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.psseisdata[key] = _psseisdata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Pre-stack Seismic SEG-Y",
                                          str(_nfile) + " SEG-Y imported successfully")
        #
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


def checkPsSeisData(psseisdata):
    return psseis_ays.checkPsSeis(psseisdata)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ImportPsSeisSegy = QtWidgets.QWidget()
    gui = importpsseissegy()
    gui.setupGUI(ImportPsSeisSegy)
    ImportPsSeisSegy.show()
    sys.exit(app.exec_())