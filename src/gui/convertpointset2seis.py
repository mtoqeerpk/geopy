#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# Create a window for converting point sets to seismic


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from basic.data import data as basic_data
from basic.matdict import matdict as basic_mdt
from pointset.analysis import analysis as point_ays
from seismic.analysis import analysis as seis_ays

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class convertpointset2seis(object):

    survinfo = {}
    seisdata = {}
    pointdata = {}
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ConvertPointSet2Seis):
        ConvertPointSet2Seis.setObjectName("ConvertPointSet2Seis")
        ConvertPointSet2Seis.setFixedSize(400, 410)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ConvertPointSet2Seis.setWindowIcon(icon)
        #
        self.lblpoint = QtWidgets.QLabel(ConvertPointSet2Seis)
        self.lblpoint.setObjectName("lblpoint")
        self.lblpoint.setGeometry(QtCore.QRect(10, 10, 170, 30))
        self.lwgpoint = QtWidgets.QListWidget(ConvertPointSet2Seis)
        self.lwgpoint.setObjectName("lwgpoint")
        self.lwgpoint.setGeometry(QtCore.QRect(10, 50, 170, 200))
        self.lwgpoint.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.lblarrow = QtWidgets.QLabel(ConvertPointSet2Seis)
        self.lblarrow.setObjectName("lblarrow")
        self.lblarrow.setGeometry(QtCore.QRect(180, 110, 40, 30))
        self.lblattrib = QtWidgets.QLabel(ConvertPointSet2Seis)
        self.lblattrib.setObjectName("lblattrib")
        self.lblattrib.setGeometry(QtCore.QRect(220, 10, 170, 30))
        self.lwgattrib = QtWidgets.QListWidget(ConvertPointSet2Seis)
        self.lwgattrib.setObjectName("lwgattrib")
        self.lwgattrib.setGeometry(QtCore.QRect(220, 50, 170, 200))
        self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.lblvalue = QtWidgets.QLabel(ConvertPointSet2Seis)
        self.lblvalue.setObjectName("lblvalue")
        self.lblvalue.setGeometry(QtCore.QRect(220, 270, 80, 30))
        self.ldtvalue = QtWidgets.QLineEdit(ConvertPointSet2Seis)
        self.ldtvalue.setObjectName("ldtvalue")
        self.ldtvalue.setGeometry(QtCore.QRect(310, 270, 80, 30))
        self.lbloverlap = QtWidgets.QLabel(ConvertPointSet2Seis)
        self.lbloverlap.setObjectName("lbloverlap")
        self.lbloverlap.setGeometry(QtCore.QRect(220, 310, 80, 30))
        self.cbboverlap = QtWidgets.QComboBox(ConvertPointSet2Seis)
        self.cbboverlap.setObjectName("cbboverlap")
        self.cbboverlap.setGeometry(QtCore.QRect(310, 310, 80, 30))
        self.btnapply = QtWidgets.QPushButton(ConvertPointSet2Seis)
        self.btnapply.setObjectName("btnedit")
        self.btnapply.setGeometry(QtCore.QRect(150, 360, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ConvertPointSet2Seis)
        self.msgbox.setObjectName("msgbox")
        _center_x = ConvertPointSet2Seis.geometry().center().x()
        _center_y = ConvertPointSet2Seis.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ConvertPointSet2Seis)
        QtCore.QMetaObject.connectSlotsByName(ConvertPointSet2Seis)


    def retranslateGUI(self, ConvertPointSet2Seis):
        self.dialog = ConvertPointSet2Seis
        #
        _translate = QtCore.QCoreApplication.translate
        ConvertPointSet2Seis.setWindowTitle(_translate("ConvertPointSet2Seis", "Convert PointSet to Seismic"))
        self.lblpoint.setText(_translate("ConvertPointSet2Seis", "Select pointsets:"))
        self.lwgpoint.itemSelectionChanged.connect(self.changeLwgPoint)
        self.lblarrow.setText(_translate("ConvertPointSet2Seis", "==>"))
        self.lblarrow.setAlignment(QtCore.Qt.AlignCenter)
        self.lblattrib.setText(_translate("ConvertPointSet2Seis", "Select properties:"))
        self.lblvalue.setText(_translate("ConvertPointSet2Seis", "Undefined value:"))
        self.ldtvalue.setText(_translate("ConvertPointSet2Seis", "-999"))
        self.lbloverlap.setText(_translate("ConvertPointSet2Seis", "Overlap points:"))
        self.cbboverlap.addItems(['Sum', 'Average', 'Maximum', 'Minimum'])
        self.btnapply.setText(_translate("ConvertPointSet2Seis", "Apply"))
        self.btnapply.clicked.connect(self.clickBtnApply)
        #
        self.lwgpoint.clear()
        if len(self.pointdata.keys()) > 0:
            for i in sorted(self.pointdata.keys()):
                if self.checkPointSet(i):
                    item = QtWidgets.QListWidgetItem(self.lwgpoint)
                    item.setText(i)
                    self.lwgpoint.addItem(item)


    def changeLwgPoint(self):
        self.lwgattrib.clear()
        _firstattrib = None
        #
        _pointlist = self.lwgpoint.selectedItems()
        _pointlist = [f.text() for f in _pointlist]
        if len(_pointlist) > 0:
            for _k in self.pointdata[_pointlist[0]].keys():
                _flag = True
                for _i in range(len(_pointlist)):
                    if _k not in self.pointdata[_pointlist[_i]].keys():
                        _flag = False
                        break
                if _flag is True\
                        and _k != 'Inline' and _k != 'Crossline' and _k != 'Z':
                    item = QtWidgets.QListWidgetItem(self.lwgattrib)
                    item.setText(_k)
                    self.lwgpoint.addItem(item)
                    if _firstattrib is None:
                        _firstattrib = item
        if _firstattrib is not None:
            self.lwgattrib.setCurrentItem(_firstattrib)


    def clickBtnApply(self):
        self.refreshMsgBox()
        #
        _pointlist = self.lwgpoint.selectedItems()
        _pointlist = [f.text() for f in _pointlist]
        if len(_pointlist) < 1:
            print("ConvertPointSet2Seis: No pointset selected for conversion")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Convert PointSet to Seismic',
                                           'No pointset selected for conversion')
            return
        #
        _attriblist = self.lwgattrib.selectedItems()
        _attriblist = [f.text() for f in _attriblist]
        if len(_attriblist) < 1:
            print("ConvertPointSet2Seis: No property selected for conversion")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                            'Convert PointSet to Seismic',
                                            'No property selected for conversion')
            return
        #
        if basic_data.str2float(self.ldtvalue.text()) is False:
            print("ConvertPointSet2Seis: Non-float undefined value")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Convert PointSet to Seismic',
                                           'Non-float undefined value')
            return
        #
        if (self.checkSurvInfo() is False) and (self.checkSeisData() is False):
            print("ConvertPointSet2Seis: No seismic survey found for conversion")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Convert PointSet to Seismic',
                                           'No seismic survey found for conversion')
            return
        #
        _survinfo = self.survinfo
        for _f in _attriblist:
            _seisdata = np.zeros([_survinfo['ZNum'], _survinfo['XLNum'], _survinfo['ILNum']]) + float(self.ldtvalue.text())
            for _p in _pointlist:
                _pointdata = basic_mdt.exportMatDict(self.pointdata[_p], ['Inline', 'Crossline', 'Z', _f])
                _pointdata = seis_ays.removeOutofSurveySample(_pointdata,
                                                              inlstart=_survinfo['ILStart'], inlend=_survinfo['ILEnd'],
                                                              xlstart=_survinfo['XLStart'], xlend=_survinfo['XLEnd'],
                                                              zstart=_survinfo['ZStart'], zend=_survinfo['ZEnd'])
                if np.shape(_pointdata)[0] < 1:
                    continue
                _ijk = seis_ays.convertIXZToIJK(_pointdata,
                                                inlstart=_survinfo['ILStart'], inlstep=_survinfo['ILStep'],
                                                xlstart=_survinfo['XLStart'], xlstep=_survinfo['XLStep'],
                                                zstart=_survinfo['ZStart'], zstep=_survinfo['ZStep'])
                for _i in range(np.shape(_ijk)[0]):
                    _ijk_i = int(_ijk[_i, 0])
                    _ijk_j = int(_ijk[_i, 1])
                    _ijk_k = int(_ijk[_i, 2])
                    _data = _seisdata[_ijk_k, _ijk_j, _ijk_i]
                    if float(_data) == float(self.ldtvalue.text()):
                        _seisdata[_ijk_k, _ijk_j, _ijk_i] = _pointdata[_i, 3]
                    else:
                        if self.cbboverlap.currentIndex() == 0:
                            _seisdata[_ijk_k, _ijk_j, _ijk_i] = _pointdata[_i, 3] + _data
                        if self.cbboverlap.currentIndex() == 1:
                            _seisdata[_ijk_k, _ijk_j, _ijk_i] = 0.5 * (_pointdata[_i, 3] + _data)
                        if self.cbboverlap.currentIndex() == 2:
                            _seisdata[_ijk_k, _ijk_j, _ijk_i] = np.max([_pointdata[_i, 3], _data])
                        if self.cbboverlap.currentIndex() == 3:
                            _seisdata[_ijk_k, _ijk_j, _ijk_i] = np.min([_pointdata[_i, 3], _data])

            self.seisdata[_f] = np.reshape(np.transpose(_seisdata, [2, 1, 0]), [-1, 1])
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Convert PointSet to Seismic",
                                          "PointSet converted successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkPointSet(self, name):
        return point_ays.checkPoint(self.pointdata[name])


    def checkSurvInfo(self):
        self.refreshMsgBox()
        #
        if seis_ays.checkSeisInfo(self.survinfo) is False:
            # print("ConvertPointSet2Seis: Survey not found")
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Convert PointSet to Seismic',
            #                                'Survey not found')
            return False
        return True


    def checkSeisData(self):
        self.refreshMsgBox()
        #
        for f in self.seisdata.keys():
            if np.shape(self.seisdata[f])[0] != self.survinfo['SampleNum']:
                # print("ConvertPointSet2Seis: Seismic & survey not match")
                # QtWidgets.QMessageBox.critical(self.msgbox,
                #                                'Convert PointSet to Seismic',
                #                                'Seismic & survey not match')
                return False
        return True


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConvertPointSet2Seis = QtWidgets.QWidget()
    gui = convertpointset2seis()
    gui.setupGUI(ConvertPointSet2Seis)
    ConvertPointSet2Seis.show()
    sys.exit(app.exec_())
