#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# Create a window for managing pre-stack seismic


from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from core.settings import settings as core_set
from psseismic.analysis import analysis as psseis_ays
from gui.editpsseis import editpsseis as gui_editpsseis

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class managepsseis(object):

    psseisdata = {}
    plotstyle = core_set.Visual['Image']
    fontstyle = core_set.Visual['Font']
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ManagePsSeis):
        ManagePsSeis.setObjectName("ManagePsSeis")
        ManagePsSeis.setFixedSize(320, 420)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/psseismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ManagePsSeis.setWindowIcon(icon)
        #
        self.lblpsseis = QtWidgets.QLabel(ManagePsSeis)
        self.lblpsseis.setObjectName("lblpsseis")
        self.lblpsseis.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.twgpsseis = QtWidgets.QTableWidget(ManagePsSeis)
        self.twgpsseis.setObjectName("twgpsseis")
        self.twgpsseis.setGeometry(QtCore.QRect(10, 50, 300, 300))
        self.twgpsseis.setColumnCount(2)
        self.twgpsseis.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgpsseis.verticalHeader().hide()
        self.btnedit = QtWidgets.QPushButton(ManagePsSeis)
        self.btnedit.setObjectName("btnedit")
        self.btnedit.setGeometry(QtCore.QRect(210, 360, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/pen.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnedit.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ManagePsSeis)
        self.msgbox.setObjectName("msgbox")
        _center_x = ManagePsSeis.geometry().center().x()
        _center_y = ManagePsSeis.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ManagePsSeis)
        QtCore.QMetaObject.connectSlotsByName(ManagePsSeis)


    def retranslateGUI(self, ManagePsSeis):
        self.dialog = ManagePsSeis
        #
        _translate = QtCore.QCoreApplication.translate
        ManagePsSeis.setWindowTitle(_translate("ManagePsSeis", "Manage Pre-stack Seismic"))
        self.lblpsseis.setText(_translate("ManagePsSeis", "Available pre-stack seismic:"))
        self.btnedit.setText(_translate("ManagePsSeis", "Edit"))
        self.btnedit.setToolTip("Edit pre-stack seismic")
        self.btnedit.clicked.connect(self.clickBtnEdit)
        #
        self.refreshTwgPsSeis()

    def clickBtnEdit(self):
        _edit = QtWidgets.QDialog()
        _gui = gui_editpsseis()
        _gui.psseisdata = self.psseisdata
        _gui.plotstyle = self.plotstyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_edit)
        _edit.exec()
        self.psseisdata = _gui.psseisdata
        _edit.show()
        #
        self.refreshTwgPsSeis()


    def refreshTwgPsSeis(self):
        self.twgpsseis.clear()
        self.twgpsseis.setHorizontalHeaderLabels(["Name", "No. of shots"])
        if len(self.psseisdata.keys()) > 0:
            _idx = 0
            self.twgpsseis.setRowCount(len(self.psseisdata.keys()))
            for i in sorted(self.psseisdata.keys()):
                if self.checkPsSeis(i):
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(i)
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.twgpsseis.setItem(_idx, 0, item)
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(str(len(list(self.psseisdata[i].keys()))))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEditable)
                    self.twgpsseis.setItem(_idx, 1, item)
                    _idx = _idx + 1
            self.twgpsseis.setRowCount(_idx)


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkPsSeis(self, name):
        return psseis_ays.checkPsSeis(self.psseisdata[name])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ManagePsSeis = QtWidgets.QWidget()
    gui = managepsseis()
    gui.setupGUI(ManagePsSeis)
    ManagePsSeis.show()
    sys.exit(app.exec_())
