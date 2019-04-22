#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for viewing seg-y textual header


from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from seismic.inputoutput import inputoutput as seis_io

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class viewsegytextualheader(object):

    segyfile = ""
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ViewSegyTextualHeader):
        ViewSegyTextualHeader.setObjectName("ViewSegyTextualHeader")
        ViewSegyTextualHeader.setFixedSize(560, 460)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ViewSegyTextualHeader.setWindowIcon(icon)
        #
        self.lblhelp = QtWidgets.QLabel(ViewSegyTextualHeader)
        self.lblhelp.setObjectName("lblhelp")
        self.lblhelp.setGeometry(QtCore.QRect(460, 10, 80, 30))
        self.lwgheader = QtWidgets.QListWidget(ViewSegyTextualHeader)
        self.lwgheader.setObjectName("lwgheader")
        self.lwgheader.setGeometry(QtCore.QRect(10, 50, 530, 380))
        self.lwgheader.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        #
        self.msgbox = QtWidgets.QMessageBox(ViewSegyTextualHeader)
        self.msgbox.setObjectName("msgbox")
        _center_x = ViewSegyTextualHeader.geometry().center().x()
        _center_y = ViewSegyTextualHeader.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ViewSegyTextualHeader)
        QtCore.QMetaObject.connectSlotsByName(ViewSegyTextualHeader)



    def retranslateGUI(self, ViewSegyTextualHeader):
        self.dialog = ViewSegyTextualHeader
        #
        _translate = QtCore.QCoreApplication.translate
        ViewSegyTextualHeader.setWindowTitle(_translate("ViewSegyTextualHeader", "SEG-Y Textual Header"))
        self.lblhelp.setText(_translate("ViewSegyTextualHeader",
                                        '<a href="https://seg.org/Portals/0/SEG/News%20and%20Resources/Technical%20Standards/seg_y_rev1.pdf">SEG-Y Format</a>'))
        self.lblhelp.setOpenExternalLinks(True)
        if os.path.exists(self.segyfile):
            _header = seis_io.readSegyTextualHeader(self.segyfile)
            for _i in _header:
                item = QtWidgets.QListWidgetItem(self.lwgheader)
                item.setText(_translate("ViewSegyTextualHeader", _i))
                self.lwgheader.addItem(item)


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ViewSegyTextualHeader = QtWidgets.QWidget()
    gui = viewsegytextualheader()
    gui.setupGUI(ViewSegyTextualHeader)
    ViewSegyTextualHeader.show()
    sys.exit(app.exec_())