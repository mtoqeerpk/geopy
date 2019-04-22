#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for importing seismic survey


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4])
from basic.data import data as basic_data
from seismic.analysis import analysis as seis_ays

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class importsurveymanual(object):

    survinfo = {}
    #
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, ImportSurveyManual):
        ImportSurveyManual.setObjectName("ImportSurveyManual")
        ImportSurveyManual.setFixedSize(400, 270)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/survey.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ImportSurveyManual.setWindowIcon(icon)
        self.lblsrvinfo = QtWidgets.QLabel(ImportSurveyManual)
        self.lblsrvinfo.setObjectName("lblsrvinfo")
        self.lblsrvinfo.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lblstart = QtWidgets.QLabel(ImportSurveyManual)
        self.lblstart.setObjectName("lblstart")
        self.lblstart.setGeometry(QtCore.QRect(120, 50, 80, 30))
        self.lblstep = QtWidgets.QLabel(ImportSurveyManual)
        self.lblstep.setObjectName("lblstep")
        self.lblstep.setGeometry(QtCore.QRect(220, 50, 40, 30))
        self.lblnum = QtWidgets.QLabel(ImportSurveyManual)
        self.lblnum.setObjectName("lblnum")
        self.lblnum.setGeometry(QtCore.QRect(280, 50, 80, 30))
        self.lblinl = QtWidgets.QLabel(ImportSurveyManual)
        self.lblinl.setObjectName("lblinl")
        self.lblinl.setGeometry(QtCore.QRect(10, 90, 100, 30))
        self.lblxl = QtWidgets.QLabel(ImportSurveyManual)
        self.lblxl.setObjectName("lblxl")
        self.lblxl.setGeometry(QtCore.QRect(10, 130, 100, 30))
        self.lblz = QtWidgets.QLabel(ImportSurveyManual)
        self.lblz.setObjectName("lblz")
        self.lblz.setGeometry(QtCore.QRect(10, 170, 100, 30))
        self.ldtinlstart = QtWidgets.QLineEdit(ImportSurveyManual)
        self.ldtinlstart.setObjectName("ldtinlstart")
        self.ldtinlstart.setGeometry(QtCore.QRect(120, 90, 80, 30))
        self.ldtinlstep = QtWidgets.QLineEdit(ImportSurveyManual)
        self.ldtinlstep.setObjectName("ldtinlstep")
        self.ldtinlstep.setGeometry(QtCore.QRect(220, 90, 40, 30))
        self.ldtinlnum = QtWidgets.QLineEdit(ImportSurveyManual)
        self.ldtinlnum.setObjectName("ldtinlnum")
        self.ldtinlnum.setGeometry(QtCore.QRect(280, 90, 80, 30))
        self.ldtxlstart = QtWidgets.QLineEdit(ImportSurveyManual)
        self.ldtxlstart.setObjectName("ldtxlstart")
        self.ldtxlstart.setGeometry(QtCore.QRect(120, 130, 80, 30))
        self.ldtxlstep = QtWidgets.QLineEdit(ImportSurveyManual)
        self.ldtxlstep.setObjectName("ldtxlstep")
        self.ldtxlstep.setGeometry(QtCore.QRect(220, 130, 40, 30))
        self.ldtxlnum = QtWidgets.QLineEdit(ImportSurveyManual)
        self.ldtxlnum.setObjectName("ldtxlnum")
        self.ldtxlnum.setGeometry(QtCore.QRect(280, 130, 80, 30))
        self.ldtzstart = QtWidgets.QLineEdit(ImportSurveyManual)
        self.ldtzstart.setObjectName("ldtzstart")
        self.ldtzstart.setGeometry(QtCore.QRect(120, 170, 80, 30))
        self.ldtzstep = QtWidgets.QLineEdit(ImportSurveyManual)
        self.ldtzstep.setObjectName("ldtzlstep")
        self.ldtzstep.setGeometry(QtCore.QRect(220, 170, 40, 30))
        self.ldtznum = QtWidgets.QLineEdit(ImportSurveyManual)
        self.ldtznum.setObjectName("ldtznum")
        self.ldtznum.setGeometry(QtCore.QRect(280, 170, 80, 30))
        self.btnimport = QtWidgets.QPushButton(ImportSurveyManual)
        self.btnimport.setObjectName("btnimport")
        self.btnimport.setGeometry(QtCore.QRect(120, 220, 160, 30))
        self.btnimport.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ImportSurveyManual)
        self.msgbox.setObjectName("msgbox")
        _center_x = ImportSurveyManual.geometry().center().x()
        _center_y = ImportSurveyManual.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ImportSurveyManual)
        QtCore.QMetaObject.connectSlotsByName(ImportSurveyManual)


    def retranslateGUI(self, ImportSurveyManual):
        self.dialog = ImportSurveyManual
        #
        _translate = QtCore.QCoreApplication.translate
        ImportSurveyManual.setWindowTitle(_translate("ImportSurveyManual", "Create Survey"))
        self.lblsrvinfo.setText(_translate("ImportSurveyManual", "Survey information:"))
        self.lblstart.setText(_translate("ImportSurveyManual", "Start"))
        self.lblstart.setAlignment(QtCore.Qt.AlignCenter)
        self.lblstep.setText(_translate("ImportSurveyManual", "Step"))
        self.lblstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnum.setText(_translate("ImportSurveyManual", "Number"))
        self.lblnum.setAlignment(QtCore.Qt.AlignCenter)
        self.lblinl.setText(_translate("ImportSurveyManual", "Inline:"))
        self.lblinl.setAlignment(QtCore.Qt.AlignRight)
        self.lblxl.setText(_translate("ImportSurveyManual", "Crossline:"))
        self.lblxl.setAlignment(QtCore.Qt.AlignRight)
        self.lblz.setText(_translate("ImportSurveyManual", "Time/depth:"))
        self.lblz.setAlignment(QtCore.Qt.AlignRight)
        self.ldtinlstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtinlstep.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtinlnum.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlstep.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlnum.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtzstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtzstep.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtznum.setAlignment(QtCore.Qt.AlignCenter)
        #
        self.btnimport.setText(_translate("ImportSurveyManual", "Create"))
        self.btnimport.clicked.connect(self.clickBtnImportSurveyManual)
        #


    def clickBtnImportSurveyManual(self):
        self.refreshMsgBox()
        #
        _inlstart = basic_data.str2int(self.ldtinlstart.text())
        _xlstart = basic_data.str2int(self.ldtxlstart.text())
        _zstart = basic_data.str2int(self.ldtzstart.text())
        _inlstep = basic_data.str2int(self.ldtinlstep.text())
        _xlstep = basic_data.str2int(self.ldtxlstep.text())
        _zstep = basic_data.str2int(self.ldtzstep.text())
        _inlnum = basic_data.str2int(self.ldtinlnum.text())
        _xlnum = basic_data.str2int(self.ldtxlnum.text())
        _znum = basic_data.str2int(self.ldtznum.text())
        if _inlstart is False or _xlstart is False or _zstart is False \
            or _inlstep is False or _xlstep is False or _zstep is False \
            or _inlnum is False or _xlnum is False or _znum is False:
            print("ImportSurveyManual: Non-integer survey information")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Create Survey',
                                           'Non-integer survey information')
            return
        if _inlnum <= 0 or _xlnum <= 0 or _znum <= 0:
            print("ImportSurveyManual: Zero survey dimension")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Create Survey',
                                           'Zero survey dimension')
            return
        if _inlstep <= 0 or _xlstep <= 0 or _zstep == 0:
            print("ImportSurveyManual: Zero survey step")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Create Survey',
                                           'Zero survey step')
            return
        #
        self.survinfo = seis_ays.createSeisInfoFrom3DMat(seis3dmat=np.zeros([_znum, _xlnum, _inlnum]),
                                                         inlstart=_inlstart,
                                                         inlstep=_inlstep,
                                                         xlstart=_xlstart,
                                                         xlstep=_xlstep,
                                                         zstart=_zstart,
                                                         zstep=_zstep)
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Create Survey",
                                          "Survey created successfully")
        return


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
    ImportSurveyManual = QtWidgets.QWidget()
    gui = importsurveymanual()
    gui.setupGUI(ImportSurveyManual)
    ImportSurveyManual.show()
    sys.exit(app.exec_())