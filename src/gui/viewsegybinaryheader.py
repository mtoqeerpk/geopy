#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# Create a window for viewing seg-y binary header


from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from seismic.inputoutput import inputoutput as seis_io

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class viewsegybinaryheader(object):

    segyfile = ""
    #
    iconpath = os.path.dirname(__file__)
    dialog = None


    def setupGUI(self, ViewSegyBinaryHeader):
        ViewSegyBinaryHeader.setObjectName("ViewSegyBinaryHeader")
        ViewSegyBinaryHeader.setFixedSize(510, 460)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ViewSegyBinaryHeader.setWindowIcon(icon)
        #
        self.lblhelp = QtWidgets.QLabel(ViewSegyBinaryHeader)
        self.lblhelp.setObjectName("lblhelp")
        self.lblhelp.setGeometry(QtCore.QRect(410, 10, 80, 30))
        self.twgheader = QtWidgets.QTableWidget(ViewSegyBinaryHeader)
        self.twgheader.setObjectName("twgheader")
        self.twgheader.setGeometry(QtCore.QRect(10, 50, 480, 380))
        self.twgheader.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgheader.setRowCount(30)
        self.twgheader.setColumnCount(1)
        #
        self.msgbox = QtWidgets.QMessageBox(ViewSegyBinaryHeader)
        self.msgbox.setObjectName("msgbox")
        _center_x = ViewSegyBinaryHeader.geometry().center().x()
        _center_y = ViewSegyBinaryHeader.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ViewSegyBinaryHeader)
        QtCore.QMetaObject.connectSlotsByName(ViewSegyBinaryHeader)



    def retranslateGUI(self, ViewSegyBinaryHeader):
        self.dialog = ViewSegyBinaryHeader
        #
        _translate = QtCore.QCoreApplication.translate
        ViewSegyBinaryHeader.setWindowTitle(_translate("ViewSegyBinaryHeader", "SEG-Y Binary Header"))
        self.lblhelp.setText(_translate("ViewSegyBinaryHeader",
                                        '<a href="https://seg.org/Portals/0/SEG/News%20and%20Resources/Technical%20Standards/seg_y_rev1.pdf">SEG-Y Format</a>'))
        self.lblhelp.setOpenExternalLinks(True)
        _rowheader = ['job_id_num (3201-3204)', 'line_num (3205-3208)',
                      'reel_num (3209-3212)', 'data_traces_per_ensemble (3213-3214)',
                      'auxiliary_traces_per_ensemble (3215-3216)', 'sample_interval (3217-3218)',
                      'original_field_sample_interval (3219-3220)', 'num_samples (3221-3222)',
                      'original_field_num_samples (3223-3224)', 'data_sample_format (3225-3226)',
                      'ensemble_fold (3227-3228)', 'trace_sorting (3229-3230)',
                      'vertical_sum_code (3231-3232)', 'sweep_frequency_at_start (3233-3234)',
                      'sweep_frequency_at_end (3235-3236)', 'sweep_length (3237-3238)',
                      'sweep_type (3239-3240)', 'sweep_trace_number (3241-3242)',
                      'sweep_trace_taper_length_at_start (3243-3244)', 'sweep_trace_taper_length_at_end (3245-3246)',
                      'taper_type (3247-3248)', 'correlated_data_traces (3249-3250)',
                      'binary_gain_recovered (3251-3252)', 'amplitude_recovery_method (3253-3254)',
                      'measurement_system (3255-3256)', 'impulse_signal_polarity (3257-3258)',
                      'vibratory_polarity_code (3259-3260)', 'format_revision_num (3501-3502)',
                      'fixed_length_trace_flag (3503-3504)', 'num_extended_textual_headers (3505-3506)']
        self.twgheader.setVerticalHeaderLabels(_rowheader)
        self.twgheader.horizontalHeader().hide()
        #
        if os.path.exists(self.segyfile):
            _header = seis_io.readSegyBinaryHeader(self.segyfile)
            # job_id_num
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.job_id_num)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(0, 0, _item)
            # line_num
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.line_num)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(1, 0, _item)
            # reel_num
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.reel_num)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(2, 0, _item)
            # data_traces_per_ensemble
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.data_traces_per_ensemble)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(3, 0, _item)
            # auxiliary_traces_per_ensemble
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.auxiliary_traces_per_ensemble)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(4, 0, _item)
            # sample_interval
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.sample_interval)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(5, 0, _item)
            # original_field_sample_interval
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.original_field_sample_interval)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(6, 0, _item)
            # num_samples
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.num_samples)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(7, 0, _item)
            # original_field_num_samples
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.original_field_num_samples)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(8, 0, _item)
            # data_sample_format
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.data_sample_format)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(9, 0, _item)
            # ensemble_fold
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.ensemble_fold)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(10, 0, _item)
            # trace_sorting
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.trace_sorting)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(11, 0, _item)
            # vertical_sum_code
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.vertical_sum_code)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(12, 0, _item)
            # sweep_frequency_at_start
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.sweep_frequency_at_start)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(13, 0, _item)
            # sweep_frequency_at_end
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.sweep_frequency_at_end)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(14, 0, _item)
            # sweep_length
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.sweep_length)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(15, 0, _item)
            # sweep_type
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.sweep_type)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(16, 0, _item)
            # sweep_trace_number
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.sweep_trace_number)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(17, 0, _item)
            # sweep_trace_taper_length_at_start
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.sweep_trace_taper_length_at_start)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(18, 0, _item)
            # sweep_trace_taper_length_at_end
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.sweep_trace_taper_length_at_end)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(19, 0, _item)
            # taper_type
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.taper_type)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(20, 0, _item)
            # correlated_data_traces
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.correlated_data_traces)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(21, 0, _item)
            # binary_gain_recovered
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.binary_gain_recovered)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(22, 0, _item)
            # amplitude_recovery_method
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.amplitude_recovery_method)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(23, 0, _item)
            # measurement_system
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.measurement_system)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(24, 0, _item)
            # impulse_signal_polarity
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.impulse_signal_polarity)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(25, 0, _item)
            # vibratory_polarity_code
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.vibratory_polarity_code)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(26, 0, _item)
            # format_revision_num
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.format_revision_num)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(27, 0, _item)
            # fixed_length_trace_flag
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.fixed_length_trace_flag)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(28, 0, _item)
            # num_extended_textual_headers
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_translate("ViewSegyBinaryHeader", str(_header.num_extended_textual_headers)))
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgheader.setItem(29, 0, _item)


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ViewSegyBinaryHeader = QtWidgets.QWidget()
    gui = viewsegybinaryheader()
    gui.setupGUI(ViewSegyBinaryHeader)
    ViewSegyBinaryHeader.show()
    sys.exit(app.exec_())