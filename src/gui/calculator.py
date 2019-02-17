#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# Create a window for editing seismic/pointset properties


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from basic.data import data as basic_data

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class calculator(object):

    data = {}
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, Calculator):
        Calculator.setObjectName("Calculator")
        Calculator.setFixedSize(250, 140)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/math.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        Calculator.setWindowIcon(icon)
        #
        self.lbloperator = QtWidgets.QLabel(Calculator)
        self.lbloperator.setObjectName("lbloperator")
        self.lbloperator.setGeometry(QtCore.QRect(10, 10, 80, 30))
        self.cbboperator = QtWidgets.QComboBox(Calculator)
        self.cbboperator.setObjectName("cbboperator")
        self.cbboperator.setGeometry(QtCore.QRect(100, 10, 140, 30))
        self.lblvalue = QtWidgets.QLabel(Calculator)
        self.lblvalue.setObjectName("lblvalue")
        self.lblvalue.setGeometry(QtCore.QRect(100, 50, 60, 30))
        self.ldtvalue = QtWidgets.QLineEdit(Calculator)
        self.ldtvalue.setObjectName("ldtvalue")
        self.ldtvalue.setGeometry(QtCore.QRect(170, 50, 70, 30))
        self.btnapply = QtWidgets.QPushButton(Calculator)
        self.btnapply.setObjectName("btnapply")
        self.btnapply.setGeometry(QtCore.QRect(75, 90, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(Calculator)
        self.msgbox.setObjectName("msgbox")
        _center_x = Calculator.geometry().center().x()
        _center_y = Calculator.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(Calculator)
        QtCore.QMetaObject.connectSlotsByName(Calculator)


    def retranslateGUI(self, Calculator):
        self.dialog = Calculator
        #
        _translate = QtCore.QCoreApplication.translate
        Calculator.setWindowTitle(_translate("Calculator", "Calculator"))
        self.lbloperator.setText(_translate("Calculator", "Select operator:"))
        self.cbboperator.addItems(['Assign (x=v)', 'Add (x+v)', 'Multipy (x*v)', 'Inverse (1/x)',
                                   'Opposite (-x)', 'Absolute(x)', 'Round(x)',
                                   'Normalize'])
        self.cbboperator.currentIndexChanged.connect(self.changeCbbOperator)
        self.lblvalue.setText(_translate("Calculator", "Value (v) ="))
        self.ldtvalue.setText(_translate("Calculator", ""))
        self.ldtvalue.setVisible(True)
        self.btnapply.setText(_translate("Calculator", "Apply"))
        self.btnapply.clicked.connect(self.clickBtnApply)


    def changeCbbOperator(self):
        if self.cbboperator.currentIndex() <= 2:
            self.lblvalue.setVisible(True)
            self.ldtvalue.setVisible(True)
        else:
            self.lblvalue.setVisible(False)
            self.ldtvalue.setText('')
            self.ldtvalue.setVisible(False)


    def clickBtnApply(self):
        self.refreshMsgBox()
        #
        if type(self.data) is not np.ndarray or np.shape(self.data)[0] < 1:
            print("Calculator: No NumPy data added into calculator")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Calculator',
                                           'No NumPy data added into calculator')
            return
        #
        if self.cbboperator.currentIndex() < 3:
            _value = basic_data.str2float(self.ldtvalue.text())
            if _value is False:
                print("Calculator: Non-float value")
                QtWidgets.QMessageBox.critical(self.msgbox,
                                               'Calculator',
                                               'Non-float value')
                return
        #
        if self.cbboperator.currentIndex() == 0:
            self.data = self.data * 0.0 + _value
        if self.cbboperator.currentIndex() == 1:
            self.data = self.data + _value
        if self.cbboperator.currentIndex() == 2:
            self.data = self.data * _value
        if self.cbboperator.currentIndex() == 3:
            self.data = np.reciprocal(self.data)
        if self.cbboperator.currentIndex() == 4:
            self.data = - self.data
        if self.cbboperator.currentIndex() == 5:
            self.data = np.abs(self.data)
        if self.cbboperator.currentIndex() == 6:
            self.data = np.round(self.data)
        if self.cbboperator.currentIndex() == 7:
            _vmin = np.min(self.data)
            _vmax = np.max(self.data)
            if _vmax > _vmin:
                self.data = (self.data -_vmin) / (_vmax-_vmin)
        #
        # QtWidgets.QMessageBox.information(self.msgbox,
        #                                   "Calculator",
        #                                   "Data calculated successfully")
        self.dialog.close()
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Calculator = QtWidgets.QWidget()
    gui = calculator()
    gui.setupGUI(Calculator)
    Calculator.show()
    sys.exit(app.exec_())
