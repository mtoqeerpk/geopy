#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     August 2018                                                                     #
#                                                                                           #
#############################################################################################

# Create a window for filtering pointset based on properties


from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from basic.data import data as basic_data
from basic.matdict import matdict as basic_mdt

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class filterpointset(object):

    pointname = ''
    pointdata = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, FilterPointSet):
        FilterPointSet.setObjectName("FilterPointSet")
        FilterPointSet.setFixedSize(300, 420)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/filter.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        FilterPointSet.setWindowIcon(icon)
        #
        self.lblattrib = QtWidgets.QLabel(FilterPointSet)
        self.lblattrib.setObjectName("lblattrib")
        self.lblattrib.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lwgattrib = QtWidgets.QListWidget(FilterPointSet)
        self.lwgattrib.setObjectName("lwgattrib")
        self.lwgattrib.setGeometry(QtCore.QRect(10, 50, 280, 200))
        self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lblfilter = QtWidgets.QLabel(FilterPointSet)
        self.lblfilter.setObjectName("lblfilter")
        self.lblfilter.setGeometry(QtCore.QRect(90, 270, 60, 30))
        self.cbbfilter = QtWidgets.QComboBox(FilterPointSet)
        self.cbbfilter.setObjectName("cbbfilter")
        self.cbbfilter.setGeometry(QtCore.QRect(160, 270, 130, 30))
        self.lblvalue = QtWidgets.QLabel(FilterPointSet)
        self.lblvalue.setObjectName("lblvalue")
        self.lblvalue.setGeometry(QtCore.QRect(160, 310, 50, 30))
        self.ldtvalue = QtWidgets.QLineEdit(FilterPointSet)
        self.ldtvalue.setObjectName("ldtvalue")
        self.ldtvalue.setGeometry(QtCore.QRect(210, 310, 80, 30))
        self.btnapply = QtWidgets.QPushButton(FilterPointSet)
        self.btnapply.setObjectName("btnedit")
        self.btnapply.setGeometry(QtCore.QRect(100, 370, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(FilterPointSet)
        self.msgbox.setObjectName("msgbox")
        _center_x = FilterPointSet.geometry().center().x()
        _center_y = FilterPointSet.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(FilterPointSet)
        QtCore.QMetaObject.connectSlotsByName(FilterPointSet)


    def retranslateGUI(self, FilterPointSet):
        self.dialog = FilterPointSet
        #
        _translate = QtCore.QCoreApplication.translate
        FilterPointSet.setWindowTitle(_translate("FilterPointSet", "Filter PointSet " + self.pointname))
        self.lblattrib.setText(_translate("FilterPointSet", "List of available properties:"))
        self.lblfilter.setText(_translate("FilterPointSet", "Select filter:"))
        self.cbbfilter.addItems(['>= value', '<= value', '== value', '> value', '< value', '!= value'])
        self.cbbfilter.setCurrentIndex(2)
        self.lblvalue.setText(_translate("FilterPointSet", "value ="))
        self.ldtvalue.setText(_translate("FilterPointSet", ""))
        self.btnapply.setText(_translate("FilterPointSet", "Apply"))
        self.btnapply.clicked.connect(self.clickBtnApply)
        #
        self.refreshLwgAttrib()


    def clickBtnApply(self):
        self.refreshMsgBox()
        #
        _attriblist = self.lwgattrib.selectedItems()
        if len(_attriblist) < 1:
            print("FilterPointSet: No property selected for filtering")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Filter PointSet',
                                           'No property selected for filtering')
            return
        _value = basic_data.str2float(self.ldtvalue.text())
        if _value is False:
            print("FilterPointSet: Non-float value specified for filtering")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Filter PointSet',
                                           'Non-float value specified for filtering')
            return
        #
        _flag = '=='
        if self.cbbfilter.currentIndex() == 0:
            _flag = '>='
        if self.cbbfilter.currentIndex() == 1:
            _flag = '<='
        if self.cbbfilter.currentIndex() == 2:
            _flag = '=='
        if self.cbbfilter.currentIndex() == 3:
            _flag = '>'
        if self.cbbfilter.currentIndex() == 4:
            _flag = '<'
        if self.cbbfilter.currentIndex() == 5:
            _flag = '!='
        self.pointdata = basic_mdt.filterDictByValue(self.pointdata,
                                                     key=_attriblist[0].text(),
                                                     value=_value,
                                                     flag=_flag)
        #
        # QtWidgets.QMessageBox.information(self.msgbox,
        #                                   "Edit Seismic/PointSet",
        #                                   "Seismic/PointSet property edited successfully")
        self.dialog.close()
        return


    def refreshLwgAttrib(self):
        self.lwgattrib.clear()
        if len(self.pointdata.keys()) > 0:
            for i in sorted(self.pointdata.keys()):
                if i != "Inline" and i != "Crossline" and i != "Z":
                    item = QtWidgets.QListWidgetItem(self.lwgattrib)
                    item.setText(i)
                    self.lwgattrib.addItem(item)
            if "Inline" in self.pointdata.keys():
                item = QtWidgets.QListWidgetItem(self.lwgattrib)
                item.setText("Inline")
                self.lwgattrib.addItem(item)
            if "Crossline" in self.pointdata.keys():
                item = QtWidgets.QListWidgetItem(self.lwgattrib)
                item.setText("Crossline")
                self.lwgattrib.addItem(item)
            if "Z" in self.pointdata.keys():
                item = QtWidgets.QListWidgetItem(self.lwgattrib)
                item.setText("Z")
                self.lwgattrib.addItem(item)


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FilterPointSet = QtWidgets.QWidget()
    gui = filterpointset()
    gui.setupGUI(FilterPointSet)
    FilterPointSet.show()
    sys.exit(app.exec_())