#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for exporting seismic as numpy


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from seismic.analysis import analysis as seis_ays

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class exportseisnpy(object):

    survinfo = {}
    seisdata = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ExportSeisNpy):
        ExportSeisNpy.setObjectName("ExportSeisNpy")
        ExportSeisNpy.setFixedSize(400, 390)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/numpy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ExportSeisNpy.setWindowIcon(icon)
        #
        self.lblattrib = QtWidgets.QLabel(ExportSeisNpy)
        self.lblattrib.setObjectName("lblattrib")
        self.lblattrib.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwgattrib = QtWidgets.QListWidget(ExportSeisNpy)
        self.lwgattrib.setObjectName("lwgattrib")
        self.lwgattrib.setGeometry(QtCore.QRect(160, 10, 230, 200))
        self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lbltype = QtWidgets.QLabel(ExportSeisNpy)
        self.lbltype.setObjectName("lbltype")
        self.lbltype.setGeometry(QtCore.QRect(10, 230, 150, 30))
        self.cbbtype = QtWidgets.QComboBox(ExportSeisNpy)
        self.cbbtype.setObjectName("cbbtype")
        self.cbbtype.setGeometry(QtCore.QRect(160, 230, 230, 30))
        self.lblsave = QtWidgets.QLabel(ExportSeisNpy)
        self.lblsave.setObjectName("lblsave")
        self.lblsave.setGeometry(QtCore.QRect(10, 280, 50, 30))
        self.ldtsave = QtWidgets.QLineEdit(ExportSeisNpy)
        self.ldtsave.setObjectName("ldtsave")
        self.ldtsave.setGeometry(QtCore.QRect(70, 280, 250, 30))
        self.btnsave = QtWidgets.QPushButton(ExportSeisNpy)
        self.btnsave.setObjectName("btnsave")
        self.btnsave.setGeometry(QtCore.QRect(330, 280, 60, 30))
        self.btnexportnpy = QtWidgets.QPushButton(ExportSeisNpy)
        self.btnexportnpy.setObjectName("btnexportnpy")
        self.btnexportnpy.setGeometry(QtCore.QRect(120, 330, 160, 30))
        self.btnexportnpy.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ExportSeisNpy)
        self.msgbox.setObjectName("msgbox")
        _center_x = ExportSeisNpy.geometry().center().x()
        _center_y = ExportSeisNpy.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ExportSeisNpy)
        QtCore.QMetaObject.connectSlotsByName(ExportSeisNpy)


    def retranslateGUI(self, ExportSeisNpy):
        self.dialog = ExportSeisNpy
        #
        _translate = QtCore.QCoreApplication.translate
        ExportSeisNpy.setWindowTitle(_translate("ExportSeisNpy", "Export Seismic NumPy"))
        self.lblattrib.setText(_translate("ExportSeisNpy", "Select output properties:"))
        if self.checkSurvInfo() is True:
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i):
                    item = QtWidgets.QListWidgetItem(self.lwgattrib)
                    item.setText(_translate("ExportSeisNpy", i))
                    self.lwgattrib.addItem(item)
            self.lwgattrib.selectAll()
        self.lbltype.setText(_translate("ExportSeisNpy", "Select output type:"))
        self.cbbtype.addItems(['Dictionary', '2-D numpy matrix', '3-D numpy matrix'])
        self.cbbtype.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, "icons/pydict.png")))
        self.cbbtype.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, "icons/vis2d.png")))
        self.cbbtype.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, "icons/vis3d.png")))
        self.lblsave.setText(_translate("ExportSeisNpy", "Save as:"))
        self.ldtsave.setText(_translate("ExportSeisNpy", ""))
        self.btnsave.setText(_translate("ExportSeisNpy", "Browse"))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnexportnpy.setText(_translate("ExportSeisNpy", "Export NumPy"))
        self.btnexportnpy.clicked.connect(self.clickBtnExportSeisNpy)


    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Select Seismic NumPy', self.rootpath,
                                        filter="Seismic NumPy files (*.seis.npy);; All files (*.*)")
        if len(_file[0]) > 0:
            self.ldtsave.setText(_file[0])


    def clickBtnExportSeisNpy(self):
        self.refreshMsgBox()
        #
        _attriblist = self.lwgattrib.selectedItems()
        if len(_attriblist) < 1:
            print("ExportSeisNpy; No property selected for export")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Export Seismic NumPy',
                                           'No property selected for export')
            return
        #
        if len(self.ldtsave.text()) < 1:
            print("ExportSeisNpy: No name specified for NumPy")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Export Seismic NumPy',
                                           'No name specified for NumPy')
            return
        print("ExportSeisNpy: Export %d properties" % (len(_attriblist)))
        #
        _savepath = os.path.split(self.ldtsave.text())[0]
        _savename = os.path.split(self.ldtsave.text())[1]
        #
        if len(_attriblist) > 1 and self.cbbtype.currentIndex() >= 1:
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Export Seismic Numpy',
                                                   'Warning: For exporting >=2 seismic, property name used as file name. Continue?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return
        #
        if self.cbbtype.currentIndex() == 0:
            _npydata = {}
            _survinfo = seis_ays.convertSeisInfoTo2DMat(self.survinfo)
            _npydata['Inline'] = _survinfo[:, 0:1]
            _npydata['Crossline'] = _survinfo[:, 1:2]
            _npydata['Z'] = _survinfo[:, 2:3]
            for i in range(len(_attriblist)):
                _npydata[_attriblist[i].text()] = self.seisdata[_attriblist[i].text()]
            #
            np.save(os.path.join(_savepath, _savename), _npydata)
        if self.cbbtype.currentIndex() == 1:
            _npydata = seis_ays.convertSeisInfoTo2DMat(self.survinfo)
            for i in range(len(_attriblist)):
                _data = self.seisdata[_attriblist[i].text()]
                _data = np.reshape(_data, [_data.shape[0], -1])
                _data = np.concatenate((_npydata, _data), axis=1)
                if len(_attriblist) > 1:
                    _savename = _attriblist[i].text() + '.seis.npy'
                #
                np.save(os.path.join(_savepath, _savename), _data)
        if self.cbbtype.currentIndex() == 2:
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Export Seismic Numpy',
                                                   'Warning: survey information not saved in 3D numpy matrix. Continue?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return
            #
            for i in range(len(_attriblist)):
                _data = self.seisdata[_attriblist[i].text()]
                _data = np.reshape(_data, [_data.shape[0], -1])
                _data = np.mean(_data, axis=1)
                _data = np.reshape(_data, [len(_data), 1])
                _data = np.transpose(np.reshape(_data, [self.survinfo['ILNum'], self.survinfo['XLNum'], self.survinfo['ZNum']]),
                                     [2, 1, 0])
                if len(_attriblist) > 1:
                    _savename = _attriblist[i].text() + '.seis.npy'
                #
                np.save(os.path.join(_savepath, _savename), _data)
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Export Seismic NumPy",
                                          str(len(_attriblist)) + " properties exported as NumPy successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkSurvInfo(self):
        self.refreshMsgBox()
        #
        if seis_ays.checkSeisInfo(self.survinfo) is False:
            # print("ExportSeisNpy: Survey not found")
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Export Seismic NumPy',
            #                                'Survey not found')
            return False
        return True

    def checkSeisData(self, f):
        self.refreshMsgBox()
        #
        return seis_ays.isSeis2DMatConsistentWithSeisInfo(self.seisdata[f], self.survinfo)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ExportSeisNpy = QtWidgets.QWidget()
    gui = exportseisnpy()
    gui.setupGUI(ExportSeisNpy)
    ExportSeisNpy.show()
    sys.exit(app.exec_())