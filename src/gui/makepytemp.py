#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# Create a window for creating python code template


from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


PyTemp = ["#############################################################################################\n",
          "#                                                                                           #\n",
          "# Template for GeoPy python compiler                                                        #\n",
          "#                                                                                           #\n",
          "# Note:                                                                                     #\n",
          "#       1. Must contains mainfunc of at least 4 args                                        #\n",
          "#       2. Add as many sub-functions as necessary                                           #\n",
          "#       3. Debug code first to avoid crashing                                               #\n",
          "#                                                                                           #\n",
          "#############################################################################################\n",
          "\n\n",
          "__all__ = ['mainfunc']\n",
          "\n\n",
          "def mainfunc(survinfo=None, seisdata=None, pointdata=None):\n",
          "    #\n",
          "    print('This is an template')\n",
          "    print('Check survey ...')\n",
          "    checkSurvInfo(survinfo)\n",
          "    print('Check seismic ...')\n",
          "    checkSeisData(seisdata)\n",
          "    print('Check point ...')\n",
          "    checkPointData(pointdata)\n",
          "    print('Call subfunc 1:')\n",
          "    subfunc1()\n",
          "    #\n",
          "    return survinfo, seisdata, pointdata\n",
          "\n\n",
          "def subfunc1(arg1=1, arg2='subfunc1', arg3=[1, 2, 3]):\n",
          "    print(arg1)\n",
          "    print(arg2)\n",
          "    print(len(arg3))\n",
          "\n\n",
          "def checkSurvInfo(survinfo):\n",
          "    if survinfo is None:\n",
          "        print('No survey found')\n",
          "    else:\n",
          "        print(survinfo)\n",
          "\n\n",
          "def checkSeisData(seisdata):\n",
          "    if seisdata is None:\n",
          "        print('No seismic found')\n",
          "    else:\n",
          "        print(seisdata.keys())\n",
          "\n\n",
          "def checkPointData(pointdata):\n",
          "    if pointdata is None:\n",
          "        print('No point found')\n",
          "    else:\n",
          "        print(pointdata.keys())"]


class makepytemp(object):

    rootpath = ''
    #
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, MakePyTemp):
        MakePyTemp.setObjectName("MakePyTemp")
        MakePyTemp.setFixedSize(400, 120)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/new.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        MakePyTemp.setWindowIcon(icon)
        self.lblfile = QtWidgets.QLabel(MakePyTemp)
        self.lblfile.setObjectName("lblfile")
        self.lblfile.setGeometry(QtCore.QRect(10, 10, 110, 30))
        self.ldtfile = QtWidgets.QLineEdit(MakePyTemp)
        self.ldtfile.setObjectName("ldtfile")
        self.ldtfile.setGeometry(QtCore.QRect(130, 10, 190, 30))
        self.btnfile = QtWidgets.QPushButton(MakePyTemp)
        self.btnfile.setObjectName("btnfile")
        self.btnfile.setGeometry(QtCore.QRect(330, 10, 60, 30))
        #
        self.btnapply = QtWidgets.QPushButton(MakePyTemp)
        self.btnapply.setObjectName("btnapply")
        self.btnapply.setGeometry(QtCore.QRect(120, 70, 160, 30))
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(MakePyTemp)
        self.msgbox.setObjectName("msgbox")
        _center_x = MakePyTemp.geometry().center().x()
        _center_y = MakePyTemp.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(MakePyTemp)
        QtCore.QMetaObject.connectSlotsByName(MakePyTemp)


    def retranslateGUI(self, MakePyTemp):
        self.dialog = MakePyTemp
        #
        _translate = QtCore.QCoreApplication.translate
        MakePyTemp.setWindowTitle(_translate("MakePyTemp", "Create Python Template"))
        self.lblfile.setText(_translate("MakePyTemp", "Select python code:"))
        self.lblfile.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtfile.setText(_translate("MakePyTemp", os.path.abspath(self.rootpath)))
        self.btnfile.setText(_translate("MakePyTemp", "Browse"))
        self.btnfile.clicked.connect(self.clickBtnFile)
        #
        self.btnapply.setText(_translate("MakePyTemp", "Create"))
        self.btnapply.clicked.connect(self.clickBtnMakePyTemp)


    def clickBtnFile(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Select Python Code', self.rootpath,
                                        filter="Python file (*.py);; All files (*.*)")
        if len(_file[0]) > 0:
            self.ldtfile.setText(_file[0])


    def clickBtnMakePyTemp(self):
        self.refreshMsgBox()
        #
        if os.path.exists(self.ldtfile.text()) and os.path.isfile(self.ldtfile.text()) is False:
            print("MakePyTemp: Directory is selected")
            QtWidgets.QMessageBox.critical(self.msgbox,
                                           'Create Python Template',
                                           'Directory is selected')
            return
        _file = open(self.ldtfile.text(), 'w')
        for s in PyTemp:
            _file.write(s)
        _file.close()
        #
        QtWidgets.QMessageBox.information(self.msgbox,
                                          "Create Template",
                                          "Template made successfully")
        return


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MakePyTemp = QtWidgets.QWidget()
    gui = makepytemp()
    gui.setupGUI(MakePyTemp)
    MakePyTemp.show()
    sys.exit(app.exec_())
