#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for cropping a survey into points


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4])
from basic.data import data as basic_data
from seismic.analysis import analysis as seis_ays

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class convertseis2pointset(object):

    survinfo = {}
    seisdata = {}
    pointdata = {}
    #
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, ConvertSeis2PointSet):
        ConvertSeis2PointSet.setObjectName("ConvertSeis2PointSet")
        ConvertSeis2PointSet.setFixedSize(440, 450)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ConvertSeis2PointSet.setWindowIcon(icon)
        self.lblsrvinfo = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblsrvinfo.setObjectName("lblsrvinfo")
        self.lblsrvinfo.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.rdbsrvall = QtWidgets.QRadioButton(ConvertSeis2PointSet)
        self.rdbsrvall.setObjectName("rdbsrvall")
        self.rdbsrvall.setGeometry(QtCore.QRect(130, 10, 150, 30))
        self.rdbsrvpart = QtWidgets.QRadioButton(ConvertSeis2PointSet)
        self.rdbsrvpart.setObjectName("rdbsrvpart")
        self.rdbsrvpart.setGeometry(QtCore.QRect(280, 10, 150, 30))
        self.lblstart = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblstart.setObjectName("lblstart")
        self.lblstart.setGeometry(QtCore.QRect(120, 50, 80, 30))
        self.lblend = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblend.setObjectName("lblend")
        self.lblend.setGeometry(QtCore.QRect(220, 50, 80, 30))
        self.lblstep = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblstep.setObjectName("lblstep")
        self.lblstep.setGeometry(QtCore.QRect(320, 50, 40, 30))
        self.lblinl = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblinl.setObjectName("lblinl")
        self.lblinl.setGeometry(QtCore.QRect(10, 90, 100, 30))
        self.lblxl = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblxl.setObjectName("lblxl")
        self.lblxl.setGeometry(QtCore.QRect(10, 130, 100, 30))
        self.lblz = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblz.setObjectName("lblz")
        self.lblz.setGeometry(QtCore.QRect(10, 170, 100, 30))
        self.ldtinlstart = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtinlstart.setObjectName("ldtinlstart")
        self.ldtinlstart.setGeometry(QtCore.QRect(120, 90, 80, 30))
        self.ldtinlend = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtinlend.setObjectName("ldtinlend")
        self.ldtinlend.setGeometry(QtCore.QRect(220, 90, 80, 30))
        self.ldtinlstep = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtinlstep.setObjectName("ldtinlstep")
        self.ldtinlstep.setGeometry(QtCore.QRect(320, 90, 40, 30))
        self.lblinlitvl = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblinlitvl.setObjectName("lblinlitvl")
        self.lblinlitvl.setGeometry(QtCore.QRect(370, 90, 10, 30))
        self.cbbinlitvl = QtWidgets.QComboBox(ConvertSeis2PointSet)
        self.cbbinlitvl.setObjectName("cbbinlitvl")
        self.cbbinlitvl.setGeometry(QtCore.QRect(385, 90, 45, 30))
        self.ldtxlstart = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtxlstart.setObjectName("ldtxlstart")
        self.ldtxlstart.setGeometry(QtCore.QRect(120, 130, 80, 30))
        self.ldtxlend = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtxlend.setObjectName("ldtxlend")
        self.ldtxlend.setGeometry(QtCore.QRect(220, 130, 80, 30))
        self.ldtxlstep = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtxlstep.setObjectName("ldtxlstep")
        self.ldtxlstep.setGeometry(QtCore.QRect(320, 130, 40, 30))
        self.lblxlitvl = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblxlitvl.setObjectName("lblxlitvl")
        self.lblxlitvl.setGeometry(QtCore.QRect(370, 130, 10, 30))
        self.cbbxlitvl = QtWidgets.QComboBox(ConvertSeis2PointSet)
        self.cbbxlitvl.setObjectName("cbbxlitvl")
        self.cbbxlitvl.setGeometry(QtCore.QRect(385, 130, 45, 30))
        self.ldtzstart = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtzstart.setObjectName("ldtzstart")
        self.ldtzstart.setGeometry(QtCore.QRect(120, 170, 80, 30))
        self.ldtzend = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtzend.setObjectName("ldtzend")
        self.ldtzend.setGeometry(QtCore.QRect(220, 170, 80, 30))
        self.ldtzstep = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtzstep.setObjectName("ldtzlstep")
        self.ldtzstep.setGeometry(QtCore.QRect(320, 170, 40, 30))
        self.lblzitvl = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblzitvl.setObjectName("lblzitvl")
        self.lblzitvl.setGeometry(QtCore.QRect(370, 170, 10, 30))
        self.cbbzitvl = QtWidgets.QComboBox(ConvertSeis2PointSet)
        self.cbbzitvl.setObjectName("cbbzitvl")
        self.cbbzitvl.setGeometry(QtCore.QRect(385, 170, 45, 30))
        #
        self.lblattrib = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblattrib.setObjectName("lblattrib")
        self.lblattrib.setGeometry(QtCore.QRect(10, 210, 150, 30))
        self.lwgattrib = QtWidgets.QListWidget(ConvertSeis2PointSet)
        self.lwgattrib.setObjectName("lwgattrib")
        self.lwgattrib.setGeometry(QtCore.QRect(10, 250, 220, 180))
        self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        ##
        self.lblsave = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblsave.setObjectName("lblsave")
        self.lblsave.setGeometry(QtCore.QRect(250, 350, 70, 30))
        self.ldtsave = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtsave.setObjectName("ldtsave")
        self.ldtsave.setGeometry(QtCore.QRect(330, 350, 100, 30))
        #
        self.btnapply = QtWidgets.QPushButton(ConvertSeis2PointSet)
        self.btnapply.setObjectName("btnapply")
        self.btnapply.setGeometry(QtCore.QRect(330, 400, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ConvertSeis2PointSet)
        self.msgbox.setObjectName("msgbox")
        _center_x = ConvertSeis2PointSet.geometry().center().x()
        _center_y = ConvertSeis2PointSet.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ConvertSeis2PointSet)
        QtCore.QMetaObject.connectSlotsByName(ConvertSeis2PointSet)


    def retranslateGUI(self, ConvertSeis2PointSet):
        self.dialog = ConvertSeis2PointSet
        #
        _translate = QtCore.QCoreApplication.translate
        ConvertSeis2PointSet.setWindowTitle(_translate("ConvertSeis2PointSet", "Convert Seismic to PointSet"))
        self.lblsrvinfo.setText(_translate("ConvertSeis2PointSet", "Select survey:"))
        self.rdbsrvall.setText(_translate("ExportSeisSegy", "All"))
        self.rdbsrvall.setChecked(False)
        self.rdbsrvall.clicked.connect(self.clickRdbSrvAll)
        self.rdbsrvpart.setText(_translate("ExportSeisSegy", "Customize"))
        self.rdbsrvpart.setChecked(True)
        self.rdbsrvpart.clicked.connect(self.clickRdbSrvPart)
        self.lblstart.setText(_translate("ConvertSeis2PointSet", "Start"))
        self.lblstart.setAlignment(QtCore.Qt.AlignCenter)
        self.lblend.setText(_translate("ConvertSeis2PointSet", "End"))
        self.lblend.setAlignment(QtCore.Qt.AlignCenter)
        self.lblstep.setText(_translate("ConvertSeis2PointSet", "Step"))
        self.lblstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblinl.setText(_translate("ConvertSeis2PointSet", "Inline:"))
        self.lblinl.setAlignment(QtCore.Qt.AlignRight)
        self.lblxl.setText(_translate("ConvertSeis2PointSet", "Crossline:"))
        self.lblxl.setAlignment(QtCore.Qt.AlignRight)
        self.lblz.setText(_translate("ConvertSeis2PointSet", "Time/depth:"))
        self.lblz.setAlignment(QtCore.Qt.AlignRight)
        self.ldtinlstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtinlend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtinlstep.setEnabled(False)
        self.ldtinlstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblinlitvl.setText(_translate("ConvertSeis2PointSet", "X"))
        self.cbbinlitvl.addItems([str(i+1) for i in range(100)])
        self.ldtxlstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlstep.setEnabled(False)
        self.ldtxlstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblxlitvl.setText(_translate("ConvertSeis2PointSet", "X"))
        self.cbbxlitvl.addItems([str(i + 1) for i in range(100)])
        self.ldtzstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtzend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtzstep.setEnabled(False)
        self.ldtzstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblzitvl.setText(_translate("ConvertSeis2PointSet", "X"))
        self.cbbzitvl.addItems([str(i + 1) for i in range(100)])
        #
        self.lblattrib.setText(_translate("ConvertSeis2PointSet", "Select properties:"))
        #
        if self.checkSurvInfo() is True:
            _survinfo = self.survinfo
            self.ldtinlstart.setText(_translate("ConvertSeis2PointSet", str(_survinfo['ILStart'])))
            self.ldtinlend.setText(_translate("ConvertSeis2PointSet", str(_survinfo['ILEnd'])))
            self.ldtinlstep.setText(_translate("ConvertSeis2PointSet", str(_survinfo['ILStep'])))
            self.ldtxlstart.setText(_translate("ConvertSeis2PointSet", str(_survinfo['XLStart'])))
            self.ldtxlend.setText(_translate("ConvertSeis2PointSet", str(_survinfo['XLEnd'])))
            self.ldtxlstep.setText(_translate("ConvertSeis2PointSet", str(_survinfo['XLStep'])))
            self.ldtzstart.setText(_translate("ConvertSeis2PointSet", str(_survinfo['ZStart'])))
            self.ldtzend.setText(_translate("ConvertSeis2PointSet", str(_survinfo['ZEnd'])))
            self.ldtzstep.setText(_translate("ConvertSeis2PointSet", str(_survinfo['ZStep'])))
            #
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i):
                    item = QtWidgets.QListWidgetItem(self.lwgattrib)
                    item.setText(i)
                    self.lwgattrib.addItem(item)
            # self.lwgattrib.selectAll()
        #
        self.lblsave.setText(_translate("ConvertSeis2PointSet", "Save as"))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate("ConvertSeis2PointSet", 'pointset'))
        self.ldtsave.setAlignment(QtCore.Qt.AlignCenter)
        #
        self.btnapply.setText(_translate("ConvertSeis2PointSet", "Apply"))
        self.btnapply.clicked.connect(self.clickBtnApply)


    def clickRdbSrvAll(self):
        if self.rdbsrvall.isChecked():
            self.rdbsrvall.setChecked(True)
            self.rdbsrvpart.setChecked(False)
            #
            self.cbbinlitvl.setCurrentIndex(0)
            self.cbbxlitvl.setCurrentIndex(0)
            self.cbbzitvl.setCurrentIndex(0)
            #
            self.ldtinlstart.setEnabled(False)
            self.ldtinlend.setEnabled(False)
            self.ldtxlstart.setEnabled(False)
            self.ldtxlend.setEnabled(False)
            self.ldtzstart.setEnabled(False)
            self.ldtzend.setEnabled(False)
            self.cbbinlitvl.setEnabled(False)
            self.cbbxlitvl.setEnabled(False)
            self.cbbzitvl.setEnabled(False)
            #
            if self.checkSurvInfo() is True:
                _survinfo = self.survinfo
                self.ldtinlstart.setText(str(_survinfo['ILStart']))
                self.ldtinlend.setText(str(_survinfo['ILEnd']))
                self.ldtinlstep.setText(str(_survinfo['ILStep']))
                self.ldtxlstart.setText(str(_survinfo['XLStart']))
                self.ldtxlend.setText(str(_survinfo['XLEnd']))
                self.ldtxlstep.setText(str(_survinfo['XLStep']))
                self.ldtzstart.setText(str(_survinfo['ZStart']))
                self.ldtzend.setText(str(_survinfo['ZEnd']))
                self.ldtzstep.setText(str(_survinfo['ZStep']))


    def clickRdbSrvPart(self):
        if self.rdbsrvpart.isChecked():
            self.rdbsrvpart.setChecked(True)
            self.rdbsrvall.setChecked(False)
            #
            self.ldtinlstart.setEnabled(True)
            self.ldtinlend.setEnabled(True)
            self.ldtxlstart.setEnabled(True)
            self.ldtxlend.setEnabled(True)
            self.ldtzstart.setEnabled(True)
            self.ldtzend.setEnabled(True)
            self.cbbinlitvl.setEnabled(True)
            self.cbbxlitvl.setEnabled(True)
            self.cbbzitvl.setEnabled(True)


    def clickBtnApply(self):
        self.refreshMsgBox()
        #
        if self.ldtsave.text() in self.pointdata.keys():
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Convert Seismic to PointSet',
                                                   self.ldtsave.text() + ' already exists. Overwrite?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return
        #
        if self.checkSurvInfo() is False:
            print("ConvertSeis2PointSet: No seismic survey found")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Convert Seismic to PointSet',
                                           'No seismic survey found')
            return
        #
        if self.rdbsrvpart.isChecked():
            _inlstart = basic_data.str2int(self.ldtinlstart.text())
            _xlstart = basic_data.str2int(self.ldtxlstart.text())
            _zstart = basic_data.str2int(self.ldtzstart.text())
            _inlend = basic_data.str2int(self.ldtinlend.text())
            _xlend = basic_data.str2int(self.ldtxlend.text())
            _zend = basic_data.str2int(self.ldtzend.text())
            if _inlstart is False or _xlstart is False or _zstart is False \
                    or _inlend is False or _xlend is False or _zend is False:
                print("ConvertSeis2PointSet: Non-integer survey selection")
                QtWidgets.QMessageBox.critical(self.msgbox,
                                               'Convert Seismic to PointSet',
                                               'Non-integer survey selection')
                return
        #
        _survinfo = self.survinfo
        #
        if self.rdbsrvall.isChecked():
            _pts = seis_ays.convertSeisInfoTo2DMat(self.survinfo)
        if self.rdbsrvpart.isChecked():
            _inlstart_idx = _inlstart - _survinfo['ILStart']
            _inlstart_idx = int(_inlstart_idx / _survinfo['ILStep'])
            _xlstart_idx = _xlstart - _survinfo['XLStart']
            _xlstart_idx = int(_xlstart_idx / _survinfo['XLStep'])
            _zstart_idx = _zstart - _survinfo['ZStart']
            _zstart_idx = int(_zstart_idx / _survinfo['ZStep'])
            if _inlstart_idx < 0:
                _inlstart_idx = 0
            if _xlstart_idx < 0:
                _xlstart_idx = 0
            if _zstart_idx < 0:
                _zstart_idx = 0
            if _inlstart_idx >= _survinfo['ILNum']:
                _inlstart_idx = _survinfo['ILNum'] - 1
            if _xlstart_idx >= _survinfo['XLNum']:
                _xlstart_idx = _survinfo['XLNum'] - 1
            if _zstart_idx >= _survinfo['ZNum']:
                _zstart_idx = _survinfo['ZNum'] - 1
            _inlend_idx = _inlend - _survinfo['ILStart']
            _inlend_idx = int(_inlend_idx / _survinfo['ILStep'])
            _xlend_idx = _xlend - _survinfo['XLStart']
            _xlend_idx = int(_xlend_idx / _survinfo['XLStep'])
            _zend_idx = _zend - _survinfo['ZStart']
            _zend_idx = int(_zend_idx / _survinfo['ZStep'])
            if _inlend_idx >= _survinfo['ILNum']:
                _inlend_idx = _survinfo['ILNum'] - 1
            if _xlend_idx >= _survinfo['XLNum']:
                _xlend_idx = _survinfo['XLNum'] - 1
            if _zend_idx >= _survinfo['ZNum']:
                _zend_idx = _survinfo['ZNum'] - 1
            if _inlend_idx < _inlstart_idx:
                _inlend_idx = _inlstart_idx
            if _xlend_idx < _xlstart_idx:
                _xlend_idx = _xlstart_idx
            if _zend_idx < _zstart_idx:
                _zend_idx = _zstart_idx
            #
            _inlidx = np.arange(_inlstart_idx, _inlend_idx + 1,
                                self.cbbinlitvl.currentIndex() + 1, dtype=int)
            _xlidx = np.arange(_xlstart_idx, _xlend_idx + 1,
                               self.cbbxlitvl.currentIndex() + 1, dtype=int)
            _zidx = np.arange(_zstart_idx, _zend_idx + 1,
                              self.cbbzitvl.currentIndex() + 1, dtype=int)
            #
            _inl = _inlidx * _survinfo['ILStep'] + _survinfo['ILStart']
            _xl = _xlidx * _survinfo['XLStep'] + _survinfo['XLStart']
            _z = _zidx * _survinfo['ZStep'] + _survinfo['ZStart']
            #
            _pts = seis_ays.retrieveSeisILSliceFrom3DMat(np.zeros([self.survinfo['ZNum'], self.survinfo['XLNum'], self.survinfo['ILNum']]),
                                                         inlsls=_inl, verbose=False, seisinfo=self.survinfo)
            _pts = seis_ays.retrieveSeisXLSliceFrom3DMat(seis_ays.convertSeis2DMatTo3DMat(_pts), xlsls=_xl, verbose=False,
                                                         seisinfo=seis_ays.getSeisInfoFrom2DMat(_pts))
            _pts = seis_ays.retrieveSeisZSliceFrom3DMat(seis_ays.convertSeis2DMatTo3DMat(_pts), zsls=_z, verbose=False,
                                                        seisinfo=seis_ays.getSeisInfoFrom2DMat(_pts))
        #
        self.pointdata[self.ldtsave.text()] = {}
        self.pointdata[self.ldtsave.text()]['Inline'] = _pts[:, 0:1]
        self.pointdata[self.ldtsave.text()]['Crossline'] = _pts[:, 1:2]
        self.pointdata[self.ldtsave.text()]['Z'] = _pts[:, 2:3]
        #
        _proplist = self.lwgattrib.selectedItems()
        _proplist = [f.text() for f in _proplist]
        #
        # Progress dialog
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/seismic.png")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Retrieve ' + str(len(_proplist)) + ' Property(s)')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        _pgsdlg.setMaximum(len(_proplist))

        for _idx in range(len(_proplist)):
            QtCore.QCoreApplication.instance().processEvents()
            _pgsdlg.setValue(_idx)
            #
            if self.rdbsrvall.isChecked():
                self.pointdata[self.ldtsave.text()][_proplist[_idx]] = self.seisdata[_proplist[_idx]]
            if self.rdbsrvpart.isChecked():
                _data = self.seisdata[_proplist[_idx]]
                _data = \
                    np.transpose(np.reshape(_data, [self.survinfo['ILNum'], self.survinfo['XLNum'], self.survinfo['ZNum']]),
                                 [2, 1, 0])
                self.pointdata[self.ldtsave.text()][_proplist[_idx]] = \
                    seis_ays.retrieveSeisSampleFrom3DMat(_data, seisinfo=self.survinfo, verbose=False,
                                                         samples=_pts)[:, 3:4]
        _pgsdlg.setValue(len(_proplist))
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Convert Seismic to PointSet",
                                          str(len(_pts)) + " seismic converted successfully")

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkSurvInfo(self):
        self.refreshMsgBox()
        #
        if seis_ays.checkSeisInfo(self.survinfo) is False:
            # print("ConvertSeis2PointSet: Survey not found")
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Convert Seismic to PointSet',
            #                                'Survey not found')
            return False
        return True

    def checkSeisData(self, f):
        self.refreshMsgBox()
        #
        return seis_ays.isSeis2DMatConsistentWithSeisInfo(self.seisdata[f], self.survinfo)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ConvertSeis2PointSet = QtWidgets.QWidget()
    gui = convertseis2pointset()
    gui.setupGUI(ConvertSeis2PointSet)
    ConvertSeis2PointSet.show()
    sys.exit(app.exec_())