#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for managing seismic survey


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4])
from seismic.analysis import analysis as seis_ays
from gui.editsurvey import editsurvey as gui_editsurvey
from gui.cropsurvey import cropsurvey as gui_cropsurvey

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class managesurvey(object):

    survinfo = {}
    seisdata = {}
    #
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, ManageSurvey):
        ManageSurvey.setObjectName("ManageSurvey")
        ManageSurvey.setFixedSize(500, 330)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/survey.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ManageSurvey.setWindowIcon(icon)
        self.lblsrvinfo = QtWidgets.QLabel(ManageSurvey)
        self.lblsrvinfo.setObjectName("lblsrvinfo")
        self.lblsrvinfo.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lblstart = QtWidgets.QLabel(ManageSurvey)
        self.lblstart.setObjectName("lblstart")
        self.lblstart.setGeometry(QtCore.QRect(120, 50, 80, 30))
        self.lblend = QtWidgets.QLabel(ManageSurvey)
        self.lblend.setObjectName("lblend")
        self.lblend.setGeometry(QtCore.QRect(220, 50, 80, 30))
        self.lblstep = QtWidgets.QLabel(ManageSurvey)
        self.lblstep.setObjectName("lblstep")
        self.lblstep.setGeometry(QtCore.QRect(320, 50, 40, 30))
        self.lblnum = QtWidgets.QLabel(ManageSurvey)
        self.lblnum.setObjectName("lblnum")
        self.lblnum.setGeometry(QtCore.QRect(380, 50, 80, 30))
        self.lblinl = QtWidgets.QLabel(ManageSurvey)
        self.lblinl.setObjectName("lblinl")
        self.lblinl.setGeometry(QtCore.QRect(10, 90, 100, 30))
        self.lblxl = QtWidgets.QLabel(ManageSurvey)
        self.lblxl.setObjectName("lblxl")
        self.lblxl.setGeometry(QtCore.QRect(10, 130, 100, 30))
        self.lblz = QtWidgets.QLabel(ManageSurvey)
        self.lblz.setObjectName("lblz")
        self.lblz.setGeometry(QtCore.QRect(10, 170, 100, 30))
        self.ldtinlstart = QtWidgets.QLineEdit(ManageSurvey)
        self.ldtinlstart.setObjectName("ldtinlstart")
        self.ldtinlstart.setGeometry(QtCore.QRect(120, 90, 80, 30))
        self.ldtinlend = QtWidgets.QLineEdit(ManageSurvey)
        self.ldtinlend.setObjectName("ldtinlend")
        self.ldtinlend.setGeometry(QtCore.QRect(220, 90, 80, 30))
        self.ldtinlstep = QtWidgets.QLineEdit(ManageSurvey)
        self.ldtinlstep.setObjectName("ldtinlstep")
        self.ldtinlstep.setGeometry(QtCore.QRect(320, 90, 40, 30))
        self.ldtinlnum = QtWidgets.QLineEdit(ManageSurvey)
        self.ldtinlnum.setObjectName("ldtinlnum")
        self.ldtinlnum.setGeometry(QtCore.QRect(380, 90, 80, 30))
        self.ldtxlstart = QtWidgets.QLineEdit(ManageSurvey)
        self.ldtxlstart.setObjectName("ldtxlstart")
        self.ldtxlstart.setGeometry(QtCore.QRect(120, 130, 80, 30))
        self.ldtxlend = QtWidgets.QLineEdit(ManageSurvey)
        self.ldtxlend.setObjectName("ldtxlend")
        self.ldtxlend.setGeometry(QtCore.QRect(220, 130, 80, 30))
        self.ldtxlstep = QtWidgets.QLineEdit(ManageSurvey)
        self.ldtxlstep.setObjectName("ldtxlstep")
        self.ldtxlstep.setGeometry(QtCore.QRect(320, 130, 40, 30))
        self.ldtxlnum = QtWidgets.QLineEdit(ManageSurvey)
        self.ldtxlnum.setObjectName("ldtxlnum")
        self.ldtxlnum.setGeometry(QtCore.QRect(380, 130, 80, 30))
        self.ldtzstart = QtWidgets.QLineEdit(ManageSurvey)
        self.ldtzstart.setObjectName("ldtzstart")
        self.ldtzstart.setGeometry(QtCore.QRect(120, 170, 80, 30))
        self.ldtzend = QtWidgets.QLineEdit(ManageSurvey)
        self.ldtzend.setObjectName("ldtzend")
        self.ldtzend.setGeometry(QtCore.QRect(220, 170, 80, 30))
        self.ldtzstep = QtWidgets.QLineEdit(ManageSurvey)
        self.ldtzstep.setObjectName("ldtzlstep")
        self.ldtzstep.setGeometry(QtCore.QRect(320, 170, 40, 30))
        self.ldtznum = QtWidgets.QLineEdit(ManageSurvey)
        self.ldtznum.setObjectName("ldtznum")
        self.ldtznum.setGeometry(QtCore.QRect(380, 170, 80, 30))
        self.btnedit = QtWidgets.QPushButton(ManageSurvey)
        self.btnedit.setObjectName("btnedit")
        self.btnedit.setGeometry(QtCore.QRect(360, 220, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/pen.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnedit.setIcon(icon)
        self.btncrop = QtWidgets.QPushButton(ManageSurvey)
        self.btncrop.setObjectName("btncrop")
        self.btncrop.setGeometry(QtCore.QRect(360, 270, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/crop.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btncrop.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ManageSurvey)
        self.msgbox.setObjectName("msgbox")
        _center_x = ManageSurvey.geometry().center().x()
        _center_y = ManageSurvey.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ManageSurvey)
        QtCore.QMetaObject.connectSlotsByName(ManageSurvey)


    def retranslateGUI(self, ManageSurvey):
        self.dialog = ManageSurvey
        #
        _translate = QtCore.QCoreApplication.translate
        ManageSurvey.setWindowTitle(_translate("ManageSurvey", "Manage Survey"))
        self.lblsrvinfo.setText(_translate("ManageSurvey", "Survey information:"))
        self.lblstart.setText(_translate("ManageSurvey", "Start"))
        self.lblstart.setAlignment(QtCore.Qt.AlignCenter)
        self.lblend.setText(_translate("ManageSurvey", "End"))
        self.lblend.setAlignment(QtCore.Qt.AlignCenter)
        self.lblstep.setText(_translate("ManageSurvey", "Step"))
        self.lblstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnum.setText(_translate("ManageSurvey", "Number"))
        self.lblnum.setAlignment(QtCore.Qt.AlignCenter)
        self.lblinl.setText(_translate("ManageSurvey", "Inline:"))
        self.lblinl.setAlignment(QtCore.Qt.AlignRight)
        self.lblxl.setText(_translate("ManageSurvey", "Crossline:"))
        self.lblxl.setAlignment(QtCore.Qt.AlignRight)
        self.lblz.setText(_translate("ManageSurvey", "Time/depth:"))
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
        self.refreshSeisInfo()
        #
        self.btnedit.setText(_translate("ManageSurvey", "Edit"))
        self.btnedit.setToolTip("Edit survey range")
        self.btnedit.clicked.connect(self.clickBtnEdit)
        self.btncrop.setText(_translate("ManageSurvey", "Crop"))
        self.btncrop.setToolTip("Crop survey size")
        self.btncrop.clicked.connect(self.clickBtnCrop)


    def clickBtnEdit(self):
        _editsurvey = QtWidgets.QDialog()
        _gui = gui_editsurvey()
        _gui.survinfo = self.survinfo
        _gui.setupGUI(_editsurvey)
        _editsurvey.exec()
        self.survinfo = _gui.survinfo
        _editsurvey.show()
        #
        self.refreshSeisInfo()


    def clickBtnCrop(self):
        _cropsurvey = QtWidgets.QDialog()
        _gui = gui_cropsurvey()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.setupGUI(_cropsurvey)
        _cropsurvey.exec()
        self.seisdata = _gui.seisdata
        self.survinfo = _gui.survinfo
        _cropsurvey.show()
        #
        self.refreshSeisInfo()


    def refreshSeisInfo(self):
        if (self.checkSurvInfo() is True):
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
        if seis_ays.checkSeisInfo(self.survinfo) is False:
            # print("ManageSurvey: Survey not found")
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Manage Survey',
            #                                'Survey not found')
            return False
        return True


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ManageSurvey = QtWidgets.QWidget()
    gui = managesurvey()
    gui.setupGUI(ManageSurvey)
    ManageSurvey.show()
    sys.exit(app.exec_())