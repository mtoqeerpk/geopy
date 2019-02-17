#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# Create a window for view pre-stack seismic


from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
import numpy as np
#
sys.path.append(os.path.dirname(__file__)[:-4])
from core.settings import settings as core_set
from psseismic.analysis import analysis as psseis_ays
from gui.plot2dpsseisshot import plot2dpsseisshot as gui_plot2dpsseisshot

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class viewpsseis(object):

    psseisname = ''
    psseisdata = {}
    plotstyle = core_set.Visual['Image']
    fontstyle = core_set.Visual['Font']
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ViewPsSeis):
        ViewPsSeis.setObjectName("ViewPsSeis")
        ViewPsSeis.setFixedSize(510, 460)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/psseismic.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ViewPsSeis.setWindowIcon(icon)
        #
        self.btnplot = QtWidgets.QPushButton(ViewPsSeis)
        self.btnplot.setObjectName("btnplot")
        self.btnplot.setGeometry(QtCore.QRect(410, 10, 80, 30))
        self.btnplot.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/gather.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnplot.setIcon(icon)
        self.twgpsseis = QtWidgets.QTableWidget(ViewPsSeis)
        self.twgpsseis.setObjectName("twgpsseis")
        self.twgpsseis.setGeometry(QtCore.QRect(10, 50, 480, 380))
        self.twgpsseis.setColumnCount(3)
        self.twgpsseis.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        #
        self.msgbox = QtWidgets.QMessageBox(ViewPsSeis)
        self.msgbox.setObjectName("msgbox")
        _center_x = ViewPsSeis.geometry().center().x()
        _center_y = ViewPsSeis.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ViewPsSeis)
        QtCore.QMetaObject.connectSlotsByName(ViewPsSeis)



    def retranslateGUI(self, ViewPsSeis):
        self.dialog = ViewPsSeis
        #
        _translate = QtCore.QCoreApplication.translate
        ViewPsSeis.setWindowTitle(_translate("ViewPsSeis", "View Pre-stack Seismic " +self.psseisname))
        self.btnplot.setText(_translate("ViewPsSeis", "Plot"))
        self.btnplot.clicked.connect(self.clickBtnPlot)
        self.twgpsseis.setColumnCount(8)
        self.twgpsseis.setHorizontalHeaderLabels(["Shot", "Valid Trace No.", "Missing Trace No.", "Sample No.", "Maximum", "Minimum", "Mean", "Std"])
        if self.checkPsSeis():
            # self.btncopy.setEnabled(True)
            self.btnplot.setEnabled(True)
            #
            _nrow = len(list(self.psseisdata.keys()))
            self.twgpsseis.setRowCount(_nrow)
            self.twgpsseis.verticalHeader().hide()
            _idx = 0
            for i in sorted(self.psseisdata.keys()):
                item = QtWidgets.QTableWidgetItem()
                item.setText(_translate("ViewPsSeis", i))
                item.setFlags(QtCore.Qt.ItemIsEditable)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgpsseis.setItem(_idx, 0, item)
                #
                item = QtWidgets.QTableWidgetItem()
                item.setText(_translate("ViewPsSeis", str(self.psseisdata[i]['ShotInfo']['TraceNum']
                                                          - len(self.psseisdata[i]['ShotInfo']['TraceMissing']))))
                item.setFlags(QtCore.Qt.ItemIsEditable)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgpsseis.setItem(_idx, 1, item)
                #
                item = QtWidgets.QTableWidgetItem()
                item.setText(_translate("ViewPsSeis", str(len(self.psseisdata[i]['ShotInfo']['TraceMissing']))))
                item.setFlags(QtCore.Qt.ItemIsEditable)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgpsseis.setItem(_idx, 2, item)
                #
                item = QtWidgets.QTableWidgetItem()
                item.setText(_translate("ViewPsSeis", str(self.psseisdata[i]['ShotInfo']['ZNum'])))
                item.setFlags(QtCore.Qt.ItemIsEditable)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgpsseis.setItem(_idx, 3, item)
                #
                _data = self.psseisdata[i]['ShotData']
                #
                item = QtWidgets.QTableWidgetItem()
                item.setText(_translate("ViewPsSeis", str(np.max(_data))))
                item.setFlags(QtCore.Qt.ItemIsEditable)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgpsseis.setItem(_idx, 4, item)
                #
                item = QtWidgets.QTableWidgetItem()
                item.setText(_translate("ViewPsSeis", str(np.min(_data))))
                item.setFlags(QtCore.Qt.ItemIsEditable)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgpsseis.setItem(_idx, 5, item)
                #
                item = QtWidgets.QTableWidgetItem()
                item.setText(_translate("ViewPsSeis", str(np.mean(_data))))
                item.setFlags(QtCore.Qt.ItemIsEditable)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgpsseis.setItem(_idx, 6, item)
                #
                item = QtWidgets.QTableWidgetItem()
                item.setText(_translate("ViewPsSeis", str(np.std(_data))))
                item.setFlags(QtCore.Qt.ItemIsEditable)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgpsseis.setItem(_idx, 7, item)
                #
                _idx = _idx + 1


    def clickBtnPlot(self):
        _plt = QtWidgets.QDialog()
        _gui = gui_plot2dpsseisshot()
        _gui.psseisdata = {}
        _gui.psseisdata[self.psseisname] = self.psseisdata
        _gui.plotstyle = self.plotstyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_plt)
        _plt.exec()
        _plt.show()


    def checkPsSeis(self):
        return psseis_ays.checkPsSeis(self.psseisdata)


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ViewPsSeis = QtWidgets.QWidget()
    gui = viewpsseis()
    gui.setupGUI(ViewPsSeis)
    ViewPsSeis.show()
    sys.exit(app.exec_())
