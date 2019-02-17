#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# Create a window for editing point sets


from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from basic.data import data as basic_data
from basic.matdict import matdict as basic_mdt
from core.settings import settings as core_set
from pointset.analysis import analysis as point_ays
from gui.viewpointset import viewpointset as gui_viewpointset
from gui.editseispointset import editseispointset as gui_editseispointset
from gui.filterpointset import filterpointset as gui_filterpointset
from gui.plot2dpointsetcrossplt import plot2dpointsetcrossplt as gui_plot2dpointsetcrossplt

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class editpointset(object):

    pointdata = {}
    rootpath = ''
    linestyle = core_set.Visual['Line']
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, EditPointSet):
        EditPointSet.setObjectName("EditPointSet")
        EditPointSet.setFixedSize(300, 420)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        EditPointSet.setWindowIcon(icon)
        #
        self.lblpoint = QtWidgets.QLabel(EditPointSet)
        self.lblpoint.setObjectName("lblpoint")
        self.lblpoint.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwgpoint = QtWidgets.QListWidget(EditPointSet)
        self.lwgpoint.setObjectName("lwgpoint")
        self.lwgpoint.setGeometry(QtCore.QRect(10, 50, 280, 200))
        self.lwgpoint.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lblaction = QtWidgets.QLabel(EditPointSet)
        self.lblaction.setObjectName("lblaction")
        self.lblaction.setGeometry(QtCore.QRect(110, 270, 40, 30))
        self.cbbaction = QtWidgets.QComboBox(EditPointSet)
        self.cbbaction.setObjectName("cbbaction")
        self.cbbaction.setGeometry(QtCore.QRect(160, 270, 130, 30))
        self.lblrename = QtWidgets.QLabel(EditPointSet)
        self.lblrename.setObjectName("lblrename")
        self.lblrename.setGeometry(QtCore.QRect(160, 310, 40, 30))
        self.ldtrename = QtWidgets.QLineEdit(EditPointSet)
        self.ldtrename.setObjectName("ldtrename")
        self.ldtrename.setGeometry(QtCore.QRect(200, 310, 90, 30))
        self.btnedit = QtWidgets.QPushButton(EditPointSet)
        self.btnedit.setObjectName("btnedit")
        self.btnedit.setGeometry(QtCore.QRect(100, 370, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnedit.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(EditPointSet)
        self.msgbox.setObjectName("msgbox")
        _center_x = EditPointSet.geometry().center().x()
        _center_y = EditPointSet.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(EditPointSet)
        QtCore.QMetaObject.connectSlotsByName(EditPointSet)


    def retranslateGUI(self, EditPointSet):
        self.dialog = EditPointSet
        #
        _translate = QtCore.QCoreApplication.translate
        EditPointSet.setWindowTitle(_translate("EditPointSet", "Edit PointSet"))
        self.lblpoint.setText(_translate("EditPointSet", "List of available pointsets:"))
        self.lblaction.setText(_translate("EditPointSet", "Action:"))
        self.cbbaction.addItems(['Copy', 'Delete', 'Rename', 'Filter', 'Subset', 'Edit', 'View', 'Cross-plot'])
        self.cbbaction.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, "icons/copy.png")))
        self.cbbaction.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, "icons/delete.png")))
        self.cbbaction.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, "icons/rename.png")))
        self.cbbaction.setItemIcon(3, QtGui.QIcon(os.path.join(self.iconpath, "icons/filter.png")))
        self.cbbaction.setItemIcon(4, QtGui.QIcon(os.path.join(self.iconpath, "icons/export.png")))
        self.cbbaction.setItemIcon(5, QtGui.QIcon(os.path.join(self.iconpath, "icons/pen.png")))
        self.cbbaction.setItemIcon(6, QtGui.QIcon(os.path.join(self.iconpath, "icons/view.png")))
        self.cbbaction.setItemIcon(7, QtGui.QIcon(os.path.join(self.iconpath, "icons/plotpoint.png")))
        self.cbbaction.currentIndexChanged.connect(self.changeCbbAction)
        self.lblrename.setText(_translate("EditPointSet", ""))
        self.lblrename.setVisible(False)
        self.ldtrename.setText(_translate("EditPointSet", ""))
        self.ldtrename.setVisible(False)
        self.btnedit.setText(_translate("EditPointSet", "Apply"))
        self.btnedit.clicked.connect(self.clickBtnEditPointSet)
        #
        self.refreshLwgPoint()


    def changeCbbAction(self):
        if self.cbbaction.currentIndex() == 2:
            self.lblrename.setText('Name:')
            self.lblrename.setVisible(True)
            self.ldtrename.setVisible(True)
        elif self.cbbaction.currentIndex() == 4:
            self.lblrename.setText('Size:')
            self.lblrename.setVisible(True)
            self.ldtrename.setVisible(True)
        else:
            self.lblrename.setText('')
            self.lblrename.setVisible(False)
            self.ldtrename.setText('')
            self.ldtrename.setVisible(False)


    def clickBtnEditPointSet(self):
        self.refreshMsgBox()
        #
        _pointlist = self.lwgpoint.selectedItems()
        if len(_pointlist) < 1:
            print("EditPointSet: No pointset selected for editing")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Edit PointSet',
                                           'No pointset selected for editing')
            return
        #
        if self.cbbaction.currentIndex() == 0:
            self.pointdata[_pointlist[0].text()+'_copy'] = self.pointdata[_pointlist[0].text()]
        if self.cbbaction.currentIndex() == 1:
            self.pointdata.pop(_pointlist[0].text())
        if self.cbbaction.currentIndex() == 2:
            if len(self.ldtrename.text()) < 1:
                print("EditPointSet: No name specified for rename")
                QtWidgets.QMessageBox.critical(self.msgbox,
                                               'Edit PointSet',
                                               'No name specified for rename')
                return
            if self.ldtrename.text() in self.pointdata.keys():
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Edit PointSet',
                                                       self.ldtrename.text() + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)

                if reply == QtWidgets.QMessageBox.No:
                    return
            self.pointdata[self.ldtrename.text()] = self.pointdata[_pointlist[0].text()]
            self.pointdata.pop(_pointlist[0].text())
        if self.cbbaction.currentIndex() == 3:
            _filter = QtWidgets.QDialog()
            _gui = gui_filterpointset()
            _gui.pointname = _pointlist[0].text()
            _gui.pointdata = self.pointdata[_pointlist[0].text()].copy()
            _gui.setupGUI(_filter)
            _filter.exec()
            self.pointdata[_pointlist[0].text()] = _gui.pointdata.copy()
            _filter.show()
        if self.cbbaction.currentIndex() == 4:
            _size = basic_data.str2int(self.ldtrename.text())
            if _size is False:
                print("EditPointSet: Non-integer size")
                QtWidgets.QMessageBox.critical(self.msgbox,
                                               'Edit PointSet',
                                               'Non-integer size')
                return
            self.pointdata[_pointlist[0].text()] = basic_mdt.retrieveDictRandom(self.pointdata[_pointlist[0].text()],
                                                                                batch_size=_size)
        if self.cbbaction.currentIndex() == 5:
            _editpoint = QtWidgets.QDialog()
            _gui = gui_editseispointset()
            _gui.seispointdata = self.pointdata[_pointlist[0].text()]
            _gui.rootpath = self.rootpath
            _gui.setupGUI(_editpoint)
            _editpoint.exec()
            self.pointdata[_pointlist[0].text()] = _gui.seispointdata
            _editpoint.show()
        if self.cbbaction.currentIndex() == 6:
            _view = QtWidgets.QDialog()
            _gui = gui_viewpointset()
            _gui.pointname = _pointlist[0].text()
            _gui.pointdata = self.pointdata[_pointlist[0].text()]
            _gui.linestyle = self.linestyle
            _gui.setupGUI(_view)
            _view.exec()
            # self.pointdata = _gui.pointdata.copy()
            _view.show()
        if self.cbbaction.currentIndex() == 7:
            _cplt = QtWidgets.QDialog()
            _gui = gui_plot2dpointsetcrossplt()
            _gui.pointdata = {}
            _gui.pointdata[_pointlist[0].text()] = self.pointdata[_pointlist[0].text()]
            _gui.linestyle = self.linestyle
            _gui.setupGUI(_cplt)
            _cplt.exec()
            _cplt.show()
        #
        self.refreshLwgPoint()
        # if self.cbbaction.currentIndex() != 3:
            # QtWidgets.QMessageBox.information(self.msgbox,
            #                                   "Edit PointSet",
            #                                   "PointSet edited successfully")
        return


    def refreshLwgPoint(self):
        self.lwgpoint.clear()
        if len(self.pointdata.keys()) > 0:
            for i in sorted(self.pointdata.keys()):
                if self.checkPointSet(i):
                    item = QtWidgets.QListWidgetItem(self.lwgpoint)
                    item.setText(i)
                    self.lwgpoint.addItem(item)


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkPointSet(self, name):
        return point_ays.checkPoint(self.pointdata[name])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EditPointSet = QtWidgets.QWidget()
    gui = editpointset()
    gui.setupGUI(EditPointSet)
    EditPointSet.show()
    sys.exit(app.exec_())
