#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     March 2018                                                                      #
#                                                                                           #
#############################################################################################

# Create a GUI for settings (GUI)

from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from core.settings import settings as core_set

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class settingsgui(object):

    mainwindow = None
    settings = core_set.GUI
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, SettingsGUI):
        SettingsGUI.setObjectName("SettingsGUI")
        SettingsGUI.setFixedSize(400, 130)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/logo.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        SettingsGUI.setWindowIcon(icon)
        #
        self.lbltoolbar = QtWidgets.QLabel(SettingsGUI)
        self.lbltoolbar.setObjectName("lbltoolbar")
        self.lbltoolbar.setGeometry(QtCore.QRect(10, 10, 50, 30))
        self.cbxtoolbarleft = QtWidgets.QCheckBox(SettingsGUI)
        self.cbxtoolbarleft.setObjectName("cbxtoolbarleft")
        self.cbxtoolbarleft.setGeometry(QtCore.QRect(30, 40, 170, 30))
        self.cbxtoolbarright = QtWidgets.QCheckBox(SettingsGUI)
        self.cbxtoolbarright.setObjectName("cbxtoolbarright")
        self.cbxtoolbarright.setGeometry(QtCore.QRect(230, 40, 170, 30))
        self.cbxtoolbartop = QtWidgets.QCheckBox(SettingsGUI)
        self.cbxtoolbartop.setObjectName("cbxtoolbartop")
        self.cbxtoolbartop.setGeometry(QtCore.QRect(30, 80, 170, 30))
        self.cbxtoolbarbottom = QtWidgets.QCheckBox(SettingsGUI)
        self.cbxtoolbarbottom.setObjectName("cbxtoolbartop")
        self.cbxtoolbarbottom.setGeometry(QtCore.QRect(230, 80, 170, 30))
        #
        self.msgbox = QtWidgets.QMessageBox(SettingsGUI)
        self.msgbox.setObjectName("msgbox")
        _center_x = SettingsGUI.geometry().center().x()
        _center_y = SettingsGUI.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(SettingsGUI)
        QtCore.QMetaObject.connectSlotsByName(SettingsGUI)


    def retranslateGUI(self, SettingsGUI):
        self.dialog = SettingsGUI
        #
        _translate = QtCore.QCoreApplication.translate
        SettingsGUI.setWindowTitle(_translate("SettingsGUI", "GeoPy Settings"))
        self.lbltoolbar.setText(_translate("SettingsGUI", "Toolbars:"))
        self.cbxtoolbarleft.setText(_translate("SettingsGUI", "Data import && export"))
        self.cbxtoolbarleft.stateChanged.connect(self.changeCbxToolbarLeft)
        self.cbxtoolbarright.setText(_translate("SettingsGUI", "Featured toolbox"))
        self.cbxtoolbarright.stateChanged.connect(self.changeCbxToolbarRight)
        self.cbxtoolbartop.setText(_translate("SettingsGUI", "Manage survey && data"))
        self.cbxtoolbartop.stateChanged.connect(self.changeCbxToolbarTop)
        self.cbxtoolbarbottom.setText(_translate("SettingsGUI", "Visualization"))
        self.cbxtoolbarbottom.stateChanged.connect(self.changeCbxToolbarBottom)
        if self.mainwindow is not None:
            self.cbxtoolbarleft.setChecked(self.settings['Toolbar']['Left'])
            self.cbxtoolbarright.setChecked(self.settings['Toolbar']['Right'])
            self.cbxtoolbartop.setChecked(self.settings['Toolbar']['Top'])
            self.cbxtoolbarbottom.setChecked(self.settings['Toolbar']['Bottom'])
            self.mainwindow.toolbarleft.setVisible(self.settings['Toolbar']['Left'])
            self.mainwindow.toolbarright.setVisible(self.settings['Toolbar']['Right'])
            self.mainwindow.toolbartop.setVisible(self.settings['Toolbar']['Top'])
            self.mainwindow.toolbarbottom.setVisible(self.settings['Toolbar']['Bottom'])


    def changeCbxToolbarLeft(self):
        self.refreshMsgBox()
        #
        if self.mainwindow is None:
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'GeoPy',
                                           'No GeoPy found')
            return
        if self.cbxtoolbarleft.isChecked():
            self.mainwindow.toolbarleft.setVisible(True)
        else:
            self.mainwindow.toolbarleft.setVisible(False)
        self.settings['Toolbar']['Left'] = self.cbxtoolbarleft.isChecked()


    def changeCbxToolbarRight(self):
        self.refreshMsgBox()
        #
        if self.mainwindow is None:
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'GeoPy',
                                           'No GeoPy found')
            return
        if self.cbxtoolbarright.isChecked():
            self.mainwindow.toolbarright.setVisible(True)
        else:
            self.mainwindow.toolbarright.setVisible(False)
        self.settings['Toolbar']['Right'] = self.cbxtoolbarright.isChecked()


    def changeCbxToolbarTop(self):
        self.refreshMsgBox()
        #
        if self.mainwindow is None:
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'GeoPy',
                                           'No GeoPy found')
            return
        if self.cbxtoolbartop.isChecked():
            self.mainwindow.toolbartop.setVisible(True)
        else:
            self.mainwindow.toolbartop.setVisible(False)
        self.settings['Toolbar']['Top'] = self.cbxtoolbartop.isChecked()


    def changeCbxToolbarBottom(self):
        self.refreshMsgBox()
        #
        if self.mainwindow is None:
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'GeoPy',
                                           'No GeoPy found')
            return
        if self.cbxtoolbarbottom.isChecked():
            self.mainwindow.toolbarbottom.setVisible(True)
        else:
            self.mainwindow.toolbarbottom.setVisible(False)
        self.settings['Toolbar']['Bottom'] = self.cbxtoolbarbottom.isChecked()


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SettingsGUI = QtWidgets.QWidget()
    gui = settingsgui()
    gui.setupGUI(SettingsGUI)
    SettingsGUI.show()
    sys.exit(app.exec_())