#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for import survey from a seismic segy


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


class importsurveysegy(object):

    survinfo = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None
    #
    segyfile = ''

    def setupGUI(self, ImportSurveySegy):
        ImportSurveySegy.setObjectName("ImportSurveySegy")
        ImportSurveySegy.setFixedSize(480, 330)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ImportSurveySegy.setWindowIcon(icon)
        self.lblsegy = QtWidgets.QLabel(ImportSurveySegy)
        self.lblsegy.setObjectName("lblsegy")
        self.lblsegy.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtsegy = QtWidgets.QLineEdit(ImportSurveySegy)
        self.ldtsegy.setObjectName("ldtisegy")
        self.ldtsegy.setGeometry(QtCore.QRect(110, 10, 290, 30))
        self.btnsegy = QtWidgets.QPushButton(ImportSurveySegy)
        self.btnsegy.setObjectName("btnsegy")
        self.btnsegy.setGeometry(QtCore.QRect(410, 10, 60, 30))
        #
        self.lblview = QtWidgets.QLabel(ImportSurveySegy)
        self.lblview.setObjectName("lblview")
        self.lblview.setGeometry(QtCore.QRect(10, 50, 100, 30))
        self.btntextualheader = QtWidgets.QPushButton(ImportSurveySegy)
        self.btntextualheader.setObjectName("btntextualheader")
        self.btntextualheader.setGeometry(QtCore.QRect(30, 90, 140, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/view.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btntextualheader.setIcon(icon)
        self.btnbinaryheader = QtWidgets.QPushButton(ImportSurveySegy)
        self.btnbinaryheader.setObjectName("btnbinaryheader")
        self.btnbinaryheader.setGeometry(QtCore.QRect(180, 90, 140, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/view.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnbinaryheader.setIcon(icon)
        self.btntraceheader = QtWidgets.QPushButton(ImportSurveySegy)
        self.btntraceheader.setObjectName("btntraceheader")
        self.btntraceheader.setGeometry(QtCore.QRect(330, 90, 140, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/view.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btntraceheader.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(ImportSurveySegy)
        self.lblpara.setObjectName("lbltraceheader")
        self.lblpara.setGeometry(QtCore.QRect(10, 140, 100, 30))
        self.lblx = QtWidgets.QLabel(ImportSurveySegy)
        self.lblx.setObjectName("lblx")
        self.lblx.setGeometry(QtCore.QRect(30, 180, 150, 30))
        self.cbbx = QtWidgets.QComboBox(ImportSurveySegy)
        self.cbbx.setObjectName("cbbx")
        self.cbbx.setGeometry(QtCore.QRect(180, 180, 60, 30))
        self.lbly = QtWidgets.QLabel(ImportSurveySegy)
        self.lbly.setObjectName("lbly")
        self.lbly.setGeometry(QtCore.QRect(260, 180, 150, 30))
        self.cbby = QtWidgets.QComboBox(ImportSurveySegy)
        self.cbby.setObjectName("cbby")
        self.cbby.setGeometry(QtCore.QRect(410, 180, 60, 30))
        self.lblinl = QtWidgets.QLabel(ImportSurveySegy)
        self.lblinl.setObjectName("lblinl")
        self.lblinl.setGeometry(QtCore.QRect(30, 220, 150, 30))
        self.cbbinl = QtWidgets.QComboBox(ImportSurveySegy)
        self.cbbinl.setObjectName("cbbinl")
        self.cbbinl.setGeometry(QtCore.QRect(180, 220, 60, 30))
        self.lblxl = QtWidgets.QLabel(ImportSurveySegy)
        self.lblxl.setObjectName("lblxl")
        self.lblxl.setGeometry(QtCore.QRect(260, 220, 150, 30))
        self.cbbxl = QtWidgets.QComboBox(ImportSurveySegy)
        self.cbbxl.setObjectName("cbbxl")
        self.cbbxl.setGeometry(QtCore.QRect(410, 220, 60, 30))
        #
        self.btnimport = QtWidgets.QPushButton(ImportSurveySegy)
        self.btnimport.setObjectName("btnimport")
        self.btnimport.setGeometry(QtCore.QRect(160, 270, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnimport.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ImportSurveySegy)
        self.msgbox.setObjectName("msgbox")
        _center_x = ImportSurveySegy.geometry().center().x()
        _center_y = ImportSurveySegy.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ImportSurveySegy)
        QtCore.QMetaObject.connectSlotsByName(ImportSurveySegy)


    def retranslateGUI(self, ImportSurveySegy):
        self.dialog = ImportSurveySegy
        #
        _translate = QtCore.QCoreApplication.translate
        ImportSurveySegy.setWindowTitle(_translate("ImportSurveySegy", "Import Survey from Seismic SEG-Y"))
        self.lblsegy.setText(_translate("ImportSurveySegy", "Select SEG-Y:"))
        self.ldtsegy.setText(_translate("ImportSurveySegy", os.path.abspath(self.rootpath)))
        self.btnsegy.setText(_translate("ImportSurveySegy", "Browse"))
        self.btnsegy.clicked.connect(self.clickBtnSegy)
        #
        self.lblview.setText(_translate("ImportSurveySegy", "View SEG-Y:"))
        self.btntextualheader.setText(_translate("ImportSurveySegy", "Textual Header"))
        self.btntextualheader.clicked.connect(self.clickBtnTextualHeader)
        self.btnbinaryheader.setText(_translate("ImportSurveySegy", "Binary Header"))
        self.btnbinaryheader.clicked.connect(self.clickBtnBinaryHeader)
        self.btntraceheader.setText(_translate("ImportSurveySegy", "Trace Header"))
        self.btntraceheader.clicked.connect(self.clickBtnTraceHeader)
        self.lblpara.setText(_translate("ImportSurveySegy", "Import settings:"))
        self.lblx.setText(_translate("ImportSurveySegy", "X coordinate at byte"))
        self.cbbx.addItems([str(i+1) for i in range(240)])
        self.cbbx.setCurrentIndex(180)
        self.lbly.setText(_translate("ImportSurveySegy", "Y coordinate at byte"))
        self.cbby.addItems([str(i + 1) for i in range(240)])
        self.cbby.setCurrentIndex(184)
        self.lblinl.setText(_translate("ImportSurveySegy", "Inline number at byte"))
        self.cbbinl.addItems([str(i + 1) for i in range(240)])
        self.cbbinl.setCurrentIndex(188)
        self.lblxl.setText(_translate("ImportSurveySegy", "Crossline number at byte"))
        self.cbbxl.addItems([str(i + 1) for i in range(240)])
        self.cbbxl.setCurrentIndex(192)
        #
        self.btnimport.setText(_translate("ImportSurveySegy", "Import SEG-Y"))
        self.btnimport.setDefault(True)
        self.btnimport.clicked.connect(self.clickBtnImport)


    def clickBtnSegy(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select Seismic SEG-Y', self.rootpath,
                                         filter="SEG-Y files (*.segy; *.sgy);;All files (*.*)")
        if len(_file[0]) > 0:
            self.segyfile = _file[0]
            self.ldtsegy.setText(str(_file[0]))


    def clickBtnTextualHeader(self):
        self.refreshMsgBox()
        #
        if os.path.exists(self.segyfile) is False or os.path.isfile(self.segyfile) is False:
            print("ImportSurveySegy: No SEG-Y selected for viewing textual header")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Survey from Seismic SEG-Y',
                                           'No SEG-Y selected for viewing textual header')
            return
        _viewheader = QtWidgets.QDialog()
        _gui = gui_viewsegytextualheader()
        _gui.segyfile = self.segyfile
        _gui.setupGUI(_viewheader)
        _viewheader.exec()
        _viewheader.show()


    def clickBtnBinaryHeader(self):
        self.refreshMsgBox()
        #
        if os.path.exists(self.segyfile) is False or os.path.isfile(self.segyfile) is False:
            print("ImportSurveySegy: No SEG-Y selected for viewing binary header")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Survey from Seismic SEG-Y',
                                           'No SEG-Y selected for viewing binary header')
            return
        _viewheader = QtWidgets.QDialog()
        _gui = gui_viewsegybinaryheader()
        _gui.segyfile = self.segyfile
        _gui.setupGUI(_viewheader)
        _viewheader.exec()
        _viewheader.show()


    def clickBtnTraceHeader(self):
        self.refreshMsgBox()
        #
        if os.path.exists(self.segyfile) is False or os.path.isfile(self.segyfile) is False:
            print("ImportSurveySegy: No SEG-Y selected for viewing trace header")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Survey from Seismic SEG-Y',
                                           'No SEG-Y selected for viewing trace header')
            return
        _viewheader = QtWidgets.QDialog()
        _gui = gui_viewsegytraceheader()
        _gui.segyfile = self.segyfile
        _gui.setupGUI(_viewheader)
        _viewheader.exec()
        _viewheader.show()


    def clickBtnImport(self):
        self.refreshMsgBox()
        #
        if os.path.exists(self.segyfile) is False or os.path.isfile(self.segyfile) is False:
            print("ImportSurveySegy: No SEG-Y selected for import")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Survey from Seismic SEG-Y',
                                           'No SEG-Y selected for import')
            return
        # format trace header format
        _traceheaderformat = seis_io.defSegyTraceHeaderFormat(x_byte=self.cbbx.currentIndex()+1,
                                                              y_byte=self.cbby.currentIndex() + 1,
                                                              inl_byte=self.cbbinl.currentIndex()+1,
                                                              xl_byte=self.cbbxl.currentIndex()+1)
        #
        _survinfo = seis_io.readSeisInfoFromSegy(self.segyfile,
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
        if seis_ays.checkSeisInfo(_survinfo):
            self.survinfo = _survinfo
        self.checkSurvInfo()
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Import Survey from Seismic SEG-Y",
                                          " Survey imported successfully")
        #
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkSurvInfo(self):
        self.refreshMsgBox()
        #
        if checkSurvInfo(self.survinfo) is False:
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Import Seismic SEG-Y',
                                           'No survey found')
            return


def checkSurvInfo(survinfo):
    return seis_ays.checkSeisInfo(survinfo)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ImportSurveySegy = QtWidgets.QWidget()
    gui = importsurveysegy()
    gui.setupGUI(ImportSurveySegy)
    ImportSurveySegy.show()
    sys.exit(app.exec_())