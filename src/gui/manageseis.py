#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     March 2018                                                                      #
#                                                                                           #
#############################################################################################

# Create a window for managing seismic properties


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from seismic.analysis import analysis as seis_ays
from gui.editseispointset import editseispointset as gui_editseispointset

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class manageseis(object):

    survinfo = {}
    seisdata = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ManageSeis):
        ManageSeis.setObjectName("ManageSeis")
        ManageSeis.setFixedSize(320, 420)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ManageSeis.setWindowIcon(icon)
        #
        self.lblseis = QtWidgets.QLabel(ManageSeis)
        self.lblseis.setObjectName("lblattrib")
        self.lblseis.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.twgseis = QtWidgets.QTableWidget(ManageSeis)
        self.twgseis.setObjectName("twgseis")
        self.twgseis.setGeometry(QtCore.QRect(10, 50, 300, 300))
        self.twgseis.setColumnCount(6)
        self.twgseis.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgseis.verticalHeader().hide()
        self.btnedit = QtWidgets.QPushButton(ManageSeis)
        self.btnedit.setObjectName("btnedit")
        self.btnedit.setGeometry(QtCore.QRect(210, 360, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/pen.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnedit.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ManageSeis)
        self.msgbox.setObjectName("msgbox")
        _center_x = ManageSeis.geometry().center().x()
        _center_y = ManageSeis.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ManageSeis)
        QtCore.QMetaObject.connectSlotsByName(ManageSeis)


    def retranslateGUI(self, ManageSeis):
        self.dialog = ManageSeis
        #
        _translate = QtCore.QCoreApplication.translate
        ManageSeis.setWindowTitle(_translate("ManageSeis", "Manage Seismic"))
        self.lblseis.setText(_translate("ManageSeis", "Seismic properties:"))
        self.refreshTwgSeis()
        self.btnedit.setText(_translate("ManageSeis", "Edit"))
        self.btnedit.setToolTip("Edit seismic properties")
        self.btnedit.clicked.connect(self.clickBtnEdit)


    def clickBtnEdit(self):
        _editseis = QtWidgets.QDialog()
        _gui = gui_editseispointset()
        _gui.seispointdata = self.seisdata
        # add info
        if self.checkSurvInfo() and self.checkSeisData():
            _survinfo = seis_ays.convertSeisInfoTo2DMat(self.survinfo)
            _gui.seispointdata['Inline'] = _survinfo[:, 0:1]
            _gui.seispointdata['Crossline'] = _survinfo[:, 1:2]
            _gui.seispointdata['Z'] = _survinfo[:, 2:3]
        _gui.rootpath = self.rootpath
        _gui.setupGUI(_editseis)
        _editseis.exec()
        self.seisdata = _gui.seispointdata
        # remove info
        if 'Inline' in self.seisdata.keys():
            self.seisdata.pop('Inline')
        if 'Crossline' in self.seisdata.keys():
            self.seisdata.pop('Crossline')
        if 'Z' in self.seisdata.keys():
            self.seisdata.pop('Z')
        _editseis.show()
        #
        self.refreshTwgSeis()


    def refreshTwgSeis(self):
        self.twgseis.clear()
        self.twgseis.setHorizontalHeaderLabels(["Property", "Dimensions", "Maximum", "Minimum", "Mean", "Std"])
        if (self.checkSurvInfo() is True) and (self.checkSeisData() is True):
            _idx = 0
            self.twgseis.setRowCount(len(self.seisdata.keys()))
            for i in sorted(self.seisdata.keys()):
                if i != "Inline" and i != "Crossline" and i != "Z":
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(i)
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.twgseis.setItem(_idx, 0, item)
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(str(np.shape(self.seisdata[i])[1:]))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEditable)
                    self.twgseis.setItem(_idx, 1, item)
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(str(np.max(self.seisdata[i])))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEditable)
                    self.twgseis.setItem(_idx, 2, item)
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(str(np.min(self.seisdata[i])))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEditable)
                    self.twgseis.setItem(_idx, 3, item)
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(str(np.mean(self.seisdata[i])))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEditable)
                    self.twgseis.setItem(_idx, 4, item)
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(str(np.std(self.seisdata[i])))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEditable)
                    self.twgseis.setItem(_idx, 5, item)
                    _idx = _idx + 1
            if "Inline" in self.seisdata.keys():
                item = QtWidgets.QTableWidgetItem()
                item.setText("Inline")
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgseis.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(np.shape(self.seisdata['Inline'])[1:]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgseis.setItem(_idx, 1, item)
                _idx = _idx + 1
            if "Crossline" in self.seisdata.keys():
                item = QtWidgets.QTableWidgetItem()
                item.setText("Crossline")
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgseis.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(np.shape(self.seisdata['Crossline'])[1:]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgseis.setItem(_idx, 1, item)
                _idx = _idx + 1
            if "Z" in self.seisdata.keys():
                item = QtWidgets.QTableWidgetItem()
                item.setText("Z")
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgseis.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(np.shape(self.seisdata['Z'])[1:]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgseis.setItem(_idx, 1, item)
                _idx = _idx + 1


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkSurvInfo(self):
        self.refreshMsgBox()
        #
        if seis_ays.checkSeisInfo(self.survinfo) is False:
            # print("ManageSeis: Survey not found")
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Manage Seismic',
            #                                'Survey not found')
            return False
        return True


    def checkSeisData(self):
        self.refreshMsgBox()
        #
        for f in self.seisdata.keys():
            if np.shape(self.seisdata[f])[0] != self.survinfo['SampleNum']:
                # print("ManageSeis: Seismic & survey not match")
                # QtWidgets.QMessageBox.critical(self.msgbox,
                #                                'Manage Seismic',
                #                                'Seismic & survey not match')
                return False
        return True



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ManageSeis = QtWidgets.QWidget()
    gui = manageseis()
    gui.setupGUI(ManageSeis)
    ManageSeis.show()
    sys.exit(app.exec_())