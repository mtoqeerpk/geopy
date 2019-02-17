#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     August 2018                                                                     #
#                                                                                           #
#############################################################################################

# Create a window for view point sets


from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from basic.matdict import matdict as basic_mdt
from core.settings import settings as core_set
from pointset.analysis import analysis as point_ays
from gui.plot2dpointsetcrossplt import plot2dpointsetcrossplt as gui_plot2dpointsetcrossplt

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class viewpointset(object):

    pointname = ''
    pointdata = {}
    linestyle = core_set.Visual['Line']
    fontstyle = core_set.Visual['Font']
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ViewPointSet):
        ViewPointSet.setObjectName("ViewPointSet")
        ViewPointSet.setFixedSize(510, 460)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/point.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ViewPointSet.setWindowIcon(icon)
        #
        self.btncopy = QtWidgets.QPushButton(ViewPointSet)
        self.btncopy.setObjectName("btncopy")
        self.btncopy.setGeometry(QtCore.QRect(310, 10, 80, 30))
        self.btncopy.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/copy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btncopy.setIcon(icon)
        self.btnplot = QtWidgets.QPushButton(ViewPointSet)
        self.btnplot.setObjectName("btnplot")
        self.btnplot.setGeometry(QtCore.QRect(410, 10, 80, 30))
        self.btnplot.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/plotpoint.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnplot.setIcon(icon)
        self.twgpoint = QtWidgets.QTableWidget(ViewPointSet)
        self.twgpoint.setObjectName("twgpoint")
        self.twgpoint.setGeometry(QtCore.QRect(10, 50, 480, 380))
        self.twgpoint.setColumnCount(3)
        self.twgpoint.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        #
        self.msgbox = QtWidgets.QMessageBox(ViewPointSet)
        self.msgbox.setObjectName("msgbox")
        _center_x = ViewPointSet.geometry().center().x()
        _center_y = ViewPointSet.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ViewPointSet)
        QtCore.QMetaObject.connectSlotsByName(ViewPointSet)



    def retranslateGUI(self, ViewPointSet):
        self.dialog = ViewPointSet
        #
        _translate = QtCore.QCoreApplication.translate
        ViewPointSet.setWindowTitle(_translate("ViewPointSet", "View PointSet " +self.pointname))
        self.btncopy.setText(_translate("ViewPointSet", "Copy"))
        self.btncopy.clicked.connect(self.clickBtnCopy)
        self.btnplot.setText(_translate("ViewPointSet", "Plot"))
        self.btnplot.clicked.connect(self.clickBtnPlot)
        if self.checkPointSet():
            # self.btncopy.setEnabled(True)
            self.btnplot.setEnabled(True)
            #
            _nrow = basic_mdt.maxDictConstantRow(self.pointdata)
            _ncol = len(self.pointdata.keys())
            self.twgpoint.setRowCount(_nrow)
            self.twgpoint.setColumnCount(_ncol)
            _colheader = [key for key in self.pointdata.keys()]
            self.twgpoint.setHorizontalHeaderLabels(_colheader)
            # self.twgpoint.verticalHeader().hide()
            for i in range(_nrow):
                for j in range(_ncol):
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(_translate("ViewPointSet", str(self.pointdata[_colheader[j]][i, 0])))
                    item.setFlags(QtCore.Qt.ItemIsEditable)
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.twgpoint.setItem(i, j, item)


    def clickBtnCopy(self):
        self.refreshMsgBox()
        #
        _s = ""
        for i in range(self.twgpoint.rowCount()):
            for j in range(self.twgpoint.columnCount()):
                _s = _s + self.twgpoint.item(i,j).text() + '\t'
            _s = _s + '\n'
        QtGui.QGuiApplication.clipboard().setText(_s)
        if len(_s) > 0:
            QtWidgets.QMessageBox.information(self.msgbox,
                                              "View PointSet",
                                              str(len(_s)) + " points copied to clipboard")


    def clickBtnPlot(self):
        _cplt = QtWidgets.QDialog()
        _gui = gui_plot2dpointsetcrossplt()
        _gui.pointdata = {}
        _gui.pointdata[self.pointname] = self.pointdata
        _gui.linestyle = self.linestyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_cplt)
        _cplt.exec()
        _cplt.show()


    def checkPointSet(self):
        return point_ays.checkPoint(self.pointdata)


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ViewPointSet = QtWidgets.QWidget()
    gui = viewpointset()
    gui.setupGUI(ViewPointSet)
    ViewPointSet.show()
    sys.exit(app.exec_())