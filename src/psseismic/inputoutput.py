#############################################################################################
#                                                                                           #
# Author:       Haibin Di                                                                   #
# Last updated: March 2019                                                                  #
#                                                                                           #
#############################################################################################

# pre-stack seismic data IO
from PyQt5 import QtCore
import os
import sys
import numpy as np
import numpy.matlib as npmat
import math
#
sys.path.append(os.path.dirname(__file__)[:-10])
import segpy.reader as syreader
import segpy.packer as sypacker
from segpy.trace_header import TraceHeaderRev1
from segpy.header import field
from segpy.types import Int32

__all__ = ['inputoutput']


def scanSegy(segyfile, traceheaderformat=TraceHeaderRev1, endian='>', verbose=True):
    traceheaderpacker = sypacker.HeaderPacker(traceheaderformat, endian)
    dataformat = np.array([4, 4, 2, 4, 4, 0, 0, 1])
    with open(segyfile, 'rb') as sid:
        dat = syreader.create_reader(sid, trace_header_format=traceheaderformat, endian=endian)
        binary_header = syreader.read_binary_reel_header(sid, endian=endian)
        num_samples = binary_header.num_samples
        sample_interval = binary_header.sample_interval / 1000
        databyte = dataformat[binary_header.data_sample_format - 1]
        #
        all_shots = {}
        pos = 3200 + 400
        for itrace in dat.trace_indexes():
            if verbose:
                sys.stdout.write(
                    '\r>>> Scan %s: %d traces ' % (segyfile, itrace + 1))
                sys.stdout.flush()
            #
            header = syreader.read_trace_header(sid, trace_header_packer=traceheaderpacker, pos=pos)
            curr_ident = header.field_record_num
            #
            trace_data = dat.trace_samples(itrace)
            if curr_ident not in all_shots.keys():
                all_shots[curr_ident] = {}
                all_shots[curr_ident]['Trace_List'] = [header.trace_num]
                all_shots[curr_ident]['Data'] = {}
                all_shots[curr_ident]['Data']['Current_Trace'] = 0
                all_shots[curr_ident]['Data'][0] = trace_data
            else:
                all_shots[curr_ident]['Trace_List'].append(header.trace_num)
                # all_shots[curr_ident]['Data'] = \
                #     np.concatenate((all_shots[curr_ident]['Data'], trace_data), axis=1)
                # alternative approch of using np.concatenate that is slow
                all_shots[curr_ident]['Data']['Current_Trace'] += 1
                curr_trace = all_shots[curr_ident]['Data']['Current_Trace']
                all_shots[curr_ident]['Data'][curr_trace] = trace_data
            pos = pos + 240 + header.num_samples * databyte
        if verbose:
            print('Done')
    #
    return all_shots, num_samples, sample_interval



def readPsSeisFromSegy(segyfile, traceheaderformat=TraceHeaderRev1, endian='>',
                       verbose=True, qpgsdlg=None):
    """
    read pre-stack seismic from segy
    Args:
        segy:       segy file
        verbose:    display message or not
    Return:
         pre-stack seismic a dictionary of all gathers, with each gather as a dictionary of two keys:
                ShotData:   gather data as a 2D mat
                ShotInfo:   gather information with the following keys:
    """
    if os.path.exists(segyfile) is False or os.path.isfile(segyfile) is False:
        print("ERROR in readSeisPSFromSegy: No pre-stack segy found")
        sys.exit()
    #
    all_shots, num_samples, sample_interval = \
        scanSegy(segyfile, traceheaderformat=traceheaderformat, endian=endian)
    #
    if verbose is True:
        print("Read " + segyfile + ": " + str(len(all_shots)) + " shots")
    #
    psseis = {}
    #
    if qpgsdlg is not None:
        qpgsdlg.setMaximum(len(all_shots))
    #
    ishot = 0
    for shot in all_shots:
        #
        trace_list = np.unique(all_shots[shot]['Trace_List'])
        trace_step = 1
        if len(trace_list) > 1:
            trace_step = min(np.abs(trace_list[0:-1]-trace_list[1:]))
        trace_start = np.min(trace_list)
        trace_num_per_line = int((np.max(trace_list) - np.min(trace_list)) / trace_step) + 1
        trace_end = trace_start + (trace_num_per_line-1)*trace_step
        #
        trace_id_previous = trace_end + 1
        nline = 0
        for itrace in range(len(all_shots[shot]['Trace_List'])):
            trace_id = all_shots[shot]['Trace_List'][itrace]
            # check if a new line
            if trace_id <= trace_id_previous:
                nline += 1
            trace_id_previous = trace_id
        #
        if qpgsdlg is not None:
            QtCore.QCoreApplication.instance().processEvents()
            qpgsdlg.setValue(ishot)
        #
        if verbose:
            sys.stdout.write(
                '\r>>> Read %d of %d shots: %s, %d line x %d traces/line (from %d to %d with step %d)'
                % (ishot+1, len(all_shots), str(shot), nline, trace_num_per_line, trace_start, trace_end, trace_step))
            sys.stdout.flush()
        ishot += 1
        # print('>>> Shot %s contains %d lines with %d traces per line (from %d to %d with step %d)'
        #       %(str(shot), nline, trace_num_per_line, trace_start, trace_end, trace_step))
        #
        psdata = {}
        psdata['ShotInfo'] = {}
        psdata['ShotInfo']['ZNum'] = num_samples
        psdata['ShotInfo']['ILNum'] = nline
        psdata['ShotInfo']['XLNum'] = trace_num_per_line
        #
        psdata['ShotInfo']['ZStart'] = 0
        psdata['ShotInfo']['ZStep'] = - sample_interval
        psdata['ShotInfo']['ZEnd'] = 0 + (psdata['ShotInfo']['ZNum'] - 1) * psdata['ShotInfo']['ZStep']
        psdata['ShotInfo']['ZRange'] = np.linspace(psdata['ShotInfo']['ZStart'], psdata['ShotInfo']['ZEnd'],
                                                   psdata['ShotInfo']['ZNum'])
        psdata['ShotInfo']['XLStart'] = trace_start
        psdata['ShotInfo']['XLStep'] = trace_step
        psdata['ShotInfo']['XLEnd'] = trace_end
        psdata['ShotInfo']['XLRange'] = np.linspace(trace_start, trace_end, trace_num_per_line)
        psdata['ShotInfo']['ILStart'] = 0
        psdata['ShotInfo']['ILStep'] = 1
        psdata['ShotInfo']['ILEnd'] = nline - 1
        psdata['ShotInfo']['ILRange'] = np.linspace(0, nline-1, nline)
        #
        psdata['ShotData'] = np.zeros([num_samples, trace_num_per_line, nline])
        psdata['ShotInfo']['TraceFlag'] = np.ones([trace_num_per_line, nline])
        #
        trace_id_previous = trace_end + 1
        idx_line = -1
        for itrace in range(len(all_shots[shot]['Trace_List'])):
            trace_id = all_shots[shot]['Trace_List'][itrace]
            # check if a new line
            if trace_id <= trace_id_previous:
                idx_line = idx_line + 1
            trace_id_previous = trace_id
            #
            idx_trace = int((trace_id - trace_start) / trace_step)
            psdata['ShotData'][:, idx_trace, idx_line] = all_shots[shot]['Data'][itrace]
            psdata['ShotInfo']['TraceFlag'][idx_trace, idx_line] = 0
        #
        psseis[str(shot)] = psdata
    #
    if qpgsdlg is not None:
        qpgsdlg.setValue(len(all_shots))
    if verbose:
        print('Done')

    return psseis


def defSegyTraceHeaderFormat(record_byte=9, trace_byte=13):
    class SegyTraceHeaderFormat(TraceHeaderRev1):
        field_record_num = field(
            Int32, offset=record_byte, default=0, documentation=
            "Original field record number. Highly recommended for all types of data."
        )

        trace_num = field(
            Int32, offset=trace_byte, default=0, documentation=
            "Trace number within the original field record. Highly recommended for all types of data."
        )

    return SegyTraceHeaderFormat


class inputoutput:
    # pack all functions as a class
    #
    readPsSeisFromSegy = readPsSeisFromSegy
    #
    defSegyTraceHeaderFormat = defSegyTraceHeaderFormat