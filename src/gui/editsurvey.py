#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for editting seismic survey


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4])
from basic.data import data as basic_data
from seismic.analysis import analysis as seis_ays

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class editsurvey(object):

    survinfo = {}
    #
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, EditSurvey):
        EditSurvey.setObjectName("EditSurvey")
        EditSurvey.setFixedSize(400, 270)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/survey.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        EditSurvey.setWindowIcon(icon)
        self.lblsrvinfo = QtWidgets.QLabel(EditSurvey)
        self.lblsrvinfo.setObjectName("lblsrvinfo")
        self.lblsrvinfo.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lblnum = QtWidgets.QLabel(EditSurvey)
        self.lblnum.setObjectName("lblnum")
        self.lblnum.setGeometry(QtCore.QRect(120, 50, 80, 30))
        self.lblstart = QtWidgets.QLabel(EditSurvey)
        self.lblstart.setObjectName("lblstart")
        self.lblstart.setGeometry(QtCore.QRect(220, 50, 80, 30))
        self.lblstep = QtWidgets.QLabel(EditSurvey)
        self.lblstep.setObjectName("lblstep")
        self.lblstep.setGeometry(QtCore.QRect(320, 50, 40, 30))
        self.lblinl = QtWidgets.QLabel(EditSurvey)
        self.lblinl.setObjectName("lblinl")
        self.lblinl.setGeometry(QtCore.QRect(10, 90, 100, 30))
        self.lblxl = QtWidgets.QLabel(EditSurvey)
        self.lblxl.setObjectName("lblxl")
        self.lblxl.setGeometry(QtCore.QRect(10, 130, 100, 30))
        self.lblz = QtWidgets.QLabel(EditSurvey)
        self.lblz.setObjectName("lblz")
        self.lblz.setGeometry(QtCore.QRect(10, 170, 100, 30))
        self.ldtinlnum = QtWidgets.QLineEdit(EditSurvey)
        self.ldtinlnum.setObjectName("ldtinlnum")
        self.ldtinlnum.setGeometry(QtCore.QRect(120, 90, 80, 30))
        self.ldtinlstart = QtWidgets.QLineEdit(EditSurvey)
        self.ldtinlstart.setObjectName("ldtinlstart")
        self.ldtinlstart.setGeometry(QtCore.QRect(220, 90, 80, 30))
        self.ldtinlstep = QtWidgets.QLineEdit(EditSurvey)
        self.ldtinlstep.setObjectName("ldtinlstep")
        self.ldtinlstep.setGeometry(QtCore.QRect(320, 90, 40, 30))
        self.ldtxlnum = QtWidgets.QLineEdit(EditSurvey)
        self.ldtxlnum.setObjectName("ldtxlnum")
        self.ldtxlnum.setGeometry(QtCore.QRect(120, 130, 80, 30))
        self.ldtxlstart = QtWidgets.QLineEdit(EditSurvey)
        self.ldtxlstart.setObjectName("ldtxlstart")
        self.ldtxlstart.setGeometry(QtCore.QRect(220, 130, 80, 30))
        self.ldtxlstep = QtWidgets.QLineEdit(EditSurvey)
        self.ldtxlstep.setObjectName("ldtxlstep")
        self.ldtxlstep.setGeometry(QtCore.QRect(320, 130, 40, 30))
        self.ldtznum = QtWidgets.QLineEdit(EditSurvey)
        self.ldtznum.setObjectName("ldtznum")
        self.ldtznum.setGeometry(QtCore.QRect(120, 170, 80, 30))
        self.ldtzstart = QtWidgets.QLineEdit(EditSurvey)
        self.ldtzstart.setObjectName("ldtzstart")
        self.ldtzstart.setGeometry(QtCore.QRect(220, 170, 80, 30))
        self.ldtzstep = QtWidgets.QLineEdit(EditSurvey)
        self.ldtzstep.setObjectName("ldtzlstep")
        self.ldtzstep.setGeometry(QtCore.QRect(320, 170, 40, 30))
        self.btnapply = QtWidgets.QPushButton(EditSurvey)
        self.btnapply.setObjectName("btnapply")
        self.btnapply.setGeometry(QtCore.QRect(120, 220, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(EditSurvey)
        self.msgbox.setObjectName("msgbox")
        _center_x = EditSurvey.geometry().center().x()
        _center_y = EditSurvey.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(EditSurvey)
        QtCore.QMetaObject.connectSlotsByName(EditSurvey)


    def retranslateGUI(self, EditSurvey):
        self.dialog = EditSurvey
        #
        _translate = QtCore.QCoreApplication.translate
        EditSurvey.setWindowTitle(_translate("EditSurvey", "Edit Survey"))
        self.lblsrvinfo.setText(_translate("EditSurvey", "Survey information:"))
        self.lblnum.setText(_translate("EditSurvey", "Number"))
        self.lblnum.setAlignment(QtCore.Qt.AlignCenter)
        self.lblstart.setText(_translate("EditSurvey", "Start"))
        self.lblstart.setAlignment(QtCore.Qt.AlignCenter)
        self.lblstep.setText(_translate("EditSurvey", "Step"))
        self.lblstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblinl.setText(_translate("EditSurvey", "Inline:"))
        self.lblinl.setAlignment(QtCore.Qt.AlignRight)
        self.lblxl.setText(_translate("EditSurvey", "Crossline:"))
        self.lblxl.setAlignment(QtCore.Qt.AlignRight)
        self.lblz.setText(_translate("EditSurvey", "Time/depth:"))
        self.lblz.setAlignment(QtCore.Qt.AlignRight)
        self.ldtinlnum.setEnabled(False)
        self.ldtinlnum.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtinlstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtinlstep.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlnum.setEnabled(False)
        self.ldtxlnum.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlstep.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtznum.setEnabled(False)
        self.ldtznum.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtzstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtzstep.setAlignment(QtCore.Qt.AlignCenter)
        self.btnapply.setText(_translate("EditSurvey", "Apply"))
        self.btnapply.clicked.connect(self.clickBtnApply)
        #
        if self.checkSurvInfo() is True:
            _seisinfo = self.survinfo
            self.ldtinlnum.setText(_translate("EditSurvey", str(_seisinfo['ILNum'])))
            self.ldtinlstart.setText(_translate("EditSurvey", str(_seisinfo['ILStart'])))
            self.ldtinlstep.setText(_translate("EditSurvey", str(_seisinfo['ILStep'])))
            self.ldtxlnum.setText(_translate("EditSurvey", str(_seisinfo['XLNum'])))
            self.ldtxlstart.setText(_translate("EditSurvey", str(_seisinfo['XLStart'])))
            self.ldtxlstep.setText(_translate("EditSurvey", str(_seisinfo['XLStep'])))
            self.ldtznum.setText(_translate("EditSurvey", str(_seisinfo['ZNum'])))
            self.ldtzstart.setText(_translate("EditSurvey", str(_seisinfo['ZStart'])))
            self.ldtzstep.setText(_translate("EditSurvey", str(_seisinfo['ZStep'])))


    def clickBtnApply(self):
        self.refreshMsgBox()
        #
        if self.checkSurvInfo() is False:
            print("EditSurvey: No seismic survey found")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Edit Survey',
                                           'No seismic survey found')
            return
        #
        _inlnum = basic_data.str2int(self.ldtinlnum.text())
        _xlnum = basic_data.str2int(self.ldtxlnum.text())
        _znum = basic_data.str2int(self.ldtznum.text())
        _inlstart = basic_data.str2int(self.ldtinlstart.text())
        _inlstep = basic_data.str2int(self.ldtinlstep.text())
        _xlstart = basic_data.str2int(self.ldtxlstart.text())
        _xlstep = basic_data.str2int(self.ldtxlstep.text())
        _zstart = basic_data.str2int(self.ldtzstart.text())
        _zstep = basic_data.str2int(self.ldtzstep.text())
        if _inlstart is False or _inlstep is False or _inlnum is False\
            or _xlstart is False or _xlstep is False or _xlnum is False\
            or _zstart is False or _zstep is False or _znum is False:
            print("EditSurvey: Non-integer survey selection")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Edit Survey',
                                           'Non-integer survey selection')
            return
        #
        _zerodata = np.zeros([_znum, _xlnum, _inlnum])
        self.survinfo = seis_ays.createSeisInfoFrom3DMat(_zerodata,
                                                         inlstart=_inlstart, inlstep=_inlstep,
                                                         xlstart=_xlstart, xlstep=_xlstep,
                                                         zstart=_zstart, zstep=_zstep
                                                         )
        #
        # QtWidgets.QMessageBox.information(self.msgbox,
        #                                   "Edit Survey",
        #                                   "Survey edited successfully")
        #
        self.dialog.close()


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkSurvInfo(self):
        self.refreshMsgBox()
        #
        if seis_ays.checkSeisInfo(self.survinfo) is False:
            # print("EditSurvey: Survey not found")
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Edit Survey',
            #                                'Survey not found')
            return False
        return True


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    EditSurvey = QtWidgets.QWidget()
    gui = editsurvey()
    gui.setupGUI(EditSurvey)
    EditSurvey.show()
    sys.exit(app.exec_())