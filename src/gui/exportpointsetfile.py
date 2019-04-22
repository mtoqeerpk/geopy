#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for exporting point sets as ascii file


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from basic.matdict import matdict as basic_mdt

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class exportpointsetfile(object):

    pointdata = {}
    #
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ExportPointSetFile):
        ExportPointSetFile.setObjectName("ExportPointSetFile")
        ExportPointSetFile.setFixedSize(400, 340)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/copy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ExportPointSetFile.setWindowIcon(icon)
        #
        self.lblpoint = QtWidgets.QLabel(ExportPointSetFile)
        self.lblpoint.setObjectName("lblpoint")
        self.lblpoint.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwgpoint = QtWidgets.QListWidget(ExportPointSetFile)
        self.lwgpoint.setObjectName("lwgpoint")
        self.lwgpoint.setGeometry(QtCore.QRect(160, 10, 230, 200))
        self.lwgpoint.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblsave = QtWidgets.QLabel(ExportPointSetFile)
        self.lblsave.setObjectName("lblsave")
        self.lblsave.setGeometry(QtCore.QRect(10, 230, 50, 30))
        self.ldtsave = QtWidgets.QLineEdit(ExportPointSetFile)
        self.ldtsave.setObjectName("ldtsave")
        self.ldtsave.setGeometry(QtCore.QRect(70, 230, 250, 30))
        self.btnsave = QtWidgets.QPushButton(ExportPointSetFile)
        self.btnsave.setObjectName("btnsave")
        self.btnsave.setGeometry(QtCore.QRect(330, 230, 60, 30))
        self.btnexportnpy = QtWidgets.QPushButton(ExportPointSetFile)
        self.btnexportnpy.setObjectName("btnexportnpy")
        self.btnexportnpy.setGeometry(QtCore.QRect(120, 280, 160, 30))
        self.btnexportnpy.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ExportPointSetFile)
        self.msgbox.setObjectName("msgbox")
        _center_x = ExportPointSetFile.geometry().center().x()
        _center_y = ExportPointSetFile.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ExportPointSetFile)
        QtCore.QMetaObject.connectSlotsByName(ExportPointSetFile)


    def retranslateGUI(self, ExportPointSetFile):
        self.dialog = ExportPointSetFile
        #
        _translate = QtCore.QCoreApplication.translate
        ExportPointSetFile.setWindowTitle(_translate("ExportPointSetFile", "Export PointSet File"))
        self.lblpoint.setText(_translate("ExportPointSetFile", "Select output pointsets:"))
        if len(self.pointdata.keys()) > 0:
            for i in sorted(self.pointdata.keys()):
                item = QtWidgets.QListWidgetItem(self.lwgpoint)
                item.setText(_translate("ExportPointSetFile", i))
                self.lwgpoint.addItem(item)
            self.lwgpoint.selectAll()
        self.lblsave.setText(_translate("ExportPointSetFile", "Save as:"))
        self.ldtsave.setText(_translate("ExportPointSetFile", ""))
        self.btnsave.setText(_translate("ExportPointSetFile", "Browse"))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnexportnpy.setText(_translate("ExportPointSetFile", "Export PointSet File"))
        self.btnexportnpy.clicked.connect(self.clickBtnExportPointSetFile)


    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Select PointSet File', self.rootpath,
                                        filter="PointSet Ascii files (*.txt);; All files (*.*)")
        if len(_file[0]) > 0:
            self.ldtsave.setText(_file[0])


    def clickBtnExportPointSetFile(self):
        self.refreshMsgBox()
        #
        _pointlist = self.lwgpoint.selectedItems()
        if len(_pointlist) < 1:
            print("ExportPointSetFile; No pointset selected for export")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Export PointSet FIle',
                                           'No pointset selected for export')
            return
        #
        if len(self.ldtsave.text()) < 1:
            print("ExportPointSetFile: No name specified for export")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Export PointSet File',
                                           'No name specified for export')
            return
        print("ExportPointSetFile: Export %d pointsets" % (len(_pointlist)))
        #
        _savepath = os.path.split(self.ldtsave.text())[0]
        _savename = os.path.split(self.ldtsave.text())[1]
        #
        if len(_pointlist) > 1:
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Export PointSet File',
                                                   'Warning: For exporting >=2 pointset, property name used as file name. Continue?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return
        #
        for i in range(len(_pointlist)):
            if len(_pointlist) > 1:
                _savename = _pointlist[i].text()
            #
            _file = open(os.path.join(_savepath, _savename), 'w')
            # write a header
            _file.write("# Headers:\n")
            if 'Inline' in self.pointdata[_pointlist[i].text()].keys():
                _file.write("# Inline\n")
            if 'Crossline' in self.pointdata[_pointlist[i].text()].keys():
                _file.write("# Crossline\n")
            if 'Z' in self.pointdata[_pointlist[i].text()].keys():
                _file.write("# Z\n")
            for j in sorted(self.pointdata[_pointlist[i].text()].keys()):
                if j != 'Inline' and j != 'Crossline' and j != 'Z':
                    _file.write("# " + j + '\n')
            # write points
            _npts = basic_mdt.maxDictConstantRow(self.pointdata[_pointlist[i].text()])
            for j in range(_npts):
                if 'Inline' in self.pointdata[_pointlist[i].text()].keys():
                    _file.write(str(self.pointdata[_pointlist[i].text()]['Inline'][j, 0])+'\t')
                if 'Crossline' in self.pointdata[_pointlist[i].text()].keys():
                    _file.write(str(self.pointdata[_pointlist[i].text()]['Crossline'][j, 0]) + '\t')
                if 'Z' in self.pointdata[_pointlist[i].text()].keys():
                    _file.write(str(self.pointdata[_pointlist[i].text()]['Z'][j, 0]) + '\t')
                for k in sorted(self.pointdata[_pointlist[i].text()].keys()):
                    if k != 'Inline' and k != 'Crossline' and k != 'Z':
                        _file.write(str(self.pointdata[_pointlist[i].text()][k][j, 0]) + '\t')
                _file.write('\n')
            #
            _file.close()
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Export PointSet File",
                                          str(len(_pointlist)) + " pointsets exported as Ascii File successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ExportPointSetFile = QtWidgets.QWidget()
    gui = exportpointsetfile()
    gui.setupGUI(ExportPointSetFile)
    ExportPointSetFile.show()
    sys.exit(app.exec_())