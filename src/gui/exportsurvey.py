#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     December 2018                                                                   #
#                                                                                           #
#############################################################################################

# Create a window for exporting seismic survey


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4])
from seismic.analysis import analysis as seis_ays

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class exportsurvey(object):

    survinfo = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, ExportSurvey):
        ExportSurvey.setObjectName("ExportSurvey")
        ExportSurvey.setFixedSize(500, 330)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/survey.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ExportSurvey.setWindowIcon(icon)
        self.lblsrvinfo = QtWidgets.QLabel(ExportSurvey)
        self.lblsrvinfo.setObjectName("lblsrvinfo")
        self.lblsrvinfo.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lblstart = QtWidgets.QLabel(ExportSurvey)
        self.lblstart.setObjectName("lblstart")
        self.lblstart.setGeometry(QtCore.QRect(120, 50, 80, 30))
        self.lblend = QtWidgets.QLabel(ExportSurvey)
        self.lblend.setObjectName("lblend")
        self.lblend.setGeometry(QtCore.QRect(220, 50, 80, 30))
        self.lblstep = QtWidgets.QLabel(ExportSurvey)
        self.lblstep.setObjectName("lblstep")
        self.lblstep.setGeometry(QtCore.QRect(320, 50, 40, 30))
        self.lblnum = QtWidgets.QLabel(ExportSurvey)
        self.lblnum.setObjectName("lblnum")
        self.lblnum.setGeometry(QtCore.QRect(380, 50, 80, 30))
        self.lblinl = QtWidgets.QLabel(ExportSurvey)
        self.lblinl.setObjectName("lblinl")
        self.lblinl.setGeometry(QtCore.QRect(10, 90, 100, 30))
        self.lblxl = QtWidgets.QLabel(ExportSurvey)
        self.lblxl.setObjectName("lblxl")
        self.lblxl.setGeometry(QtCore.QRect(10, 130, 100, 30))
        self.lblz = QtWidgets.QLabel(ExportSurvey)
        self.lblz.setObjectName("lblz")
        self.lblz.setGeometry(QtCore.QRect(10, 170, 100, 30))
        self.ldtinlstart = QtWidgets.QLineEdit(ExportSurvey)
        self.ldtinlstart.setObjectName("ldtinlstart")
        self.ldtinlstart.setGeometry(QtCore.QRect(120, 90, 80, 30))
        self.ldtinlend = QtWidgets.QLineEdit(ExportSurvey)
        self.ldtinlend.setObjectName("ldtinlend")
        self.ldtinlend.setGeometry(QtCore.QRect(220, 90, 80, 30))
        self.ldtinlstep = QtWidgets.QLineEdit(ExportSurvey)
        self.ldtinlstep.setObjectName("ldtinlstep")
        self.ldtinlstep.setGeometry(QtCore.QRect(320, 90, 40, 30))
        self.ldtinlnum = QtWidgets.QLineEdit(ExportSurvey)
        self.ldtinlnum.setObjectName("ldtinlnum")
        self.ldtinlnum.setGeometry(QtCore.QRect(380, 90, 80, 30))
        self.ldtxlstart = QtWidgets.QLineEdit(ExportSurvey)
        self.ldtxlstart.setObjectName("ldtxlstart")
        self.ldtxlstart.setGeometry(QtCore.QRect(120, 130, 80, 30))
        self.ldtxlend = QtWidgets.QLineEdit(ExportSurvey)
        self.ldtxlend.setObjectName("ldtxlend")
        self.ldtxlend.setGeometry(QtCore.QRect(220, 130, 80, 30))
        self.ldtxlstep = QtWidgets.QLineEdit(ExportSurvey)
        self.ldtxlstep.setObjectName("ldtxlstep")
        self.ldtxlstep.setGeometry(QtCore.QRect(320, 130, 40, 30))
        self.ldtxlnum = QtWidgets.QLineEdit(ExportSurvey)
        self.ldtxlnum.setObjectName("ldtxlnum")
        self.ldtxlnum.setGeometry(QtCore.QRect(380, 130, 80, 30))
        self.ldtzstart = QtWidgets.QLineEdit(ExportSurvey)
        self.ldtzstart.setObjectName("ldtzstart")
        self.ldtzstart.setGeometry(QtCore.QRect(120, 170, 80, 30))
        self.ldtzend = QtWidgets.QLineEdit(ExportSurvey)
        self.ldtzend.setObjectName("ldtzend")
        self.ldtzend.setGeometry(QtCore.QRect(220, 170, 80, 30))
        self.ldtzstep = QtWidgets.QLineEdit(ExportSurvey)
        self.ldtzstep.setObjectName("ldtzlstep")
        self.ldtzstep.setGeometry(QtCore.QRect(320, 170, 40, 30))
        self.ldtznum = QtWidgets.QLineEdit(ExportSurvey)
        self.ldtznum.setObjectName("ldtznum")
        self.ldtznum.setGeometry(QtCore.QRect(380, 170, 80, 30))
        self.lblsave = QtWidgets.QLabel(ExportSurvey)
        self.lblsave.setObjectName("lblsave")
        self.lblsave.setGeometry(QtCore.QRect(10, 220, 100, 30))
        self.ldtsave = QtWidgets.QLineEdit(ExportSurvey)
        self.ldtsave.setObjectName("ldtsave")
        self.ldtsave.setGeometry(QtCore.QRect(120, 220, 240, 30))
        self.btnsave = QtWidgets.QPushButton(ExportSurvey)
        self.btnsave.setObjectName("btnsave")
        self.btnsave.setGeometry(QtCore.QRect(380, 220, 80, 30))
        self.btnexport = QtWidgets.QPushButton(ExportSurvey)
        self.btnexport.setObjectName("btnexport")
        self.btnexport.setGeometry(QtCore.QRect(170, 270, 160, 30))
        self.btnexport.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ExportSurvey)
        self.msgbox.setObjectName("msgbox")
        _center_x = ExportSurvey.geometry().center().x()
        _center_y = ExportSurvey.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ExportSurvey)
        QtCore.QMetaObject.connectSlotsByName(ExportSurvey)


    def retranslateGUI(self, ExportSurvey):
        self.dialog = ExportSurvey
        #
        _translate = QtCore.QCoreApplication.translate
        ExportSurvey.setWindowTitle(_translate("ExportSurvey", "Export Survey"))
        self.lblsrvinfo.setText(_translate("ExportSurvey", "Survey information:"))
        self.lblstart.setText(_translate("ExportSurvey", "Start"))
        self.lblstart.setAlignment(QtCore.Qt.AlignCenter)
        self.lblend.setText(_translate("ExportSurvey", "End"))
        self.lblend.setAlignment(QtCore.Qt.AlignCenter)
        self.lblstep.setText(_translate("ExportSurvey", "Step"))
        self.lblstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnum.setText(_translate("ExportSurvey", "Number"))
        self.lblnum.setAlignment(QtCore.Qt.AlignCenter)
        self.lblinl.setText(_translate("ExportSurvey", "Inline:"))
        self.lblinl.setAlignment(QtCore.Qt.AlignRight)
        self.lblxl.setText(_translate("ExportSurvey", "Crossline:"))
        self.lblxl.setAlignment(QtCore.Qt.AlignRight)
        self.lblz.setText(_translate("ExportSurvey", "Time/depth:"))
        self.lblz.setAlignment(QtCore.Qt.AlignRight)
        self.ldtinlstart.setEnabled(False)
        self.ldtinlstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtinlend.setEnabled(False)
        self.ldtinlend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtinlstep.setEnabled(False)
        self.ldtinlstep.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtinlnum.setEnabled(False)
        self.ldtinlnum.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlstart.setEnabled(False)
        self.ldtxlstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlend.setEnabled(False)
        self.ldtxlend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlstep.setEnabled(False)
        self.ldtxlstep.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlnum.setEnabled(False)
        self.ldtxlnum.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtzstart.setEnabled(False)
        self.ldtzstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtzend.setEnabled(False)
        self.ldtzend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtzstep.setEnabled(False)
        self.ldtzstep.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtznum.setEnabled(False)
        self.ldtznum.setAlignment(QtCore.Qt.AlignCenter)
        #
        self.lblsave.setText(_translate("ExportSurvey", "Save as:"))
        self.ldtsave.setText(_translate("ExportSurvey", ""))
        self.btnsave.setText(_translate("ExportSurvey", "Browse"))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnexport.setText(_translate("ExportSeisNpy", "Export Survey"))
        self.btnexport.clicked.connect(self.clickBtnExportSurvey)
        #
        self.refreshSeisInfo()


    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Select Survey Numpy', self.rootpath,
                                        filter="Survey Numpy files (*.srv.npy);; All files (*.*)")
        if len(_file[0]) > 0:
            self.ldtsave.setText(_file[0])


    def clickBtnExportSurvey(self):
        self.refreshMsgBox()
        #
        if self.checkSurvInfo() is False:
            print("ExportSurvey: No survey found")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Export Survey',
                                           'No survey found')
            return
        #
        if len(self.ldtsave.text()) < 1:
            print("ExportSurvey: No name specified for survey")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Export Survey',
                                           'No name specified for survey')
            return
        #
        print("ExportSurvey: Export survey as %s" % self.ldtsave.text())
        #
        np.save(self.ldtsave.text(), self.survinfo)
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Export Survey",
                                          "Survey exported successfully")
        return


    def refreshSeisInfo(self):
        if self.checkSurvInfo():
            _seisinfo = self.survinfo
            self.ldtinlstart.setText(str(_seisinfo['ILStart']))
            self.ldtinlend.setText(str(_seisinfo['ILEnd']))
            self.ldtinlstep.setText(str(_seisinfo['ILStep']))
            self.ldtinlnum.setText(str(_seisinfo['ILNum']))
            self.ldtxlstart.setText(str(_seisinfo['XLStart']))
            self.ldtxlend.setText(str(_seisinfo['XLEnd']))
            self.ldtxlstep.setText(str(_seisinfo['XLStep']))
            self.ldtxlnum.setText(str(_seisinfo['XLNum']))
            self.ldtzstart.setText(str(_seisinfo['ZStart']))
            self.ldtzend.setText(str(_seisinfo['ZEnd']))
            self.ldtzstep.setText(str(_seisinfo['ZStep']))
            self.ldtznum.setText(str(_seisinfo['ZNum']))


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkSurvInfo(self):
        self.refreshMsgBox()
        #
        return seis_ays.checkSeisInfo(self.survinfo)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ExportSurvey = QtWidgets.QWidget()
    gui = exportsurvey()
    gui.setupGUI(ExportSurvey)
    ExportSurvey.show()
    sys.exit(app.exec_())