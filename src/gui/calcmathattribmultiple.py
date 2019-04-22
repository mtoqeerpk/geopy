#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for calculating seismic attribute (math) (multi properties)


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from seismic.analysis import analysis as seis_ays

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class calcmathattribmultiple(object):

    survinfo = {}
    seisdata = {}
    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None
    #
    mathattriblist = ['+', '-', '*', '/']


    def setupGUI(self, CalcMathAttribMultiple):
        CalcMathAttribMultiple.setObjectName("CalcMathAttribMultiple")
        CalcMathAttribMultiple.setFixedSize(500, 380)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/file.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        CalcMathAttribMultiple.setWindowIcon(icon)
        #
        self.lblproperty1 = QtWidgets.QLabel(CalcMathAttribMultiple)
        self.lblproperty1.setObjectName("lblproperty1")
        self.lblproperty1.setGeometry(QtCore.QRect(10, 10, 200, 30))
        self.lwgproperty1 = QtWidgets.QListWidget(CalcMathAttribMultiple)
        self.lwgproperty1.setObjectName("lwgproperty1")
        self.lwgproperty1.setGeometry(QtCore.QRect(10, 50, 200, 200))
        self.lwgproperty1.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lblproperty2 = QtWidgets.QLabel(CalcMathAttribMultiple)
        self.lblproperty2.setObjectName("lblproperty2")
        self.lblproperty2.setGeometry(QtCore.QRect(290, 10, 200, 30))
        self.lwgproperty2 = QtWidgets.QListWidget(CalcMathAttribMultiple)
        self.lwgproperty2.setObjectName("lwgproperty2")
        self.lwgproperty2.setGeometry(QtCore.QRect(290, 50, 200, 200))
        self.lwgproperty2.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.cbbattrib = QtWidgets.QComboBox(CalcMathAttribMultiple)
        self.cbbattrib.setObjectName("cbbattrib")
        self.cbbattrib.setGeometry(QtCore.QRect(230, 135, 40, 30))
        self.lblname = QtWidgets.QLabel(CalcMathAttribMultiple)
        self.lblname.setObjectName("lblname")
        self.lblname.setGeometry(QtCore.QRect(310, 270, 80, 30))
        self.ldtname = QtWidgets.QLineEdit(CalcMathAttribMultiple)
        self.ldtname.setObjectName("ldtname")
        self.ldtname.setGeometry(QtCore.QRect(390, 270, 100, 30))
        self.btnapply = QtWidgets.QPushButton(CalcMathAttribMultiple)
        self.btnapply.setObjectName("btnapply")
        self.btnapply.setGeometry(QtCore.QRect(200, 330, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(CalcMathAttribMultiple)
        self.msgbox.setObjectName("msgbox")
        _center_x = CalcMathAttribMultiple.geometry().center().x()
        _center_y = CalcMathAttribMultiple.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(CalcMathAttribMultiple)
        QtCore.QMetaObject.connectSlotsByName(CalcMathAttribMultiple)


    def retranslateGUI(self, CalcMathAttribMultiple):
        self.dialog = CalcMathAttribMultiple
        #
        _translate = QtCore.QCoreApplication.translate
        CalcMathAttribMultiple.setWindowTitle(_translate("CalcMathAttribMultiple", "Calculate Math Attribute between Properties"))
        self.lblproperty1.setText(_translate("CalcMathAttribMultiple", "Select property 1:"))
        self.lblproperty2.setText(_translate("CalcMathAttribMultiple", "Select property 2:"))
        self.cbbattrib.addItems(self.mathattriblist)
        self.cbbattrib.currentIndexChanged.connect(self.changeCbbAttrib)
        self.lblname.setText(_translate("CalcMathAttribMultiple", "Output name:"))
        self.ldtname.setText(_translate("CalcMathAttribMultiple", "Add"))
        self.btnapply.setText(_translate("CalcMathAttribMultiple", "Apply"))
        self.btnapply.clicked.connect(self.clickBtnCalcMathAttribMultiple)
        #
        self.refreshLwgProperty(self.lwgproperty1)
        self.refreshLwgProperty(self.lwgproperty2)


    def changeCbbAttrib(self):
        if self.cbbattrib.currentIndex() == 0:
            self.ldtname.setText('Add')
        if self.cbbattrib.currentIndex() == 1:
            self.ldtname.setText('Subtract')
        if self.cbbattrib.currentIndex() == 2:
            self.ldtname.setText('Multiply')
        if self.cbbattrib.currentIndex() == 4:
            self.ldtname.setText('Divide')


    def clickBtnCalcMathAttribMultiple(self):
        self.refreshMsgBox()
        #
        _property1 = self.lwgproperty1.selectedItems()
        if len(_property1) < 1:
            print("CalcMathAttribMultiple: No property 1 selected for attribute analysis")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Calculate Math Attribute between Properties',
                                           'No property 1 selected for attribute analysis')
            return
        _property2 = self.lwgproperty2.selectedItems()
        if len(_property2) < 1:
            print("CalcMathAttribMultiple: No property 2 selected for attribute analysis")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Calculate Math Attribute between Properties',
                                           'No property 2 selected for attribute analysis')
            return
        if len(self.ldtname.text()) < 1:
            print("CalcMathAttribMultiple: No name specified for output attribute")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Calculate Math Attribute between Properties',
                                           'No name specified for output attribute')
            return
        if self.ldtname.text() in self.seisdata.keys():
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Calculate Math Attribute between Properties',
                                                   self.ldtname.text() + ' already exists. Overwrite?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return
        #
        _seisdata1 = self.seisdata[_property1[0].text()]
        _seisdata2 = self.seisdata[_property2[0].text()]
        #
        if self.cbbattrib.currentIndex() == 0:
            self.seisdata[self.ldtname.text()] = np.add(_seisdata1, _seisdata2)
        if self.cbbattrib.currentIndex() == 1:
            self.seisdata[self.ldtname.text()] = np.subtract(_seisdata1, _seisdata2)
        if self.cbbattrib.currentIndex() == 2:
            self.seisdata[self.ldtname.text()] = np.multiply(_seisdata1, _seisdata2)
        if self.cbbattrib.currentIndex() == 3:
            self.seisdata[self.ldtname.text()] = np.divide(_seisdata1, _seisdata2)
        #
        self.refreshLwgProperty(self.lwgproperty1)
        self.refreshLwgProperty(self.lwgproperty2)
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Calculate Math Attribute between Properties",
                                          "Math attribute " + self.mathattriblist[self.cbbattrib.currentIndex()] + " calculated successfully")
        return


    def refreshLwgProperty(self, lwgproperty):
        lwgproperty.clear()
        if self.checkSurvInfo() is True:
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i) is True:
                    item = QtWidgets.QListWidgetItem(lwgproperty)
                    item.setText(i)
                    lwgproperty.addItem(item)


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


    def checkSurvInfo(self):
        self.refreshMsgBox()
        #
        if seis_ays.checkSeisInfo(self.survinfo) is False:
            # print("CalcMathAttribSingle: Survey not found")
            # QtWidgets.QMessageBox.critical(self.msgbox,
            #                                'Calculate Math Attribute from Single Property',
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
    CalcMathAttribMultiple = QtWidgets.QWidget()
    gui = calcmathattribmultiple()
    gui.setupGUI(CalcMathAttribMultiple)
    CalcMathAttribMultiple.show()
    sys.exit(app.exec_())