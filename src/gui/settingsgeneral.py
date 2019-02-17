#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     March 2018                                                                      #
#                                                                                           #
#############################################################################################

# Create a GUI for settings (general)

from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from core.settings import settings as core_set

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class settingsgeneral(object):

    settings = core_set.General
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, SettingsGeneral):
        SettingsGeneral.setObjectName("SettingsGeneral")
        SettingsGeneral.setFixedSize(400, 70)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/settings.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        SettingsGeneral.setWindowIcon(icon)
        #
        self.lblrootpath = QtWidgets.QLabel(SettingsGeneral)
        self.lblrootpath.setObjectName("lblrootpath")
        self.lblrootpath.setGeometry(QtCore.QRect(10, 20, 50, 30))
        self.ldtrootpath = QtWidgets.QLineEdit(SettingsGeneral)
        self.ldtrootpath.setObjectName("ldtrootpath")
        self.ldtrootpath.setGeometry(QtCore.QRect(70, 20, 270, 30))
        self.btnrootpath = QtWidgets.QPushButton(SettingsGeneral)
        self.btnrootpath.setObjectName("btnrootpath")
        self.btnrootpath.setGeometry(QtCore.QRect(350, 20, 40, 30))
        #
        self.msgbox = QtWidgets.QMessageBox(SettingsGeneral)
        self.msgbox.setObjectName("msgbox")
        _center_x = SettingsGeneral.geometry().center().x()
        _center_y = SettingsGeneral.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(SettingsGeneral)
        QtCore.QMetaObject.connectSlotsByName(SettingsGeneral)


    def retranslateGUI(self, SettingsGeneral):
        self.dialog = SettingsGeneral
        #
        _translate = QtCore.QCoreApplication.translate
        SettingsGeneral.setWindowTitle(_translate("SettingsGeneral", "General Settings"))
        self.lblrootpath.setText(_translate("SettingsGeneral", "Root path:"))
        self.ldtrootpath.setText(_translate("SettingsGeneral", self.settings['RootPath']))
        self.ldtrootpath.setEnabled(False)
        self.btnrootpath.setText(_translate("SettingsGeneral", "Reset"))
        self.btnrootpath.clicked.connect(self.clickBtnRootpath)


    def clickBtnRootpath(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getExistingDirectory(None, 'Select Root Path', self.settings['RootPath'],
                                             options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if len(_file) > 0:
            self.ldtrootpath.setText(_file)
            self.settings['RootPath'] = _file


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SettingsGeneral = QtWidgets.QWidget()
    gui = settingsgeneral()
    gui.setupGUI(SettingsGeneral)
    SettingsGeneral.show()
    sys.exit(app.exec_())