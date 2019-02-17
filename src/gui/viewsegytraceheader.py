#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     April 2018                                                                      #
#                                                                                           #
#############################################################################################

# Create a window for view segy trace header


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4])
from seismic.inputoutput import inputoutput as seis_io

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class viewsegytraceheader(object):

    segyfile = ""
    #
    iconpath = os.path.dirname(__file__)
    dialog = None
    #
    tracenumlist = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]


    def setupGUI(self, ViewSegyTraceHeader):
        ViewSegyTraceHeader.setObjectName("ViewSegyTraceHeader")
        ViewSegyTraceHeader.setFixedSize(850, 460)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        ViewSegyTraceHeader.setWindowIcon(icon)
        #
        self.lblhelp = QtWidgets.QLabel(ViewSegyTraceHeader)
        self.lblhelp.setObjectName("lblhelp")
        self.lblhelp.setGeometry(QtCore.QRect(750, 10, 80, 30))
        self.lbltracenum = QtWidgets.QLabel(ViewSegyTraceHeader)
        self.lbltracenum.setObjectName("lbltracenum")
        self.lbltracenum.setGeometry(QtCore.QRect(570, 10, 80, 30))
        self.cbbtracenum = QtWidgets.QComboBox(ViewSegyTraceHeader)
        self.cbbtracenum.setObjectName("cbbtracenum")
        self.cbbtracenum.setGeometry(QtCore.QRect(650, 10, 60, 30))
        self.twgheader = QtWidgets.QTableWidget(ViewSegyTraceHeader)
        self.twgheader.setObjectName("twgheader")
        self.twgheader.setGeometry(QtCore.QRect(10, 50, 820, 380))
        self.twgheader.setRowCount(88)
        self.twgheader.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        #
        self.msgbox = QtWidgets.QMessageBox(ViewSegyTraceHeader)
        self.msgbox.setObjectName("msgbox")
        _center_x = ViewSegyTraceHeader.geometry().center().x()
        _center_y = ViewSegyTraceHeader.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        #
        self.retranslateGUI(ViewSegyTraceHeader)
        QtCore.QMetaObject.connectSlotsByName(ViewSegyTraceHeader)



    def retranslateGUI(self, ViewSegyTraceHeader):
        self.dialog = ViewSegyTraceHeader
        #
        _translate = QtCore.QCoreApplication.translate
        ViewSegyTraceHeader.setWindowTitle(_translate("ViewSegyTraceHeader", "SEG-Y Trace Header"))
        self.lblhelp.setText(_translate("ViewSegyTraceHeader",
                                        '<a href="https://seg.org/Portals/0/SEG/News%20and%20Resources/Technical%20Standards/seg_y_rev1.pdf">SEG-Y Format</a>'))
        self.lblhelp.setOpenExternalLinks(True)
        #
        self.lbltracenum.setText(_translate("ViewSegyTraceHeader", "No. of traces:"))
        self.cbbtracenum.addItems([str(num) for num in self.tracenumlist])
        self.showTraceHeader(10)
        self.cbbtracenum.currentIndexChanged.connect(self.changeCbbTracenum)


    def changeCbbTracenum(self):
        self.showTraceHeader(self.tracenumlist[self.cbbtracenum.currentIndex()])


    def showTraceHeader(self, tracenum):
        self.twgheader.clear()
        #
        _rowheader = ['line_sequence_num (1-4)', 'file_sequence_num (5-8)',
                      'field_record_num (9-12)', 'trace_num (13-16)',
                      'energy_source_point_num (17-20)', 'ensemble_num (21-24)',
                      'ensemble_trace_num (25-28)', 'trace_identification_code (29-30)',
                      'num_vertically_summed_traces (31-32)', 'num_horizontally_stacked_traces (33-34)',
                      'data_use (35-36)', 'source_receiver_offset (37-40)',
                      'receiver_group_elevation (41-44)', 'surface_elevation_at_source (45-48)',
                      'source_depth_below_surface (49-52)', 'datum_elevation_at_receiver_group (53-56)',
                      'datum_elevation_at_source (57-60)', 'water_depth_at_source (61-64)',
                      'water_depth_at_group (65-68)', 'elevation_scalar (69-70)',
                      'xy_scalar (71-72)', 'source_x (73-76)',
                      'source_y (77-80)', 'group_x (81-84)',
                      'group_y (85-88)', 'coordinate_units (89-90)',
                      'weathering_velocity (91-92)', 'subweathering_velocity (93-94)',
                      'uphole_time_at_source (95-96)', 'uphole_time_at_group (97-98)',
                      'source_static_correction (99-100)', 'group_static_correction (101-102)',
                      'total_static (103-104)', 'lag_time_a (105-106)',
                      'lag_time_b (107-108)', 'delay_recording_time (109-110)',
                      'mute_start_time (111-112)', 'mute_end_time (113-114)',
                      'num_samples (115-116)', 'sample_interval (117-118)',
                      'gain_type_of_field_instruments (119-120)', 'instrument_gain_constant (121-122)',
                      'instrument_initial_gain (123-124)', 'correlated (125-126)',
                      'sweep_frequency_at_start (127-128)', 'sweep_frequency_at_end (129-130)',
                      'sweep_length (131-132)', 'sweep_type (133-134)',
                      'sweep_trace_taper_length_at_start (135-136)', 'sweep_trace_taper_length_at_end (137-138)',
                      'taper_type (139-140)', 'alias_filter_frequency (141-142)',
                      'alias_filter_slope (143-144)', 'notch_filter_frequency (145-146)',
                      'notch_filter_slope (147-148)', 'low_cut_frequency (149-150)',
                      'high_cut_frequency (151-152)', 'low_cut_slope (153-154)',
                      'high_cut_slope (155-156)', 'year_recorded (157-158)',
                      'day_of_year (159-160)', 'hour_of_day (161-162)',
                      'minute_of_hour (163-164)', 'second_of_minute (165-166)',
                      'time_basis_code (167-168)', 'trace_weighting_factor (169-170)',
                      'geophone_group_num_roll_switch_position_one (171-172)',
                      'geophone_group_num_first_trace_original_field (173-174)',
                      'geophone_group_num_last_trace_original_field (175-176)', 'gap_size (177-178)',
                      'over_travel (179-180)', 'cdp_x (181-184)',
                      'cdp_y (185-189)', 'inline_number (189-192)',
                      'crossline_number (193-196)', 'shotpoint_number (197-200)',
                      'shotpoint_scalar (201-202)', 'trace_unit (203-204)',
                      'transduction_constant_mantissa (205-208)', 'transduction_constant_exponent (208-210)',
                      'transduction_units (211-212)', 'device_trace_identifier (213-214)',
                      'time_scalar (215-216)', 'source_type (217-218)',
                      'source_energy_direction (219-224)', 'source_measurement_mantissa (225-228)',
                      'source_measurement_exponent (229-230)', 'source_measurement_unit (231-232)']
        self.twgheader.setVerticalHeaderLabels(_rowheader)
        #
        if os.path.exists(self.segyfile):
            _traceidx = np.linspace(0, tracenum-1, tracenum, dtype=int)
            self.twgheader.setColumnCount(tracenum)
            _colheader = ["Trace "+str(i+1) for i in _traceidx]
            self.twgheader.setHorizontalHeaderLabels(_colheader)
            #
            # Progress dialog
            _pgsdlg = QtWidgets.QProgressDialog()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, "icons/segy.png")),
                           QtGui.QIcon.Normal, QtGui.QIcon.Off)
            _pgsdlg.setWindowIcon(icon)
            _pgsdlg.setWindowTitle('View SEG-Y Trace Header')
            _pgsdlg.setCancelButton(None)
            _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            _pgsdlg.forceShow()
            _pgsdlg.setFixedWidth(400)
            _pgsdlg.setMaximum(tracenum)
            #
            for _idx in _traceidx:
                #
                QtCore.QCoreApplication.instance().processEvents()
                _pgsdlg.setValue(_idx+1)
                #
                _header = seis_io.readSegyTraceHeader(self.segyfile, traceidx=_idx)
                # line_dequence_num
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.line_sequence_num))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(0, _idx, _item)
                # file_sequence_num
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.file_sequence_num))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(1, _idx, _item)
                # field_record_num
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.field_record_num))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(2, _idx, _item)
                # trace_num
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.trace_num))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(3, _idx, _item)
                # energy_source_point_num
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.energy_source_point_num))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(4, _idx, _item)
                # ensemble_num
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.ensemble_num))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(5, _idx, _item)
                # ensemble_trace_num
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.ensemble_trace_num))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(6, _idx, _item)
                # trace_identification_code
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.trace_identification_code))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(7, _idx, _item)
                # num_vertically_summed_traces
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.num_vertically_summed_traces))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(8, _idx, _item)
                # num_horizontally_stacked_traces
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.num_horizontally_stacked_traces))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(9, _idx, _item)
                # data_use
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.data_use))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(10, _idx, _item)
                # source_receiver_offset
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.source_receiver_offset))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(11, _idx, _item)
                # receiver_group_elevation
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.receiver_group_elevation))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(12, _idx, _item)
                # surface_elevation_at_source
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.surface_elevation_at_source))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(13, _idx, _item)
                # source_depth_below_surface
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.source_depth_below_surface))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(14, _idx, _item)
                # datum_elevation_at_receiver_group
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.datum_elevation_at_receiver_group))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(15, _idx, _item)
                # datum_elevation_at_source
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.datum_elevation_at_source))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(16, _idx, _item)
                # water_depth_at_source
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.water_depth_at_source))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(17, _idx, _item)
                # water_depth_at_group
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.water_depth_at_group))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(18, _idx, _item)
                # elevation_scalar
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.elevation_scalar))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(19, _idx, _item)
                # xy_scalar
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.xy_scalar))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(20, _idx, _item)
                # source_x
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.source_x))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(21, _idx, _item)
                # source_y
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.source_y))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(22, _idx, _item)
                # group_x
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.group_x))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(23, _idx, _item)
                # group_y
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.group_y))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(24, _idx, _item)
                # coordinate_units
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.coordinate_units))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(25, _idx, _item)
                # weathering_velocity
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.weathering_velocity))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(26, _idx, _item)
                # subweathering_velocity
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.subweathering_velocity))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(27, _idx, _item)
                # uphole_time_at_source
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.uphole_time_at_source))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(28, _idx, _item)
                # uphole_time_at_group
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.uphole_time_at_group))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(29, _idx, _item)
                # source_static_correction
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.source_static_correction))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(30, _idx, _item)
                # group_static_correction
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.group_static_correction))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(31, _idx, _item)
                # total_static
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.total_static))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(32, _idx, _item)
                # lag_time_a
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.lag_time_a))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(33, _idx, _item)
                # lag_time_b
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.lag_time_b))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(34, _idx, _item)
                # delay_recording_time
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.delay_recording_time))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(35, _idx, _item)
                # mute_start_time
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.mute_start_time))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(36, _idx, _item)
                # mute_end_time
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.mute_end_time))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(37, _idx, _item)
                # num_samples
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.num_samples))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(38, _idx, _item)
                # sample_interval
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.sample_interval))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(39, _idx, _item)
                # gain_type_of_field_instruments
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.gain_type_of_field_instruments))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(40, _idx, _item)
                # instrument_gain_constant
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.instrument_gain_constant))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(41, _idx, _item)
                # instrument_initial_gain
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.instrument_initial_gain))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(42, _idx, _item)
                # correlated
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.correlated))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(43, _idx, _item)
                # sweep_frequency_at_start
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.sweep_frequency_at_start))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(44, _idx, _item)
                # sweep_frequency_at_end
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.sweep_frequency_at_end))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(45, _idx, _item)
                # sweep_length
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.sweep_length))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(46, _idx, _item)
                # sweep_type
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.sweep_type))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(47, _idx, _item)
                # sweep_trace_taper_length_at_start
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.sweep_trace_taper_length_at_start))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(48, _idx, _item)
                # sweep_trace_taper_length_at_end
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.sweep_trace_taper_length_at_end))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(49, _idx, _item)
                # taper_type
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.taper_type))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(50, _idx, _item)
                # alias_filter_frequency
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.alias_filter_frequency))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(51, _idx, _item)
                # alias_filter_slope
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.alias_filter_slope))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(52, _idx, _item)
                # notch_filter_frequency
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.notch_filter_frequency))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(53, _idx, _item)
                # notch_filter_slope
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.notch_filter_slope))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(54, _idx, _item)
                # low_cut_frequency
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.low_cut_frequency))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(55, _idx, _item)
                # high_cut_frequency
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.high_cut_frequency))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(56, _idx, _item)
                # low_cut_slope
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.low_cut_slope))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(57, _idx, _item)
                # high_cut_slope
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.high_cut_slope))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(58, _idx, _item)
                # year_recorded
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.year_recorded))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(59, _idx, _item)
                # day_of_year
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.day_of_year))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(60, _idx, _item)
                # hour_of_day
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.hour_of_day))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(61, _idx, _item)
                # minute_of_hour
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.minute_of_hour))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(62, _idx, _item)
                # second_of_minute
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.second_of_minute))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(63, _idx, _item)
                # time_basis_code
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.time_basis_code))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(64, _idx, _item)
                # trace_weighting_factor
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.trace_weighting_factor))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(65, _idx, _item)
                # geophone_group_num_roll_switch_position_one
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.geophone_group_num_roll_switch_position_one))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(66, _idx, _item)
                # geophone_group_num_first_trace_original_field
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(
                    str(_header.geophone_group_num_first_trace_original_field))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(67, _idx, _item)
                # geophone_group_num_last_trace_original_field
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(
                    str(_header.geophone_group_num_last_trace_original_field))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(68, _idx, _item)
                # gap_size
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.gap_size))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(69, _idx, _item)
                # over_travel
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.over_travel))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(70, _idx, _item)
                # cdp_x
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.cdp_x))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(71, _idx, _item)
                # cdp_y
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.cdp_y))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(72, _idx, _item)
                # inline_number
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.inline_number))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(73, _idx, _item)
                # crossline_number
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.crossline_number))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(74, _idx, _item)
                # shotpoint_number
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.shotpoint_number))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(75, _idx, _item)
                # shotpoint_scalar
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.shotpoint_scalar))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(76, _idx, _item)
                # trace_unit
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.trace_unit))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(77, _idx, _item)
                # transduction_constant_mantissa
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.transduction_constant_mantissa))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(78, _idx, _item)
                # transduction_constant_exponent
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.transduction_constant_exponent))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(79, _idx, _item)
                # transduction_units
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.transduction_units))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(80, _idx, _item)
                # device_trace_identifier
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.device_trace_identifier))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(81, _idx, _item)
                # time_scalar
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.time_scalar))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(82, _idx, _item)
                # source_type
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.source_type))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(83, _idx, _item)
                # source_energy_direction
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.source_energy_direction))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(84, _idx, _item)
                # source_measurement_mantissa
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.source_measurement_mantissa))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(85, _idx, _item)
                # source_measurement_exponent
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.source_measurement_exponent))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(86, _idx, _item)
                # source_measurement_unit
                _item = QtWidgets.QTableWidgetItem()
                _item.setText(str(_header.source_measurement_unit))
                _item.setFlags(QtCore.Qt.ItemIsEditable)
                _item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgheader.setItem(87, _idx, _item)
            #
            _pgsdlg.setValue(tracenum)


    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ViewSegyTraceHeader = QtWidgets.QWidget()
    gui = viewsegytraceheader()
    gui.setupGUI(ViewSegyTraceHeader)
    ViewSegyTraceHeader.show()
    sys.exit(app.exec_())