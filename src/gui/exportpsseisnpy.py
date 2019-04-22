#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for exporting pre-stack seismic as numpy


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])


QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class exportpsseisnpy(object):

    psseisdata = {}
    #
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ExportPsSeisNpy):
        ExportPsSeisNpy.setObjectName("ExportPsSeisNpy")
        ExportPsSeisNpy.setFixedSize(400, 390)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ExportPsSeisNpy.setWindowIcon(icon)
        #
        self.lblpsseis = QtWidgets.QLabel(ExportPsSeisNpy)
        self.lblpsseis.setObjectName("lblpsseis")
        self.lblpsseis.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwgpsseis = QtWidgets.QListWidget(ExportPsSeisNpy)
        self.lwgpsseis.setObjectName("lwgpsseis")
        self.lwgpsseis.setGeometry(QtCore.QRect(160, 10, 230, 200))
        self.lwgpsseis.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lbltype = QtWidgets.QLabel(ExportPsSeisNpy)
        self.lbltype.setObjectName("lbltype")
        self.lbltype.setGeometry(QtCore.QRect(10, 230, 150, 30))
        self.cbbtype = QtWidgets.QComboBox(ExportPsSeisNpy)
        self.cbbtype.setObjectName("cbbtype")
        self.cbbtype.setGeometry(QtCore.QRect(160, 230, 230, 30))
        self.lblsave = QtWidgets.QLabel(ExportPsSeisNpy)
        self.lblsave.setObjectName("lblsave")
        self.lblsave.setGeometry(QtCore.QRect(10, 280, 50, 30))
        self.ldtsave = QtWidgets.QLineEdit(ExportPsSeisNpy)
        self.ldtsave.setObjectName("ldtsave")
        self.ldtsave.setGeometry(QtCore.QRect(70, 280, 250, 30))
        self.btnsave = QtWidgets.QPushButton(ExportPsSeisNpy)
        self.btnsave.setObjectName("btnsave")
        self.btnsave.setGeometry(QtCore.QRect(330, 280, 60, 30))
        self.btnexportnpy = QtWidgets.QPushButton(ExportPsSeisNpy)
        self.btnexportnpy.setObjectName("btnexportnpy")
        self.btnexportnpy.setGeometry(QtCore.QRect(120, 330, 160, 30))
        self.btnexportnpy.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ExportPsSeisNpy)
        self.msgbox.setObjectName("msgbox")
        _center_x = ExportPsSeisNpy.geometry().center().x()
        _center_y = ExportPsSeisNpy.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ExportPsSeisNpy)
        QtCore.QMetaObject.connectSlotsByName(ExportPsSeisNpy)


    def retranslateGUI(self, ExportPsSeisNpy):
        self.dialog = ExportPsSeisNpy
        #
        _translate = QtCore.QCoreApplication.translate
        ExportPsSeisNpy.setWindowTitle(_translate("ExportPsSeisNpy", "Export Pre-stack Seismic NumPy"))
        self.lblpsseis.setText(_translate("ExportPsSeisNpy", "Select output pre-stack:"))
        if len(self.psseisdata.keys()) > 0:
            for i in sorted(self.psseisdata.keys()):
                item = QtWidgets.QListWidgetItem(self.lwgpsseis)
                item.setText(_translate("ExportPsSeisNpy", i))
                self.lwgpsseis.addItem(item)
            self.lwgpsseis.selectAll()
        self.lbltype.setText(_translate("ExportPsSeisNpy", "Select output type:"))
        self.cbbtype.addItems(['Dictionary', '3D numpy matrix'])
        self.cbbtype.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, "icons/pydict.png")))
        self.cbbtype.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, "icons/vis3d.png")))
        self.lblsave.setText(_translate("ExportPsSeisNpy", "Save as:"))
        self.ldtsave.setText(_translate("ExportPsSeisNpy", ""))
        self.btnsave.setText(_translate("ExportPsSeisNpy", "Browse"))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnexportnpy.setText(_translate("ExportPsSeisNpy", "Export Pre-stack NumPy"))
        self.btnexportnpy.clicked.connect(self.clickBtnExportPsSeisNpy)


    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Select Pre-stack Seismic NumPy', self.rootpath,
                                        filter="Pre-stack Seismic NumPy files (*.psseis.npy);; All files (*.*)")
        if len(_file[0]) > 0:
            self.ldtsave.setText(_file[0])


    def clickBtnExportPsSeisNpy(self):
        self.refreshMsgBox()
        #
        _psseislist = self.lwgpsseis.selectedItems()
        if len(_psseislist) < 1:
            print("ExportPsSeisNpy; No pre-stack seismic selected for export")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Export Pre-stack Seismic NumPy',
                                           'No pre-stack seismic selected for export')
            return
        #
        if len(self.ldtsave.text()) < 1:
            print("ExportPsSeisNpy: No name specified for NumPy")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Export Pre-stack Seismic NumPy',
                                           'No name specified for NumPy')
            return
        print("ExportPsSeisNpy: Export %d pre-stack seismic" % (len(_psseislist)))
        #
        _savepath = os.path.split(self.ldtsave.text())[0]
        _savename = os.path.split(self.ldtsave.text())[1]
        #
        if len(_psseislist) > 1 and self.cbbtype.currentIndex() >= 1:
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Export Pre-stack Seismic Numpy',
                                                   'Warning: For exporting >=2 pre-stack, property name used as file name. Continue?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return
        #
        if self.cbbtype.currentIndex() == 0:
            _npydata = {}
            for i in range(len(_psseislist)):
                _npydata[_psseislist[i].text()] = self.psseisdata[_psseislist[i].text()]
            #
            np.save(os.path.join(_savepath, _savename), _npydata)
        if self.cbbtype.currentIndex() == 1:
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Export Pre-stack Seismic Numpy',
                                                   'Warning: shots separately saved as numpy matrix & shot information lost. Continue?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return
            #
            _savename = _savename.replace('.psseis.npy', '')
            for _ps in _psseislist:
                if len(_psseislist) > 1:
                    _savename = _ps.text()
                _data = self.psseisdata[_ps.text()]
                for j in _data.keys():
                    if 'ShotData' in _data[j].keys():
                        np.save(os.path.join(_savepath, _savename+'_shot_'+j+'.psseis.npy'), _data[j]['ShotData'])
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Export Pre-stack Seismic NumPy",
                                          str(len(_psseislist)) + " pre-stack seismic exported as NumPy successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ExportPsSeisNpy = QtWidgets.QWidget()
    gui = exportpsseisnpy()
    gui.setupGUI(ExportPsSeisNpy)
    ExportPsSeisNpy.show()
    sys.exit(app.exec_())