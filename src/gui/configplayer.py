#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# Create a GUI for player configuration

from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
import numpy as np
#
sys.path.append(os.path.dirname(__file__)[:-4])
from vis.player import player as vis_player


QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class configplayer(object):

    playerconfig = {}
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ConfigPlayer):
        ConfigPlayer.setObjectName("ConfigPlayer")
        ConfigPlayer.setFixedSize(820, 280)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/video.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ConfigPlayer.setWindowIcon(icon)
        #
        self.twgplayer = QtWidgets.QTableWidget(ConfigPlayer)
        self.twgplayer.setObjectName("twgplayer")
        self.twgplayer.setGeometry(QtCore.QRect(10, 10, 800, 200))
        self.twgplayer.setColumnCount(9)
        self.twgplayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgplayer.verticalHeader().hide()
        #
        self.btnapply = QtWidgets.QPushButton(ConfigPlayer)
        self.btnapply.setObjectName("btnapply")
        self.btnapply.setGeometry(QtCore.QRect(360, 230, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/ok.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        #
        self.msgbox = QtWidgets.QMessageBox(ConfigPlayer)
        self.msgbox.setObjectName("msgbox")
        _center_x = ConfigPlayer.geometry().center().x()
        _center_y = ConfigPlayer.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ConfigPlayer)
        QtCore.QMetaObject.connectSlotsByName(ConfigPlayer)


    def retranslateGUI(self, ConfigPlayer):
        self.dialog = ConfigPlayer
        #
        _translate = QtCore.QCoreApplication.translate
        ConfigPlayer.setWindowTitle(_translate("ConfigPlayer", "Player Configuration"))
        #
        self.twgplayer.setHorizontalHeaderLabels(["", '|<--', "<<--", '<<<<', '>>||',
                                                  '>>>>', '-->>', '-->|', 'Interval'])
        self.twgplayer.setRowCount(len(self.playerconfig.keys()))
        _idx = 0
        for play in sorted(self.playerconfig.keys()):
            item = QtWidgets.QTableWidgetItem()
            item.setText(play)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgplayer.setItem(_idx, 0, item)
            #
            for prop in vis_player.PlayerPropertyList[:-1]:
                _idxprop = list.index(vis_player.PlayerPropertyList, prop)
                item = QtWidgets.QComboBox()
                item.addItems(vis_player.PlayerKeyList)
                item.setCurrentIndex(list.index(vis_player.PlayerKeyList,
                                                self.playerconfig[play][prop]))
                self.twgplayer.setCellWidget(_idx, _idxprop+1, item)
            prop = vis_player.PlayerPropertyList[-1]
            _idxprop = list.index(vis_player.PlayerPropertyList, prop)
            item = QtWidgets.QComboBox()
            item.addItems([str(t) for t in vis_player.PlayerIntervalList])
            item.setCurrentIndex(list.index(vis_player.PlayerIntervalList,
                                            self.playerconfig[play][prop]))
            self.twgplayer.setCellWidget(_idx, _idxprop + 1, item)
            #
            _idx = _idx + 1
        #
        self.btnapply.setText(_translate("ConfigPlayer", "Apply"))
        self.btnapply.clicked.connect(self.clickBtnApply)


    def clickBtnApply(self):
        self.refreshMsgBox()
        #
        for player in sorted(self.playerconfig.keys()):
            _idx = list.index(sorted(self.playerconfig.keys()), player)
            _config = {}
            _config['First'] = vis_player.PlayerKeyList[self.twgplayer.cellWidget(_idx, 1).currentIndex()]
            _config['Previous'] = vis_player.PlayerKeyList[self.twgplayer.cellWidget(_idx, 2).currentIndex()]
            _config['Backward'] = vis_player.PlayerKeyList[self.twgplayer.cellWidget(_idx, 3).currentIndex()]
            _config['Pause'] = vis_player.PlayerKeyList[self.twgplayer.cellWidget(_idx, 4).currentIndex()]
            _config['Forward'] = vis_player.PlayerKeyList[self.twgplayer.cellWidget(_idx, 5).currentIndex()]
            _config['Next'] = vis_player.PlayerKeyList[self.twgplayer.cellWidget(_idx, 6).currentIndex()]
            _config['Last'] = vis_player.PlayerKeyList[self.twgplayer.cellWidget(_idx, 7).currentIndex()]
            _config['Interval'] = vis_player.PlayerIntervalList[self.twgplayer.cellWidget(_idx, 8).currentIndex()]
            self.playerconfig[player] = _config
        #
        self.dialog.close()


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConfigPlayer = QtWidgets.QWidget()
    gui = configplayer()
    gui.setupGUI(ConfigPlayer)
    ConfigPlayer.show()
    sys.exit(app.exec_())
