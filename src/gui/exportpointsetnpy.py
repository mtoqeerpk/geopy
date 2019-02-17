#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# Create a window for exporting point sets as numpy


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from basic.matdict import matdict as basic_mdt

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class exportpointsetnpy(object):

    pointdata = {}
    #
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ExportPointSetNpy):
        ExportPointSetNpy.setObjectName("ExportPointSetNpy")
        ExportPointSetNpy.setFixedSize(400, 390)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ExportPointSetNpy.setWindowIcon(icon)
        #
        self.lblpoint = QtWidgets.QLabel(ExportPointSetNpy)
        self.lblpoint.setObjectName("lblpoint")
        self.lblpoint.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwgpoint = QtWidgets.QListWidget(ExportPointSetNpy)
        self.lwgpoint.setObjectName("lwgpoint")
        self.lwgpoint.setGeometry(QtCore.QRect(160, 10, 230, 200))
        self.lwgpoint.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lbltype = QtWidgets.QLabel(ExportPointSetNpy)
        self.lbltype.setObjectName("lbltype")
        self.lbltype.setGeometry(QtCore.QRect(10, 230, 150, 30))
        self.cbbtype = QtWidgets.QComboBox(ExportPointSetNpy)
        self.cbbtype.setObjectName("cbbtype")
        self.cbbtype.setGeometry(QtCore.QRect(160, 230, 230, 30))
        self.lblsave = QtWidgets.QLabel(ExportPointSetNpy)
        self.lblsave.setObjectName("lblsave")
        self.lblsave.setGeometry(QtCore.QRect(10, 280, 50, 30))
        self.ldtsave = QtWidgets.QLineEdit(ExportPointSetNpy)
        self.ldtsave.setObjectName("ldtsave")
        self.ldtsave.setGeometry(QtCore.QRect(70, 280, 250, 30))
        self.btnsave = QtWidgets.QPushButton(ExportPointSetNpy)
        self.btnsave.setObjectName("btnsave")
        self.btnsave.setGeometry(QtCore.QRect(330, 280, 60, 30))
        self.btnexportnpy = QtWidgets.QPushButton(ExportPointSetNpy)
        self.btnexportnpy.setObjectName("btnexportnpy")
        self.btnexportnpy.setGeometry(QtCore.QRect(120, 330, 160, 30))
        self.btnexportnpy.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ExportPointSetNpy)
        self.msgbox.setObjectName("msgbox")
        _center_x = ExportPointSetNpy.geometry().center().x()
        _center_y = ExportPointSetNpy.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ExportPointSetNpy)
        QtCore.QMetaObject.connectSlotsByName(ExportPointSetNpy)


    def retranslateGUI(self, ExportPointSetNpy):
        self.dialog = ExportPointSetNpy
        #
        _translate = QtCore.QCoreApplication.translate
        ExportPointSetNpy.setWindowTitle(_translate("ExportPointSetNpy", "Export PointSet NumPy"))
        self.lblpoint.setText(_translate("ExportPointSetNpy", "Select output pointsets:"))
        if len(self.pointdata.keys()) > 0:
            for i in sorted(self.pointdata.keys()):
                item = QtWidgets.QListWidgetItem(self.lwgpoint)
                item.setText(_translate("ExportPointSetNpy", i))
                self.lwgpoint.addItem(item)
            self.lwgpoint.selectAll()
        self.lbltype.setText(_translate("ExportPointSetNpy", "Select output type:"))
        self.cbbtype.addItems(['Dictionary', '2D numpy matrix'])
        self.cbbtype.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, "icons/pydict.png")))
        self.cbbtype.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, "icons/py2dmat.png")))
        self.lblsave.setText(_translate("ExportPointSetNpy", "Save as:"))
        self.ldtsave.setText(_translate("ExportPointSetNpy", ""))
        self.btnsave.setText(_translate("ExportPointSetNpy", "Browse"))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnexportnpy.setText(_translate("ExportPointSetNpy", "Export PointSet NumPy"))
        self.btnexportnpy.clicked.connect(self.clickBtnExportPointSetNpy)


    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Select PointSet NumPy', self.rootpath,
                                        filter="PointSet NumPy files (*.pts.npy);; All files (*.*)")
        if len(_file[0]) > 0:
            self.ldtsave.setText(_file[0])


    def clickBtnExportPointSetNpy(self):
        self.refreshMsgBox()
        #
        _pointlist = self.lwgpoint.selectedItems()
        if len(_pointlist) < 1:
            print("ExportPointSetNpy; No pointset selected for export")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Export PointSet NumPy',
                                           'No pointset selected for export')
            return
        #
        if len(self.ldtsave.text()) < 1:
            print("ExportPointSetNpy: No name specified for NumPy")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Export PointSet NumPy',
                                           'No name specified for NumPy')
            return
        print("ExportPointSetNpy: Export %d pointsets" % (len(_pointlist)))
        #
        _savepath = os.path.split(self.ldtsave.text())[0]
        _savename = os.path.split(self.ldtsave.text())[1]
        #
        if len(_pointlist) > 1 and self.cbbtype.currentIndex() >= 1:
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Export PointSet Numpy',
                                                   'Warning: For exporting >=2 pointset, property name used as file name. Continue?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return
        #
        if self.cbbtype.currentIndex() == 0:
            _npydata = {}
            for i in range(len(_pointlist)):
                _npydata[_pointlist[i].text()] = self.pointdata[_pointlist[i].text()]
            #
            np.save(os.path.join(_savepath, _savename), _npydata)
        if self.cbbtype.currentIndex() == 1:
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Export PointSet Numpy',
                                                   'Warning: property header not saved innumpy matrix. Continue?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return
            for i in range(len(_pointlist)):
                _data = basic_mdt.exportMatDict(self.pointdata[_pointlist[i].text()],
                                                ['Inline', 'Crossline', 'Z'])
                for j in self.pointdata[_pointlist[i].text()].keys():
                    if j != 'Inline' and j != 'Crossline' and j != 'Z':
                        _data = np.concatenate((_data, self.pointdata[_pointlist[i].text()][j]), axis=1)
                #
                if len(_pointlist) > 1:
                    _savename = _pointlist[i].text() + '.pts.npy'
                #
                np.save(os.path.join(_savepath, _savename), _data)
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Export PointSet NumPy",
                                          str(len(_pointlist)) + " pointsets exported as NumPy successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ExportPointSetNpy = QtWidgets.QWidget()
    gui = exportpointsetnpy()
    gui.setupGUI(ExportPointSetNpy)
    ExportPointSetNpy.show()
    sys.exit(app.exec_())
