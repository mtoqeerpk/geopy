#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for converting pre-stack to seismic


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from psseismic.analysis import analysis as psseis_ays
from seismic.analysis import analysis as seis_ays

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class convertpsseis2seis(object):

    survinfo = {}
    seisdata = {}
    psseisdata = {}
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ConvertPsSeis2Seis):
        ConvertPsSeis2Seis.setObjectName("ConvertPsSeis2Seis")
        ConvertPsSeis2Seis.setFixedSize(400, 410)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/psseismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ConvertPsSeis2Seis.setWindowIcon(icon)
        #
        self.lblpsseis = QtWidgets.QLabel(ConvertPsSeis2Seis)
        self.lblpsseis.setObjectName("lblpsseis")
        self.lblpsseis.setGeometry(QtCore.QRect(10, 10, 170, 30))
        self.lwgpsseis = QtWidgets.QListWidget(ConvertPsSeis2Seis)
        self.lwgpsseis.setObjectName("lwgpsseis")
        self.lwgpsseis.setGeometry(QtCore.QRect(10, 50, 170, 200))
        self.lwgpsseis.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lblarrow = QtWidgets.QLabel(ConvertPsSeis2Seis)
        self.lblarrow.setObjectName("lblarrow")
        self.lblarrow.setGeometry(QtCore.QRect(180, 110, 40, 30))
        self.lblpsshot = QtWidgets.QLabel(ConvertPsSeis2Seis)
        self.lblpsshot.setObjectName("lblpsshot")
        self.lblpsshot.setGeometry(QtCore.QRect(220, 10, 170, 30))
        self.lwgpsshot = QtWidgets.QListWidget(ConvertPsSeis2Seis)
        self.lwgpsshot.setObjectName("lwgshot")
        self.lwgpsshot.setGeometry(QtCore.QRect(220, 50, 170, 200))
        self.lwgpsshot.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.btnapply = QtWidgets.QPushButton(ConvertPsSeis2Seis)
        self.btnapply.setObjectName("btnedit")
        self.btnapply.setGeometry(QtCore.QRect(150, 360, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ConvertPsSeis2Seis)
        self.msgbox.setObjectName("msgbox")
        _center_x = ConvertPsSeis2Seis.geometry().center().x()
        _center_y = ConvertPsSeis2Seis.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ConvertPsSeis2Seis)
        QtCore.QMetaObject.connectSlotsByName(ConvertPsSeis2Seis)


    def retranslateGUI(self, ConvertPsSeis2Seis):
        self.dialog = ConvertPsSeis2Seis
        #
        _translate = QtCore.QCoreApplication.translate
        ConvertPsSeis2Seis.setWindowTitle(_translate("ConvertPsSeis2Seis", "Convert Pre-stack to Seismic"))
        self.lblpsseis.setText(_translate("ConvertPsSeis2Seis", "Select pre-stack:"))
        self.lwgpsseis.itemSelectionChanged.connect(self.changeLwgPsSeis)
        self.lblarrow.setText(_translate("ConvertPsSeis2Seis", "==>"))
        self.lblarrow.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpsshot.setText(_translate("ConvertPsSeis2Seis", "Select shot:"))
        self.btnapply.setText(_translate("ConvertPsSeis2Seis", "Apply"))
        self.btnapply.clicked.connect(self.clickBtnApply)
        #
        self.lwgpsseis.clear()
        if len(self.psseisdata.keys()) > 0:
            for i in sorted(self.psseisdata.keys()):
                if self.checkPsSeisData(i):
                    item = QtWidgets.QListWidgetItem(self.lwgpsseis)
                    item.setText(i)
                    self.lwgpsseis.addItem(item)


    def changeLwgPsSeis(self):
        self.lwgpsshot.clear()
        _firstshot = None
        #
        _psseislist = self.lwgpsseis.selectedItems()
        _psseislist = [f.text() for f in _psseislist]
        if len(_psseislist) > 0:
            for _k in self.psseisdata[_psseislist[0]].keys():
                item = QtWidgets.QListWidgetItem(self.lwgpsshot)
                item.setText(_k)
                self.lwgpsshot.addItem(item)
                if _firstshot is None:
                    _firstshot = item
        if _firstshot is not None:
            self.lwgpsshot.setCurrentItem(_firstshot)


    def clickBtnApply(self):
        self.refreshMsgBox()
        #
        _psseislist = self.lwgpsseis.selectedItems()
        _psseislist = [f.text() for f in _psseislist]
        if len(_psseislist) < 1:
            print("ConvertPsSeis2Seis: No pre-stack selected for conversion")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Convert Pre-stack to Seismic',
                                           'No pre-stack selected for conversion')
            return
        #
        _psshotlist = self.lwgpsshot.selectedItems()
        _psshotlist = [f.text() for f in _psshotlist]
        if len(_psshotlist) < 1:
            print("ConvertPsSeis2Seis: No shot selected for conversion")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                            'Convert Pre-stack to Seismic',
                                            'No shot selected for conversion')
            return
        #
        _psseisdata = self.psseisdata[_psseislist[0]][_psshotlist[0]]['ShotData']
        _psseisinfo = self.psseisdata[_psseislist[0]][_psshotlist[0]]['ShotInfo']
        _nz, _nt, _nl = np.shape(_psseisdata)
        if checkSurvInfo(self.survinfo) \
                and self.survinfo['ZNum'] == np.shape(_psseisdata)[0] \
                and self.survinfo['XLNum'] == np.shape(_psseisdata)[1] \
                and self.survinfo['ILNum'] == np.shape(_psseisdata)[2]:
            _survinfo = self.survinfo
        else:
            _survinfo = seis_ays.createSeisInfoFrom3DMat(_psseisdata,
                                                         zstart=_psseisinfo['ZStart'],
                                                         zstep=_psseisinfo['ZStep'],
                                                         xlstart=_psseisinfo['XLStart'],
                                                         xlstep=_psseisinfo['XLStep'],
                                                         inlstart=_psseisinfo['ILStart'],
                                                         inlstep=_psseisinfo['ILStep']
                                                         )
        #
        _seisdata = {}
        _seisdata[_psshotlist[0]] = np.reshape(np.transpose(_psseisdata, [2, 1, 0]), [-1, 1])
        #
        # add new data to seisdata
        if checkSurvInfo(_survinfo):
            self.survinfo = _survinfo
        for key in _seisdata.keys():
            if key in self.seisdata.keys() and checkSeisData(self.seisdata[key], self.survinfo):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Convert Pre-stack to Seismic',
                                                       key + ' already exists. Overwrite?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
            self.seisdata[key] = _seisdata[key]
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Convert Pre-stack to Seismic",
                                          "Pre-stack seismic converted successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkPsSeisData(self, name):
        return psseis_ays.checkPsSeis(self.psseisdata[name])


def checkSurvInfo(survinfo):
    return seis_ays.checkSeisInfo(survinfo)

def checkSeisData(seisdata, survinfo):
    return seis_ays.isSeis2DMatConsistentWithSeisInfo(seisdata, survinfo)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConvertPsSeis2Seis = QtWidgets.QWidget()
    gui = convertpsseis2seis()
    gui.setupGUI(ConvertPsSeis2Seis)
    ConvertPsSeis2Seis.show()
    sys.exit(app.exec_())