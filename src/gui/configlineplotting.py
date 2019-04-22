#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a GUI for 1D curve plot

from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
import numpy as np
#
sys.path.append(os.path.dirname(__file__)[:-4])
from vis.color import color as vis_color
from vis.line import line as vis_line
from vis.marker import marker as vis_marker

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class configlineplotting(object):

    lineplottingconfig = {}
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ConfigLinePlotting):
        ConfigLinePlotting.setObjectName("ConfigLinePlotting")
        ConfigLinePlotting.setFixedSize(420, 280)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/settings.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ConfigLinePlotting.setWindowIcon(icon)
        #
        self.twgline = QtWidgets.QTableWidget(ConfigLinePlotting)
        self.twgline.setObjectName("twgline")
        self.twgline.setGeometry(QtCore.QRect(10, 10, 400, 200))
        self.twgline.setColumnCount(6)
        self.twgline.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgline.verticalHeader().hide()
        #
        self.btnapply = QtWidgets.QPushButton(ConfigLinePlotting)
        self.btnapply.setObjectName("btnapply")
        self.btnapply.setGeometry(QtCore.QRect(160, 230, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ConfigLinePlotting)
        self.msgbox.setObjectName("msgbox")
        _center_x = ConfigLinePlotting.geometry().center().x()
        _center_y = ConfigLinePlotting.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ConfigLinePlotting)
        QtCore.QMetaObject.connectSlotsByName(ConfigLinePlotting)


    def retranslateGUI(self, ConfigLinePlotting):
        self.dialog = ConfigLinePlotting
        #
        _translate = QtCore.QCoreApplication.translate
        ConfigLinePlotting.setWindowTitle(_translate("ConfigLinePlotting", "Line Plotting Configuration"))
        #
        self.twgline.setHorizontalHeaderLabels(["Line", "Color", 'Width', 'Style', 'Marker', 'Marker Size'])
        self.twgline.setRowCount(len(self.lineplottingconfig.keys()))
        _idx = 0
        for line in sorted(self.lineplottingconfig.keys()):
            item = QtWidgets.QTableWidgetItem()
            item.setText(line)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgline.setItem(_idx, 0, item)
            #
            item = QtWidgets.QComboBox()
            item.addItems(vis_color.ColorList)
            for _i in range(len(vis_color.ColorList)):
                item.setItemIcon(_i, QtGui.QIcon(
                    QtGui.QPixmap(
                        os.path.join(self.iconpath, "icons/color_" + vis_color.ColorList[_i] + ".png")).
                        scaled(80, 40)))
            item.setCurrentIndex(list.index(vis_color.ColorList,
                                            self.lineplottingconfig[line]['Color']))
            self.twgline.setCellWidget(_idx, 1, item)
            #
            item = QtWidgets.QComboBox()
            item.addItems([str(_i) for _i in vis_line.LineWidthList])
            item.setCurrentIndex(list.index(vis_line.LineWidthList,
                                            self.lineplottingconfig[line]['Width']))
            self.twgline.setCellWidget(_idx, 2, item)
            #
            item = QtWidgets.QComboBox()
            item.addItems(vis_line.LineStyleList)

            for _i in range(len(vis_line.LineStyleList)):
                item.setItemIcon(_i, QtGui.QIcon(
                    QtGui.QPixmap(
                        os.path.join(self.iconpath, "icons/line_" + vis_line.LineStyleList[_i] + ".png")).
                        scaled(80, 40)))
            item.setCurrentIndex(list.index(vis_line.LineStyleList,
                                            self.lineplottingconfig[line]['Style']))
            self.twgline.setCellWidget(_idx, 3, item)
            #
            item = QtWidgets.QComboBox()
            item.addItems(vis_marker.MarkerStyleList)
            item.setCurrentIndex(list.index(vis_marker.MarkerStyleList,
                                            self.lineplottingconfig[line]['MarkerStyle']))
            self.twgline.setCellWidget(_idx, 4, item)
            #
            item = QtWidgets.QComboBox()
            item.addItems([str(_i) for _i in vis_marker.MarkerSizeList])
            item.setCurrentIndex(list.index(vis_marker.MarkerSizeList,
                                            self.lineplottingconfig[line]['MarkerSize']))
            self.twgline.setCellWidget(_idx, 5, item)
            #
            _idx = _idx + 1
        #
        self.btnapply.setText(_translate("ConfigLinePlotting", "Apply"))
        self.btnapply.clicked.connect(self.clickBtnApply)


    def clickBtnApply(self):
        self.refreshMsgBox()
        #
        for line in sorted(self.lineplottingconfig.keys()):
            _idx = list.index(sorted(self.lineplottingconfig.keys()), line)
            _config = {}
            _config['Color'] = vis_color.ColorList[self.twgline.cellWidget(_idx, 1).currentIndex()]
            _config['Width'] = vis_line.LineWidthList[self.twgline.cellWidget(_idx, 2).currentIndex()]
            _config['Style'] = vis_line.LineStyleList[self.twgline.cellWidget(_idx, 3).currentIndex()]
            _config['MarkerStyle'] = vis_marker.MarkerStyleList[self.twgline.cellWidget(_idx, 4).currentIndex()]
            _config['MarkerSize'] = vis_marker.MarkerSizeList[self.twgline.cellWidget(_idx, 5).currentIndex()]
            self.lineplottingconfig[line] = _config
        #
        self.dialog.close()


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConfigLinePlotting = QtWidgets.QWidget()
    gui = configlineplotting()
    gui.setupGUI(ConfigLinePlotting)
    ConfigLinePlotting.show()
    sys.exit(app.exec_())