#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     January 2019                                                                    #
#                                                                                           #
#############################################################################################

# Create a window for editing pre-stack seismic


from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from core.settings import settings as core_set
from psseismic.analysis import analysis as psseis_ays
from gui.plot2dpsseisshot import plot2dpsseisshot as gui_plot2dpsseisshot
from gui.viewpsseis import viewpsseis as gui_viewpsseis

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class editpsseis(object):

    psseisdata = {}
    plotstyle = core_set.Visual['Image']
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, EditPsSeis):
        EditPsSeis.setObjectName("EditPsSeis")
        EditPsSeis.setFixedSize(300, 420)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/psseismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        EditPsSeis.setWindowIcon(icon)
        #
        self.lblpsseis = QtWidgets.QLabel(EditPsSeis)
        self.lblpsseis.setObjectName("lblpsseis")
        self.lblpsseis.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwgpsseis = QtWidgets.QListWidget(EditPsSeis)
        self.lwgpsseis.setObjectName("lwgpsseis")
        self.lwgpsseis.setGeometry(QtCore.QRect(10, 50, 280, 200))
        self.lwgpsseis.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lblaction = QtWidgets.QLabel(EditPsSeis)
        self.lblaction.setObjectName("lblaction")
        self.lblaction.setGeometry(QtCore.QRect(110, 270, 40, 30))
        self.cbbaction = QtWidgets.QComboBox(EditPsSeis)
        self.cbbaction.setObjectName("cbbaction")
        self.cbbaction.setGeometry(QtCore.QRect(160, 270, 130, 30))
        self.lblrename = QtWidgets.QLabel(EditPsSeis)
        self.lblrename.setObjectName("lblrename")
        self.lblrename.setGeometry(QtCore.QRect(160, 310, 40, 30))
        self.ldtrename = QtWidgets.QLineEdit(EditPsSeis)
        self.ldtrename.setObjectName("ldtrename")
        self.ldtrename.setGeometry(QtCore.QRect(200, 310, 90, 30))
        self.btnedit = QtWidgets.QPushButton(EditPsSeis)
        self.btnedit.setObjectName("btnedit")
        self.btnedit.setGeometry(QtCore.QRect(100, 370, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnedit.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(EditPsSeis)
        self.msgbox.setObjectName("msgbox")
        _center_x = EditPsSeis.geometry().center().x()
        _center_y = EditPsSeis.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(EditPsSeis)
        QtCore.QMetaObject.connectSlotsByName(EditPsSeis)


    def retranslateGUI(self, EditPsSeis):
        self.dialog = EditPsSeis
        #
        _translate = QtCore.QCoreApplication.translate
        EditPsSeis.setWindowTitle(_translate("EditPsSeis", "Edit Pre-stack Seismic"))
        self.lblpsseis.setText(_translate("EditPsSeis", "Available pre-stack seismic:"))
        self.lblaction.setText(_translate("EditPsSeis", "Action:"))
        self.cbbaction.addItems(['Copy', 'Delete', 'Rename', 'View', 'Gather-plot'])
        self.cbbaction.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, "icons/copy.png")))
        self.cbbaction.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, "icons/delete.png")))
        self.cbbaction.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, "icons/rename.png")))
        self.cbbaction.setItemIcon(3, QtGui.QIcon(os.path.join(self.iconpath, "icons/view.png")))
        self.cbbaction.setItemIcon(4, QtGui.QIcon(os.path.join(self.iconpath, "icons/gather.png")))
        self.cbbaction.currentIndexChanged.connect(self.changeCbbAction)
        self.lblrename.setText(_translate("EditPsSeis", ""))
        self.lblrename.setVisible(False)
        self.ldtrename.setText(_translate("EditPsSeis", ""))
        self.ldtrename.setVisible(False)
        self.btnedit.setText(_translate("EditPsSeis", "Apply"))
        self.btnedit.clicked.connect(self.clickBtnEditPsSeis)
        #
        self.refreshLwgPsSeis()


    def changeCbbAction(self):
        if self.cbbaction.currentIndex() == 2:
            self.lblrename.setText('Name:')
            self.lblrename.setVisible(True)
            self.ldtrename.setVisible(True)
        else:
            self.lblrename.setText('')
            self.lblrename.setVisible(False)
            self.ldtrename.setText('')
            self.ldtrename.setVisible(False)


    def clickBtnEditPsSeis(self):
        self.refreshMsgBox()
        #
        _psseislist = self.lwgpsseis.selectedItems()
        if len(_psseislist) < 1:
            print("EditPsSeis: No pre-stack seismic selected for editing")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Edit Pre-stack Seismic',
                                           'No pre-stack seismic selected for editing')
            return
        #
        if self.cbbaction.currentIndex() == 0:
            self.psseisdata[_psseislist[0].text()+'_copy'] = self.psseisdata[_psseislist[0].text()]
        if self.cbbaction.currentIndex() == 1:
            self.psseisdata.pop(_psseislist[0].text())
        if self.cbbaction.currentIndex() == 2:
            if len(self.ldtrename.text()) < 1:
                print("EditPsSeis: No name specified for rename")
                QtWidgets.QMessageBox.critical(self.msgbox,
                                               'Edit Pre-stack Seismic',
                                               'No name specified for rename')
                return
            if self.ldtrename.text() in self.psseisdata.keys():
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Edit Pre-stack Seismic',
                                                       self.ldtrename.text() + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)

                if reply == QtWidgets.QMessageBox.No:
                    return
            self.psseisdata[self.ldtrename.text()] = self.psseisdata[_psseislist[0].text()]
            self.psseisdata.pop(_psseislist[0].text())
        if self.cbbaction.currentIndex() == 3:
            _view = QtWidgets.QDialog()
            _gui = gui_viewpsseis()
            _gui.psseisname = _psseislist[0].text()
            _gui.psseisdata = self.psseisdata[_psseislist[0].text()]
            _gui.plotstyle = self.plotstyle
            _gui.setupGUI(_view)
            _view.exec()
            _view.show()
        if self.cbbaction.currentIndex() == 4:
            _plt = QtWidgets.QDialog()
            _gui = gui_plot2dpsseisshot()
            _gui.psseisdata = {}
            _gui.psseisdata[_psseislist[0].text()] = self.psseisdata[_psseislist[0].text()]
            _gui.plotstyle = self.plotstyle
            _gui.setupGUI(_plt)
            _plt.exec()
            _plt.show()
        #
        self.refreshLwgPsSeis()
        # if self.cbbaction.currentIndex() != 3:
            # QtWidgets.QMessageBox.information(self.msgbox,
            #                                   "Edit PointSet",
            #                                   "PointSet edited successfully")
        return


    def refreshLwgPsSeis(self):
        self.lwgpsseis.clear()
        if len(self.psseisdata.keys()) > 0:
            for i in sorted(self.psseisdata.keys()):
                if self.checkPsSeis(i):
                    item = QtWidgets.QListWidgetItem(self.lwgpsseis)
                    item.setText(i)
                    self.lwgpsseis.addItem(item)


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkPsSeis(self, name):
        return psseis_ays.checkPsSeis(self.psseisdata[name])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EditPsSeis = QtWidgets.QWidget()
    gui = editpsseis()
    gui.setupGUI(EditPsSeis)
    EditPsSeis.show()
    sys.exit(app.exec_())