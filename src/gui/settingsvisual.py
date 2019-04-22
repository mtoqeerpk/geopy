#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a GUI for setting (visualization)

from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from core.settings import settings as core_set
from vis.font import font as vis_font
from vis.line import line as vis_line
from vis.marker import marker as vis_marker
from vis.image import image as vis_image
from vis.colormap import colormap as vis_cmap
from vis.player import player as vis_player

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class settingsvisual(object):

    settings = core_set.Visual
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, SettingsVisual):
        SettingsVisual.setObjectName("SettingsVisual")
        SettingsVisual.setFixedSize(840, 470)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/image.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        SettingsVisual.setWindowIcon(icon)
        #
        self.lblfont = QtWidgets.QLabel(SettingsVisual)
        self.lblfont.setObjectName("lblfont")
        self.lblfont.setGeometry(QtCore.QRect(430, 10, 160, 30))
        self.lblfontname = QtWidgets.QLabel(SettingsVisual)
        self.lblfontname.setObjectName("lblfontname")
        self.lblfontname.setGeometry(QtCore.QRect(450, 50, 70, 30))
        self.cbbfontname = QtWidgets.QComboBox(SettingsVisual)
        self.cbbfontname.setObjectName("cbbfontname")
        self.cbbfontname.setGeometry(QtCore.QRect(520, 50, 110, 30))
        self.lblfontweight = QtWidgets.QLabel(SettingsVisual)
        self.lblfontweight.setObjectName("lblfontweight")
        self.lblfontweight.setGeometry(QtCore.QRect(650, 90, 70, 30))
        self.cbbfontweight = QtWidgets.QComboBox(SettingsVisual)
        self.cbbfontweight.setObjectName("cbbfontweight")
        self.cbbfontweight.setGeometry(QtCore.QRect(720, 90, 110, 30))
        self.lblfontsize = QtWidgets.QLabel(SettingsVisual)
        self.lblfontsize.setObjectName("lblfontsize")
        self.lblfontsize.setGeometry(QtCore.QRect(450, 90, 70, 30))
        self.cbbfontsize = QtWidgets.QComboBox(SettingsVisual)
        self.cbbfontsize.setObjectName("cbbfontsize")
        self.cbbfontsize.setGeometry(QtCore.QRect(520, 90, 110, 30))
        self.lblfontcolor = QtWidgets.QLabel(SettingsVisual)
        self.lblfontcolor.setObjectName("lblfontcolor")
        self.lblfontcolor.setGeometry(QtCore.QRect(450, 130, 70, 30))
        self.cbbfontcolor = QtWidgets.QComboBox(SettingsVisual)
        self.cbbfontcolor.setObjectName("cbbfontcolor")
        self.cbbfontcolor.setGeometry(QtCore.QRect(520, 130, 110, 30))
        #
        self.lblline = QtWidgets.QLabel(SettingsVisual)
        self.lblline.setObjectName("lblline")
        self.lblline.setGeometry(QtCore.QRect(10, 10, 160, 30))
        self.lbllinecolor = QtWidgets.QLabel(SettingsVisual)
        self.lbllinecolor.setObjectName("lbllinecolor")
        self.lbllinecolor.setGeometry(QtCore.QRect(30, 50, 70, 30))
        self.cbblinecolor = QtWidgets.QComboBox(SettingsVisual)
        self.cbblinecolor.setObjectName("cbblinecolor")
        self.cbblinecolor.setGeometry(QtCore.QRect(100, 50, 110, 30))
        self.lbllinestyle = QtWidgets.QLabel(SettingsVisual)
        self.lbllinestyle.setObjectName("lbllinestyle")
        self.lbllinestyle.setGeometry(QtCore.QRect(30, 90, 70, 30))
        self.cbblinestyle = QtWidgets.QComboBox(SettingsVisual)
        self.cbblinestyle.setObjectName("cbblinestyle")
        self.cbblinestyle.setGeometry(QtCore.QRect(100, 90, 110, 30))
        self.lbllinewidth = QtWidgets.QLabel(SettingsVisual)
        self.lbllinewidth.setObjectName("lbllinewidth")
        self.lbllinewidth.setGeometry(QtCore.QRect(230, 90, 70, 30))
        self.cbblinewidth = QtWidgets.QComboBox(SettingsVisual)
        self.cbblinewidth.setObjectName("cbblinewidth")
        self.cbblinewidth.setGeometry(QtCore.QRect(300, 90, 110, 30))
        self.lblmarkerstyle = QtWidgets.QLabel(SettingsVisual)
        self.lblmarkerstyle.setObjectName("lblmarkerstyle")
        self.lblmarkerstyle.setGeometry(QtCore.QRect(30, 130, 70, 30))
        self.cbbmarkerstyle = QtWidgets.QComboBox(SettingsVisual)
        self.cbbmarkerstyle.setObjectName("cbbmarkerstyle")
        self.cbbmarkerstyle.setGeometry(QtCore.QRect(100, 130, 110, 30))
        self.lblmarkersize = QtWidgets.QLabel(SettingsVisual)
        self.lblmarkersize.setObjectName("lblmarkersize")
        self.lblmarkersize.setGeometry(QtCore.QRect(230, 130, 70, 30))
        self.cbbmarkersize = QtWidgets.QComboBox(SettingsVisual)
        self.cbbmarkersize.setObjectName("cbbmarkersize")
        self.cbbmarkersize.setGeometry(QtCore.QRect(300, 130, 110, 30))
        #
        self.lblsurf = QtWidgets.QLabel(SettingsVisual)
        self.lblsurf.setObjectName("lblsurf")
        self.lblsurf.setGeometry(QtCore.QRect(10, 180, 160, 30))
        self.lblcmap = QtWidgets.QLabel(SettingsVisual)
        self.lblcmap.setObjectName("lblcmap")
        self.lblcmap.setGeometry(QtCore.QRect(30, 220, 70, 30))
        self.cbbcmap = QtWidgets.QComboBox(SettingsVisual)
        self.cbbcmap.setObjectName("cbbcolor")
        self.cbbcmap.setGeometry(QtCore.QRect(100, 220, 110, 30))
        self.lblinterp = QtWidgets.QLabel(SettingsVisual)
        self.lblinterp.setObjectName("lblinterp")
        self.lblinterp.setGeometry(QtCore.QRect(230, 220, 70, 30))
        self.cbbinterp = QtWidgets.QComboBox(SettingsVisual)
        self.cbbinterp.setObjectName("cbbinterp")
        self.cbbinterp.setGeometry(QtCore.QRect(300, 220, 110, 30))
        #
        self.lblplayer = QtWidgets.QLabel(SettingsVisual)
        self.lblplayer.setObjectName("lblplayer")
        self.lblplayer.setGeometry(QtCore.QRect(10, 270, 160, 30))
        self.twgplayer = QtWidgets.QTableWidget(SettingsVisual)
        self.twgplayer.setObjectName("twgplayer")
        self.twgplayer.setGeometry(QtCore.QRect(30, 310, 800, 90))
        self.twgplayer.setColumnCount(8)
        self.twgplayer.setRowCount(1)
        self.twgplayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgplayer.verticalHeader().hide()
        #
        self.btnapply = QtWidgets.QPushButton(SettingsVisual)
        self.btnapply.setObjectName("btnapply")
        self.btnapply.setGeometry(QtCore.QRect(370, 420, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(SettingsVisual)
        self.msgbox.setObjectName("msgbox")
        _center_x = SettingsVisual.geometry().center().x()
        _center_y = SettingsVisual.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(SettingsVisual)
        QtCore.QMetaObject.connectSlotsByName(SettingsVisual)


    def retranslateGUI(self, SettingsVisual):
        self.dialog = SettingsVisual
        #
        _translate = QtCore.QCoreApplication.translate
        SettingsVisual.setWindowTitle(_translate("SettingsVisual", "Visual Settings"))
        #
        self.lblfont.setText(_translate("SettingsVisual", "Font:"))
        self.lblfontname.setText(_translate("SettingsVisual", "Name:"))
        self.cbbfontname.addItems(vis_font.FontNameList)
        self.lblfontweight.setText(_translate("SettingsVisual", "Weight:"))
        self.cbbfontweight.addItems(vis_font.FontWeightList)
        self.lblfontsize.setText(_translate("SettingsVisual", "Size:"))
        self.cbbfontsize.addItems([str(w) for w in vis_font.FontSizeList])
        self.lblfontcolor.setText(_translate("SettingsVisual", "Color:"))
        self.cbbfontcolor.addItems(vis_font.FontColorList)
        for _i in range(len(vis_font.FontColorList)):
            self.cbbfontcolor.setItemIcon(_i, QtGui.QIcon(
                QtGui.QPixmap(
                    os.path.join(self.iconpath, "icons/color_" + vis_font.FontColorList[_i] + ".png")).scaled(80, 40)))
        #
        self.lblline.setText(_translate("SettingsVisual", "Line / Curve:"))
        self.lbllinecolor.setText(_translate("SettingsVisual", "Color:"))
        self.cbblinecolor.addItems(vis_line.LineColorList)
        for _i in range(len(vis_line.LineColorList)):
            self.cbblinecolor.setItemIcon(_i, QtGui.QIcon(
                QtGui.QPixmap(
                    os.path.join(self.iconpath, "icons/color_" + vis_line.LineColorList[_i] + ".png")).scaled(80, 40)))
        self.lbllinestyle.setText(_translate("SettingsVisual", "Line style:"))
        self.cbblinestyle.addItems(vis_line.LineStyleList)
        for _i in range(len(vis_line.LineStyleList)):
            self.cbblinestyle.setItemIcon(_i, QtGui.QIcon(
                QtGui.QPixmap(
                    os.path.join(self.iconpath, "icons/line_" + vis_line.LineStyleList[_i] + ".png")).scaled(80, 40)))
        self.lbllinewidth.setText(_translate("SettingsVisual", "Line width:"))
        self.cbblinewidth.addItems([str(w) for w in vis_line.LineWidthList])
        self.lblmarkerstyle.setText(_translate("SettingsVisual", "Marker style:"))
        self.cbbmarkerstyle.addItems(vis_marker.MarkerStyleList)
        self.lblmarkersize.setText(_translate("SettingsVisual", "Marker size:"))
        self.cbbmarkersize.addItems([str(w) for w in vis_marker.MarkerSizeList])
        #
        self.lblsurf.setText(_translate("SettingsVisual", "Surface / Volume:"))
        self.lblcmap.setText(_translate("SettingsVisual", "Color map:"))
        self.cbbcmap.addItems(vis_cmap.ColorMapList)
        for _i in range(len(vis_cmap.ColorMapList)):
            self.cbbcmap.setItemIcon(_i, QtGui.QIcon(
                QtGui.QPixmap(
                    os.path.join(self.iconpath, "icons/cmap_" + vis_cmap.ColorMapList[_i] + ".png")).scaled(80, 40)))
        self.lblinterp.setText(_translate("SettingsVisual", "Interpolation:"))
        self.cbbinterp.addItems(vis_image.InterpolationList)
        for _i in range(len(vis_image.InterpolationList)):
            self.cbbinterp.setItemIcon(_i, QtGui.QIcon(
                QtGui.QPixmap(
                    os.path.join(self.iconpath, "icons/interp_" + vis_image.InterpolationList[_i] + ".png")).scaled(80, 40)))
        #
        self.lblplayer.setText(_translate("SettingsVisual", "Player:"))
        self.twgplayer.setHorizontalHeaderLabels(['|<--', "<<--", '<<<<', '>>||',
                                                  '>>>>', '-->>', '-->|', 'Interval'])
        for _i in vis_player.PlayerPropertyList[:-1]:
            _idx = list.index(vis_player.PlayerPropertyList, _i)
            item = QtWidgets.QComboBox()
            item.addItems(vis_player.PlayerKeyList)
            self.twgplayer.setCellWidget(0, _idx, item)
        _idx = list.index(vis_player.PlayerPropertyList, vis_player.PlayerPropertyList[-1])
        item = QtWidgets.QComboBox()
        item.addItems([str(t) for t in vis_player.PlayerIntervalList])
        self.twgplayer.setCellWidget(0, _idx, item)
        #
        self.btnapply.setText(_translate("SettingsVisual", "Apply"))
        self.btnapply.clicked.connect(self.clickBtnApply)
        #
        self.cbbfontname.setCurrentIndex(list.index(vis_font.FontNameList, self.settings['Font']['Name']))
        self.cbbfontweight.setCurrentIndex(list.index(vis_font.FontWeightList, self.settings['Font']['Weight']))
        self.cbbfontsize.setCurrentIndex(list.index(vis_font.FontSizeList, self.settings['Font']['Size']))
        self.cbbfontcolor.setCurrentIndex(list.index(vis_font.FontColorList, self.settings['Font']['Color']))
        #
        self.cbblinecolor.setCurrentIndex(list.index(vis_line.LineColorList, self.settings['Line']['Color']))
        self.cbblinewidth.setCurrentIndex(list.index(vis_line.LineWidthList, self.settings['Line']['Width']))
        self.cbblinestyle.setCurrentIndex(list.index(vis_line.LineStyleList, self.settings['Line']['Style']))
        self.cbbmarkerstyle.setCurrentIndex(list.index(vis_marker.MarkerStyleList, self.settings['Line']['MarkerStyle']))
        self.cbbmarkersize.setCurrentIndex(list.index(vis_marker.MarkerSizeList, self.settings['Line']['MarkerSize']))
        #
        self.cbbcmap.setCurrentIndex(list.index(vis_cmap.ColorMapList, self.settings['Image']['Colormap']))
        self.cbbinterp.setCurrentIndex(list.index(vis_image.InterpolationList, self.settings['Image']['Interpolation']))
        #
        for _i in vis_player.PlayerPropertyList[:-1]:
            _idx = list.index(vis_player.PlayerPropertyList, _i)
            self.twgplayer.cellWidget(0, _idx).setCurrentIndex(list.index(vis_player.PlayerKeyList,
                                                                          self.settings['Player'][_i]))
        _i = vis_player.PlayerPropertyList[-1]
        _idx = list.index(vis_player.PlayerPropertyList, _i)
        self.twgplayer.cellWidget(0, _idx).setCurrentIndex(list.index(vis_player.PlayerIntervalList,
                                                                      self.settings['Player'][_i]))


    def clickBtnApply(self):
        self.refreshMsgBox()
        #
        self.settings['Font']['Name'] = vis_font.FontNameList[self.cbbfontname.currentIndex()]
        self.settings['Font']['Weight'] = vis_font.FontWeightList[self.cbbfontweight.currentIndex()]
        self.settings['Font']['Size'] = vis_font.FontSizeList[self.cbbfontsize.currentIndex()]
        self.settings['Font']['Color'] = vis_font.FontColorList[self.cbbfontcolor.currentIndex()]
        #
        self.settings['Line']['Color'] = vis_line.LineColorList[self.cbblinecolor.currentIndex()]
        self.settings['Line']['Width'] = vis_line.LineWidthList[self.cbblinewidth.currentIndex()]
        self.settings['Line']['Style'] = vis_line.LineStyleList[self.cbblinestyle.currentIndex()]
        self.settings['Line']['MarkerStyle'] = vis_marker.MarkerStyleList[self.cbbmarkerstyle.currentIndex()]
        self.settings['Line']['MarkerSize'] = vis_marker.MarkerSizeList[self.cbbmarkersize.currentIndex()]
        #
        self.settings['Image']['Colormap'] = vis_cmap.ColorMapList[self.cbbcmap.currentIndex()]
        self.settings['Image']['Interpolation'] = vis_image.InterpolationList[self.cbbinterp.currentIndex()]
        #
        for _prop in vis_player.PlayerPropertyList[:-1]:
            _idx = list.index(vis_player.PlayerPropertyList, _prop)
            self.settings['Player'][_prop] = \
                vis_player.PlayerKeyList[self.twgplayer.cellWidget(0, _idx).currentIndex()]
        _prop = vis_player.PlayerPropertyList[-1]
        _idx = list.index(vis_player.PlayerPropertyList, _prop)
        self.settings['Player'][_prop] = \
            vis_player.PlayerIntervalList[self.twgplayer.cellWidget(0, _idx).currentIndex()]
        #
        self.dialog.close()


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SettingsVisual = QtWidgets.QWidget()
    gui = settingsvisual()
    gui.setupGUI(SettingsVisual)
    SettingsVisual.show()
    sys.exit(app.exec_())