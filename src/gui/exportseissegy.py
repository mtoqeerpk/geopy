#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for exporting seismic segys


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from seismic.inputoutput import inputoutput as seis_io
from seismic.analysis import analysis as seis_ays

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class exportseissegy(object):

    survinfo = {}
    seisdata = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, ExportSeisSegy):
        ExportSeisSegy.setObjectName("ExportSeisSegy")
        ExportSeisSegy.setFixedSize(400, 470)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ExportSeisSegy.setWindowIcon(icon)
        #
        self.lblattrib = QtWidgets.QLabel(ExportSeisSegy)
        self.lblattrib.setObjectName("lblattrib")
        self.lblattrib.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwgattrib = QtWidgets.QListWidget(ExportSeisSegy)
        self.lwgattrib.setObjectName("lwgattrib")
        self.lwgattrib.setGeometry(QtCore.QRect(160, 10, 230, 200))
        self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblsurvey = QtWidgets.QLabel(ExportSeisSegy)
        self.lblsurvey.setObjectName("lblsurvey")
        self.lblsurvey.setGeometry(QtCore.QRect(10, 230, 150, 30))
        self.rdbsurveynew = QtWidgets.QRadioButton(ExportSeisSegy)
        self.rdbsurveynew.setObjectName("rdbsurvey")
        self.rdbsurveynew.setGeometry(QtCore.QRect(10, 270, 190, 30))
        self.rdbsurveyref = QtWidgets.QRadioButton(ExportSeisSegy)
        self.rdbsurveyref.setObjectName("rdbsurvey")
        self.rdbsurveyref.setGeometry(QtCore.QRect(200, 270, 190, 30))
        self.ldtsurveyref = QtWidgets.QLineEdit(ExportSeisSegy)
        self.ldtsurveyref.setObjectName("ldtsurveyref")
        self.ldtsurveyref.setGeometry(QtCore.QRect(10, 310, 310, 30))
        self.btnsurveyref = QtWidgets.QPushButton(ExportSeisSegy)
        self.btnsurveyref.setObjectName("btnsurveyref")
        self.btnsurveyref.setGeometry(QtCore.QRect(330, 310, 60, 30))
        self.lblsave = QtWidgets.QLabel(ExportSeisSegy)
        self.lblsave.setObjectName("lblsave")
        self.lblsave.setGeometry(QtCore.QRect(10, 360, 50, 30))
        self.ldtsave = QtWidgets.QLineEdit(ExportSeisSegy)
        self.ldtsave.setObjectName("ldtsave")
        self.ldtsave.setGeometry(QtCore.QRect(70, 360, 250, 30))
        self.btnsave = QtWidgets.QPushButton(ExportSeisSegy)
        self.btnsave.setObjectName("btnsave")
        self.btnsave.setGeometry(QtCore.QRect(330, 360, 60, 30))
        self.btnexportsegy = QtWidgets.QPushButton(ExportSeisSegy)
        self.btnexportsegy.setObjectName("btnexportsegy")
        self.btnexportsegy.setGeometry(QtCore.QRect(120, 410, 160, 30))
        self.btnexportsegy.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ExportSeisSegy)
        self.msgbox.setObjectName("msgbox")
        _center_x = ExportSeisSegy.geometry().center().x()
        _center_y = ExportSeisSegy.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ExportSeisSegy)
        QtCore.QMetaObject.connectSlotsByName(ExportSeisSegy)


    def retranslateGUI(self, ExportSeisSegy):
        self.dialog = ExportSeisSegy
        #
        _translate = QtCore.QCoreApplication.translate
        ExportSeisSegy.setWindowTitle(_translate("ExportSeisSegy", "Export Seismic SEG-Y"))
        self.lblattrib.setText(_translate("ExportSeisSegy", "Select output properties:"))
        if self.checkSurvInfo() is True:
            _firstattrib = None
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i):
                    item = QtWidgets.QListWidgetItem(self.lwgattrib)
                    item.setText(_translate("ExportSeisSegy", i))
                    self.lwgattrib.addItem(item)
                    if _firstattrib is None:
                        _firstattrib = item
            self.lwgattrib.setCurrentItem(_firstattrib)
        self.lblsurvey.setText(_translate("ExportSeisSegy", "Setup output survey:"))
        self.rdbsurveynew.setText(_translate("ExportSeisSegy", "from input data dimensions"))
        self.rdbsurveynew.setChecked(True)
        self.rdbsurveynew.clicked.connect(self.clickRdbSurveyNew)
        self.rdbsurveyref.setText(_translate("ExportSeisSegy", "from a reference SEG-Y file"))
        self.rdbsurveyref.setChecked(False)
        self.rdbsurveyref.clicked.connect(self.clickRdbSurveyRef)
        self.ldtsurveyref.setText(_translate("ExportSeisSegy", ""))
        self.ldtsurveyref.setEnabled(False)
        self.btnsurveyref.setText(_translate("ExportSeisSegy", "Browse"))
        self.btnsurveyref.setEnabled(False)
        self.btnsurveyref.clicked.connect(self.clickBtnSurveyRef)
        self.lblsave.setText(_translate("ExportSeisSegy", "Save to:"))
        self.ldtsave.setText(_translate("ExportSeisSegy", os.path.abspath(self.rootpath)))
        self.btnsave.setText(_translate("ExportSeisSegy", "Browse"))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnexportsegy.setText(_translate("ExportSeisSegy", "Export Seismic SEG-Y"))
        self.btnexportsegy.clicked.connect(self.clickBtnExportSeisSegy)


    def clickRdbSurveyRef(self):
        if self.rdbsurveyref.isChecked():
            self.rdbsurveyref.setChecked(True)
            self.rdbsurveynew.setChecked(False)
            # self.ldtsurveyref.setText(os.path.abspath(self.rootpath))
            self.ldtsurveyref.setEnabled(True)
            self.btnsurveyref.setEnabled(True)


    def clickRdbSurveyNew(self):
        if self.rdbsurveynew.isChecked():
            self.rdbsurveyref.setChecked(False)
            self.rdbsurveynew.setChecked(True)
            self.ldtsurveyref.setText('')
            self.ldtsurveyref.setEnabled(False)
            self.btnsurveyref.setEnabled(False)


    def clickBtnSurveyRef(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select Reference SEG-Y', self.rootpath,
                                        filter="SEG-Y files (*.segy; *.sgy);; All files (*.*)")
        if len(_file[0]) > 0:
            self.ldtsurveyref.setText(_file[0])


    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getExistingDirectory(None, 'Select Export Folder', self.rootpath,
                                             options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if len(_file) > 0:
            self.ldtsave.setText(_file)


    def clickBtnExportSeisSegy(self):
        self.refreshMsgBox()
        #
        _attriblist = self.lwgattrib.selectedItems()
        if len(_attriblist) < 1:
            print("ExportSeisSegy: No property selected for export")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Export Seismic SEG-Y',
                                           'No property selected for export')
            return
        if self.rdbsurveyref.isChecked() and (os.path.exists(self.ldtsurveyref.text()) is False):
            print("ExportSeisSegy: Reference SEG-Y not found")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Export Seismic SEG-Y',
                                           'Reference SEG-Y not found')
            return
        # Progress dialog
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Export Seismic SEG-Y')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        #
        for i in range(len(_attriblist)):
            #
            _pgsdlg.setWindowTitle('Export '+str(i+1)+' of '+str(len(_attriblist))+' Seismic SEG-Y')
            #
            _segyfile = os.path.join(self.ldtsave.text(),
                                     _attriblist[i].text() + '.segy')
            print("ExportSeisSegy: Export %d of %d SEG-Y: %s" % (i + 1, len(_attriblist), _segyfile))
            _data = self.seisdata[_attriblist[i].text()]
            _data = np.reshape(_data, [_data.shape[0], -1])
            _data = np.mean(_data, axis=1)
            _data = np.reshape(_data, [len(_data), 1])
            _data = np.transpose(np.reshape(_data, [self.survinfo['ILNum'], self.survinfo['XLNum'], self.survinfo['ZNum']]),
                                 [2, 1, 0])
            if self.rdbsurveynew.isChecked():
                seis_io.writeSeis3DMatToSegyNoRef(_data, _segyfile,
                                                  inlstart=self.survinfo['ILStart'], inlstep=self.survinfo['ILStep'],
                                                  xlstart=self.survinfo['XLStart'], xlstep=self.survinfo['XLStep'],
                                                  zstart=self.survinfo['ZStart'], zstep=self.survinfo['ZStep'],
                                                  verbose=False,
                                                  qpgsdlg=_pgsdlg)
            else:
                _reffile = self.ldtsurveyref.text()
                seis_io.writeSeis3DMatToSegyWithRef(_data, _segyfile, _reffile, verbose=False,
                                                    qpgsdlg=_pgsdlg)
        # _pgsdlg.setValue(len(_attriblist) * _tracenum)
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Export Seismic SEG-Y",
                                          str(len(_attriblist)) + " properties exported as SEG-Y successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkSurvInfo(self):
        self.refreshMsgBox()
        #
        if seis_ays.checkSeisInfo(self.survinfo) is False:
            # print("ExportSeisSegy: Survey not found")
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Export Seismic SEG-Y',
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
    ExportSeisSegy = QtWidgets.QWidget()
    gui = exportseissegy()
    gui.setupGUI(ExportSeisSegy)
    ExportSeisSegy.show()
    sys.exit(app.exec_())