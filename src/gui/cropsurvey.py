#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# Create a window for cropping seismic survey


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4])
from seismic.analysis import analysis as seis_ays
from basic.data import data as basic_data
from basic.matdict import matdict as basic_mdt

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class cropsurvey(object):

    survinfo = {}
    seisdata = {}
    #
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, CropSurvey):
        CropSurvey.setObjectName("CropSurvey")
        CropSurvey.setFixedSize(480, 280)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/survey.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        CropSurvey.setWindowIcon(icon)
        self.lblsrvinfo = QtWidgets.QLabel(CropSurvey)
        self.lblsrvinfo.setObjectName("lblsrvinfo")
        self.lblsrvinfo.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lblstart = QtWidgets.QLabel(CropSurvey)
        self.lblstart.setObjectName("lblstart")
        self.lblstart.setGeometry(QtCore.QRect(120, 50, 80, 30))
        self.lblend = QtWidgets.QLabel(CropSurvey)
        self.lblend.setObjectName("lblend")
        self.lblend.setGeometry(QtCore.QRect(220, 50, 80, 30))
        self.lblstep = QtWidgets.QLabel(CropSurvey)
        self.lblstep.setObjectName("lblstep")
        self.lblstep.setGeometry(QtCore.QRect(320, 50, 40, 30))
        self.lblinl = QtWidgets.QLabel(CropSurvey)
        self.lblinl.setObjectName("lblinl")
        self.lblinl.setGeometry(QtCore.QRect(10, 90, 100, 30))
        self.lblxl = QtWidgets.QLabel(CropSurvey)
        self.lblxl.setObjectName("lblxl")
        self.lblxl.setGeometry(QtCore.QRect(10, 130, 100, 30))
        self.lblz = QtWidgets.QLabel(CropSurvey)
        self.lblz.setObjectName("lblz")
        self.lblz.setGeometry(QtCore.QRect(10, 170, 100, 30))
        self.ldtinlstart = QtWidgets.QLineEdit(CropSurvey)
        self.ldtinlstart.setObjectName("ldtinlstart")
        self.ldtinlstart.setGeometry(QtCore.QRect(120, 90, 80, 30))
        self.ldtinlend = QtWidgets.QLineEdit(CropSurvey)
        self.ldtinlend.setObjectName("ldtinlend")
        self.ldtinlend.setGeometry(QtCore.QRect(220, 90, 80, 30))
        self.ldtinlstep = QtWidgets.QLineEdit(CropSurvey)
        self.ldtinlstep.setObjectName("ldtinlstep")
        self.ldtinlstep.setGeometry(QtCore.QRect(320, 90, 40, 30))
        self.lblinlitvl = QtWidgets.QLabel(CropSurvey)
        self.lblinlitvl.setObjectName("lblinlitvl")
        self.lblinlitvl.setGeometry(QtCore.QRect(370, 90, 10, 30))
        self.cbbinlitvl = QtWidgets.QComboBox(CropSurvey)
        self.cbbinlitvl.setObjectName("cbbinlitvl")
        self.cbbinlitvl.setGeometry(QtCore.QRect(385, 90, 40, 30))
        self.ldtxlstart = QtWidgets.QLineEdit(CropSurvey)
        self.ldtxlstart.setObjectName("ldtxlstart")
        self.ldtxlstart.setGeometry(QtCore.QRect(120, 130, 80, 30))
        self.ldtxlend = QtWidgets.QLineEdit(CropSurvey)
        self.ldtxlend.setObjectName("ldtxlend")
        self.ldtxlend.setGeometry(QtCore.QRect(220, 130, 80, 30))
        self.ldtxlstep = QtWidgets.QLineEdit(CropSurvey)
        self.ldtxlstep.setObjectName("ldtxlstep")
        self.ldtxlstep.setGeometry(QtCore.QRect(320, 130, 40, 30))
        self.lblxlitvl = QtWidgets.QLabel(CropSurvey)
        self.lblxlitvl.setObjectName("lblxlitvl")
        self.lblxlitvl.setGeometry(QtCore.QRect(370, 130, 10, 30))
        self.cbbxlitvl = QtWidgets.QComboBox(CropSurvey)
        self.cbbxlitvl.setObjectName("cbbxlitvl")
        self.cbbxlitvl.setGeometry(QtCore.QRect(385, 130, 40, 30))
        self.ldtzstart = QtWidgets.QLineEdit(CropSurvey)
        self.ldtzstart.setObjectName("ldtzstart")
        self.ldtzstart.setGeometry(QtCore.QRect(120, 170, 80, 30))
        self.ldtzend = QtWidgets.QLineEdit(CropSurvey)
        self.ldtzend.setObjectName("ldtzend")
        self.ldtzend.setGeometry(QtCore.QRect(220, 170, 80, 30))
        self.ldtzstep = QtWidgets.QLineEdit(CropSurvey)
        self.ldtzstep.setObjectName("ldtzlstep")
        self.ldtzstep.setGeometry(QtCore.QRect(320, 170, 40, 30))
        self.lblzitvl = QtWidgets.QLabel(CropSurvey)
        self.lblzitvl.setObjectName("lblzitvl")
        self.lblzitvl.setGeometry(QtCore.QRect(370, 170, 10, 30))
        self.cbbzitvl = QtWidgets.QComboBox(CropSurvey)
        self.cbbzitvl.setObjectName("cbbzitvl")
        self.cbbzitvl.setGeometry(QtCore.QRect(385, 170, 40, 30))
        self.btnapply = QtWidgets.QPushButton(CropSurvey)
        self.btnapply.setObjectName("btnapply")
        self.btnapply.setGeometry(QtCore.QRect(190, 230, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(CropSurvey)
        self.msgbox.setObjectName("msgbox")
        _center_x = CropSurvey.geometry().center().x()
        _center_y = CropSurvey.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(CropSurvey)
        QtCore.QMetaObject.connectSlotsByName(CropSurvey)


    def retranslateGUI(self, CropSurvey):
        self.dialog = CropSurvey
        #
        _translate = QtCore.QCoreApplication.translate
        CropSurvey.setWindowTitle(_translate("CropSurvey", "Crop Survey"))
        self.lblsrvinfo.setText(_translate("CropSurvey", "Survey information:"))
        self.lblstart.setText(_translate("CropSurvey", "Start"))
        self.lblstart.setAlignment(QtCore.Qt.AlignCenter)
        self.lblend.setText(_translate("CropSurvey", "End"))
        self.lblend.setAlignment(QtCore.Qt.AlignCenter)
        self.lblstep.setText(_translate("CropSurvey", "Step"))
        self.lblstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblinl.setText(_translate("CropSurvey", "Inline:"))
        self.lblinl.setAlignment(QtCore.Qt.AlignRight)
        self.lblxl.setText(_translate("CropSurvey", "Crossline:"))
        self.lblxl.setAlignment(QtCore.Qt.AlignRight)
        self.lblz.setText(_translate("CropSurvey", "Time/depth:"))
        self.lblz.setAlignment(QtCore.Qt.AlignRight)
        self.ldtinlstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtinlend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtinlstep.setEnabled(False)
        self.ldtinlstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblinlitvl.setText(_translate("CropSurvey", "X"))
        self.cbbinlitvl.addItems([str(i+1) for i in range(100)])
        self.ldtxlstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlstep.setEnabled(False)
        self.ldtxlstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblxlitvl.setText(_translate("CropSurvey", "X"))
        self.cbbxlitvl.addItems([str(i + 1) for i in range(100)])
        self.ldtzstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtzend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtzstep.setEnabled(False)
        self.ldtzstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblzitvl.setText(_translate("CropSurvey", "X"))
        self.cbbzitvl.addItems([str(i + 1) for i in range(100)])
        #
        if (self.checkSurvInfo() is True) and (self.checkSeisData() is True):
            _survinfo = self.survinfo
            self.ldtinlstart.setText(_translate("CropSurvey", str(_survinfo['ILStart'])))
            self.ldtinlend.setText(_translate("CropSurvey", str(_survinfo['ILEnd'])))
            self.ldtinlstep.setText(_translate("CropSurvey", str(_survinfo['ILStep'])))
            self.ldtxlstart.setText(_translate("CropSurvey", str(_survinfo['XLStart'])))
            self.ldtxlend.setText(_translate("CropSurvey", str(_survinfo['XLEnd'])))
            self.ldtxlstep.setText(_translate("CropSurvey", str(_survinfo['XLStep'])))
            self.ldtzstart.setText(_translate("CropSurvey", str(_survinfo['ZStart'])))
            self.ldtzend.setText(_translate("CropSurvey", str(_survinfo['ZEnd'])))
            self.ldtzstep.setText(_translate("CropSurvey", str(_survinfo['ZStep'])))
        #
        self.btnapply.setText(_translate("CropSurvey", "Apply"))
        self.btnapply.clicked.connect(self.clickBtnApply)


    def clickBtnApply(self):
        self.refreshMsgBox()
        #
        if self.checkSurvInfo() is False:
            print("CropSurvey: No seismic survey found")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Crop Survey',
                                           'No seismic survey found')
            return
        #
        _inlstart = basic_data.str2int(self.ldtinlstart.text())
        _xlstart = basic_data.str2int(self.ldtxlstart.text())
        _zstart = basic_data.str2int(self.ldtzstart.text())
        _inlend = basic_data.str2int(self.ldtinlend.text())
        _xlend = basic_data.str2int(self.ldtxlend.text())
        _zend = basic_data.str2int(self.ldtzend.text())
        if _inlstart is False or _xlstart is False or _zstart is False \
                or _inlend is False or _xlend is False or _zend is False:
            print("CropSurvey: Non-integer survey selection")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Crop Survey',
                                           'Non-integer survey selection')
            return
        #
        _survinfo = self.survinfo
        #
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
        _inlidx = np.arange(_inlstart_idx, _inlend_idx+1,
                            self.cbbinlitvl.currentIndex()+1, dtype=int)
        _xlidx = np.arange(_xlstart_idx, _xlend_idx+1,
                           self.cbbxlitvl.currentIndex() + 1, dtype=int)
        _zidx = np.arange(_zstart_idx, _zend_idx+1,
                          self.cbbzitvl.currentIndex() + 1, dtype=int)
        _idx = np.zeros([len(_inlidx), len(_xlidx), len(_zidx)])
        # survinfo
        self.survinfo = seis_ays.createSeisInfoFrom3DMat(np.transpose(_idx, [2, 1, 0]),
                                                         inlstart=_inlstart_idx*_survinfo['ILStep']+_survinfo['ILStart'],
                                                         inlstep=(self.cbbinlitvl.currentIndex()+1)*_survinfo['ILStep'],
                                                         xlstart=_xlstart_idx*_survinfo['XLStep']+_survinfo['XLStart'],
                                                         xlstep=(self.cbbxlitvl.currentIndex()+1)*_survinfo['XLStep'],
                                                         zstart=_zstart_idx*_survinfo['ZStep']+_survinfo['ZStart'],
                                                         zstep=(self.cbbzitvl.currentIndex()+1)*_survinfo['ZStep'])
        # seisdata
        for i in range(len(_inlidx)):
            for j in range(len(_xlidx)):
                _idx[i, j, :] = _zidx + _xlidx[j] * _survinfo['ZNum'] + _inlidx[i] * _survinfo['XLNum'] * _survinfo['ZNum']
        _idx = np.reshape(_idx, [len(_zidx) * len(_xlidx) * len(_inlidx)])
        if (self.seisdata is not None) and len(self.seisdata.keys()) > 0:
            self.seisdata = basic_mdt.retrieveDictByIndex(self.seisdata, _idx)
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Crop Survey",
                                          "Survey cropped successfully")
        #
        self.dialog.close()


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))

    def checkSurvInfo(self):
        self.refreshMsgBox()
        #
        if seis_ays.checkSeisInfo(self.survinfo) is False:
            # print("CropSurvey: Survey not found")
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Crop Survey',
            #                                'Survey not found')
            return False
        return True

    def checkSeisData(self):
        self.refreshMsgBox()
        #
        for f in self.seisdata.keys():
            if np.shape(self.seisdata[f])[0] != self.survinfo['SampleNum']:
                # print("CropSurvey: Seismic & survey not match")
                # QtWidgets.QMessageBox.critical(self.msgbox,
                #                                'Crop Survey',
                #                                'Seismic & survey not match')
                return False
        return True


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    CropSurvey = QtWidgets.QWidget()
    gui = cropsurvey()
    gui.setupGUI(CropSurvey)
    CropSurvey.show()
    sys.exit(app.exec_())
