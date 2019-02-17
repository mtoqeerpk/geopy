#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# seismic data processing functions

from PyQt5 import QtCore
import sys
import numpy as np
import numpy.matlib as npmat


__all__ = ['analysis']


def getSeisInfoFrom2DMat(seis2dmat, inlcol=0, xlcol=1, zcol=2):
    """
    Get basic information of 3D seismic survey from 2D seismic matrix
    Args:
        seis2dmat:  2D mat of seismic data containing at least three columns [IL, XL, Z]
        inlcol:     index of inline column. Default is the first column (0)
        xlcol:      index of crossline column. Default is the second column (1)
        zcol:       index of z column. Default is the third column (2)
    Returns:
        seisinfo:   survey information for quick reading
                    A dictionary containing the following keys:
                        ILStart --- first inline No.
                        ILEnd   --- last inline No.
                        ILStep  --- step between two adjacent inlines
                        ILNum   --- number of inlines
                        ILRange --- array of all inlines
                        XLStart --- first crossline No.
                        XLEnd   --- last crossline No.
                        XLStep  --- step between two adjacent crosslines
                        XLNum   --- number of crosslines
                        XLRange --- array of all crosslines
                        ZStart  --- top z slice
                        ZEnd    --- bottom z slice
                        ZStep   --- step between two adjacent z slices
                        ZNum    --- number of z slices
                        ZRange  --- array of all z slices
    Note:
        Negative z is used in the vertical direction
    """

    # Initialize
    seisinfo = {}

    # Check size of input 2D matrix
    if np.ndim(seis2dmat) != 2:
        print('ERROR in getSeisInfoFrom2DMat: 2D seismic matrix expected')
        sys.exit()
    if inlcol < 0 or len(seis2dmat[0,:]) < inlcol:
        print('ERROR in getSeisInfoFrom2DMat: No inline column found in 2D seismic matrix')
        sys.exit()
    if xlcol < 0 or len(seis2dmat[0,:]) < xlcol:
        print('ERROR in getSeisInfoFrom2DMat: No crossline column found in 2D seismic matrix')
        sys.exit()
    if zcol < 0 or len(seis2dmat[0,:]) < zcol:
        print('ERROR in getSeisInfoFrom2DMat: No z column found in 2D seismic matrix')
        sys.exit()

    # Starting from the Z column
    zrange = seis2dmat[:, zcol]
    zstart = zrange[0]
    zend = zrange[-1]
    zstep = -1
    znum = 1
    if zstart != zend:
        zstep = zrange[1] - zrange[0]
        znum = (zend-zstart) / zstep + 1
    zstart = np.round(zstart).astype(np.int32)
    zstep = np.round(zstep).astype(np.int32)
    if zstep == 0:
        zstep = -1
    znum = np.round(znum).astype(np.int32)
    zend = (zstart + (znum-1)*zstep).astype(np.int32)
    zrange = np.linspace(zstart, zend, znum).astype(np.int32)
    # Add to seisinfo
    seisinfo['ZStart'] = zstart
    seisinfo['ZEnd'] = zend
    seisinfo['ZStep'] = zstep
    seisinfo['ZNum'] = znum
    seisinfo['ZRange'] = zrange

    # Then the Crossline column
    xlrange = seis2dmat[:, xlcol]
    xlstart = xlrange[0]
    xlend = xlrange[-1]
    xlstep = 1
    xlnum = 1
    if xlstart != xlend:
        xlstep = xlrange[int(znum)] - xlrange[0]
        xlnum = (xlend-xlstart) / xlstep + 1
    xlstart = np.round(xlstart).astype(np.int32)
    xlstep = np.round(xlstep).astype(np.int32)
    if xlstep == 0:
        xlstep = 1
    xlnum = np.round(xlnum).astype(np.int32)
    xlend = (xlstart + (xlnum-1)*xlstep).astype(np.int32)
    xlrange = np.linspace(xlstart, xlend, xlnum).astype(np.int32)
    # Add to seisinfo
    seisinfo['XLStart'] = xlstart
    seisinfo['XLEnd'] = xlend
    seisinfo['XLStep'] = xlstep
    seisinfo['XLNum'] = xlnum
    seisinfo['XLRange'] = xlrange

    # Finally the Inline column
    inlrange = seis2dmat[:, inlcol]
    inlstart = inlrange[0]
    inlend = inlrange[-1]
    inlstep = 1
    inlnum = 1
    if inlstart != inlend:
        inlstep = inlrange[int(znum*xlnum)] - inlrange[0]
        inlnum = (inlend-inlstart) / inlstep + 1
    inlstart = np.round(inlstart).astype(np.int32)
    inlstep = np.round(inlstep).astype(np.int32)
    inlnum = np.round(inlnum).astype(np.int32)
    if inlstep == 0:
        inlstep = 1
    inlend = (inlstart + (inlnum - 1) * inlstep).astype(np.int32)
    inlrange = np.linspace(inlstart, inlend, inlnum).astype(np.int32)
    # Add to seisinfo
    seisinfo['ILStart'] = inlstart
    seisinfo['ILEnd'] = inlend
    seisinfo['ILStep'] = inlstep
    seisinfo['ILNum'] = inlnum
    seisinfo['ILRange'] = inlrange

    #
    seisinfo['TraceNum'] = (inlnum * xlnum).astype(np.int64)
    seisinfo['SampleNum'] = (seisinfo['TraceNum'] * znum).astype(np.int64)

    return seisinfo


def checkSeisInfo(seisinfo):
    """
    Check basic information of seismic
    Args:
        seisinfo:   survey information for quick reading
                    A dictionary containing the following keys:
                        ILStart --- first inline No.
                        ILEnd   --- last inline No.
                        ILStep  --- step between two adjacent inlines
                        ILNum   --- number of inlines
                        ILRange --- array of all inlines
                        XLStart --- first crossline No.
                        XLEnd   --- last crossline No.
                        XLStep  --- step between two adjacent crosslines
                        XLNum   --- number of crosslines
                        XLRange --- array of all crosslines
                        ZStart  --- top z slice
                        ZEnd    --- bottom z slice
                        ZStep   --- step between two adjacent z slices
                        ZNum    --- number of z slices
                        ZRange  --- array of all z slices
    Note:
        Negative z is used in the vertical direction
    """

    info = ['ILStart', 'ILEnd', 'ILStep', 'ILNum', 'ILRange',
            'XLStart', 'XLEnd', 'XLStep', 'XLNum', 'XLRange',
            'ZStart', 'ZEnd', 'ZStep', 'ZNum', 'ZRange',
            'TraceNum', 'SampleNum']

    if seisinfo is None:
        return False

    for f in info:
        if f not in seisinfo.keys():
            #print("Error in checkSeisInfo: %s not found in seisinfo" %f)
            return False

    return True


def makeSeisInfo(inlstart=0, inlstep=0, inlnum=0,
                 xlstart=0, xlstep=0, xlnum=0,
                 zstart=0, zstep=0, znum=0):
    seisinfo = {}
    seisinfo['ILStart'] = inlstart
    seisinfo['ILEnd'] = inlstart + (inlnum-1)*inlstep
    seisinfo['ILStep'] = inlstep
    seisinfo['ILNum'] = inlnum
    seisinfo['ILRange'] = np.linspace(0, inlnum-1, 1) * inlstep + inlstart
    seisinfo['XLStart'] = xlstart
    seisinfo['XLEnd'] = xlstart + (xlnum-1)*xlstep
    seisinfo['XLStep'] = xlstep
    seisinfo['XLNum'] = xlnum
    seisinfo['XLRange'] = np.linspace(0, inlnum-1, 1) * xlstep + xlstart
    seisinfo['ZStart'] = zstart
    seisinfo['ZEnd'] = zstart + (znum-1) * zstep
    seisinfo['ZStep'] = zstep
    seisinfo['ZNum'] = znum
    seisinfo['ZRange'] = np.linspace(0, inlnum-1, 1) * zstep + zstart
    seisinfo['TraceNum'] = (inlnum * xlnum)
    seisinfo['SampleNum'] = (seisinfo['TraceNum'] * znum)



def createSeisInfoFrom3DMat(seis3dmat, inlstart=0, inlstep=1,
                            xlstart=0, xlstep=1,
                            zstart=0, zstep=-1):
    """
    Create basic information of 3D seismic survey from 3D seismic matrix
    In particular, inline/crossline No. starts from 0 with step 1
                   z slices starts from 0 with step -1
    Argus:
        seis3dmat:  3D matrix of the seismic data [Z/XL/IL]
        inlstart:   first inline No.. Default is 0
        inlstep:    step between two adjacent inlines. Default is 1
        xlstart:    first crosslien No.. Default is 0
        xlstep:     step between two adjacent crosslines. Default is 1
        zstart:     top z slice. Default is 0
        zstep:      step between two adjacent z slices. Default is -1
    Returns:
         seisinfo:  survey information for quick reading
                    A dictionary containing the following keys:
                        ILStart --- first inline No.
                        ILEnd   --- last inline No.
                        ILStep  --- step between two adjacent inlines
                        ILNum   --- number of inlines
                        ILRange --- array of all inlines
                        XLStart --- first crossline No.
                        XLEnd   --- last crossline No.
                        XLStep  --- step between two adjacent crosslines
                        XLNum   --- number of crosslines
                        XLRange --- array of all crosslines
                        ZStart  --- top z slice
                        ZEnd    --- bottom z slice
                        ZStep   --- step between two adjacent z slices
                        ZNum    --- number of z slices
                        ZRange  --- array of all z slices
    Note:
        Negative z is used in the vertical direction
    """

    # Initialize
    seisinfo = {}

    # Check the dimension of input
    if np.ndim(seis3dmat) != 3:
        print('ERROR in createSeisInfoFrom3DMat: 3D seismic matrix expected')
        sys.exit()

    znum, xlnum, inlnum = np.shape(seis3dmat)

    inlstart = np.round(inlstart).astype(np.int32)
    inlstep = np.round(inlstep).astype(np.int32)
    inlnum = np.round(inlnum).astype(np.int32)
    if inlstep == 0:
        inlstep = 1
    inlend = (inlstart + inlstep * (inlnum-1)).astype(np.int32)
    inlrange = np.linspace(inlstart, inlend, inlnum).astype(np.int32)
    seisinfo['ILStart'] = inlstart
    seisinfo['ILEnd'] = inlend
    seisinfo['ILStep'] = inlstep
    seisinfo['ILNum'] = inlnum
    seisinfo['ILRange'] = inlrange

    xlstart = np.round(xlstart).astype(np.int32)
    xlstep = np.round(xlstep).astype(np.int32)
    xlnum = np.round(xlnum).astype(np.int32)
    if xlstep == 0:
        xlstep = 1
    xlend = (xlstart + xlstep * (xlnum-1)).astype(np.int32)
    xlrange = np.linspace(xlstart, xlend, xlnum).astype(np.int32)
    seisinfo['XLStart'] = xlstart
    seisinfo['XLEnd'] = xlend
    seisinfo['XLStep'] = xlstep
    seisinfo['XLNum'] = xlnum
    seisinfo['XLRange'] = xlrange

    zstart = np.round(zstart).astype(np.int32)
    zstep = np.round(zstep).astype(np.int32)
    znum = np.round(znum).astype(np.int32)
    if zstep == 0:
        zstep = -1
    zend = (zstart + zstep * (znum - 1)).astype(np.int32)
    zrange = np.linspace(zstart, zend, znum).astype(np.int32)
    seisinfo['ZStart'] = zstart
    seisinfo['ZEnd'] = zend
    seisinfo['ZStep'] = zstep
    seisinfo['ZNum'] = znum
    seisinfo['ZRange'] = zrange

    seisinfo['TraceNum'] = (inlnum * xlnum).astype(np.int64)
    seisinfo['SampleNum'] = (seisinfo['TraceNum'] * znum).astype(np.int64)

    return seisinfo


def convertSeis2DMatTo3DMat(seis2dmat, datacol=3,
                            inlcol=0, xlcol=1, zcol=2):
    """
    Convert seismic data in 2D Matrix to 3D Matrix
    Argus:
        seis2dmat:  2D matrix of seismic data containing at least four columns
                    [IL, XL, Z, Value ...]
        datacol:    index of data column for conversion (indexing from 0)
                    Default is the fourth column (3)
        inlcol:     index of inline column. Default is the first column (0)
        xlcol:      index of crossline column. Default is the second column (1)
        zcol:       index of z column. Default is the third column (2)
    Returns:
        seis3dmat:  3D seismic matrix [Z/XL/IL]
    """

    # Check size of input 2D matrix
    if np.ndim(seis2dmat) != 2:
        print('ERROR in convertSeis2DMatTo3DMat: 2D seismic matrix expected')
        sys.exit()
    if datacol < 0 or len(seis2dmat[0, :]) <= datacol:
        print('ERROR in convertSeis2DMatTo3DMat: No data column found in 2D seismic matrix')
        sys.exit()
    if inlcol < 0 or len(seis2dmat[0, :]) <= inlcol:
        print('ERROR in convertSeis2DMatTo3DMat: No inline column found in 2D seismic matrix')
        sys.exit()
    if xlcol < 0 or len(seis2dmat[0, :]) <= xlcol:
        print('ERROR in convertSeis2DMatTo3DMat: No crossline column found in 2D seismic matrix')
        sys.exit()
    if zcol < 0 or len(seis2dmat[0, :]) <= zcol:
        print('ERROR in convertSeis2DMatTo3DMat: No z column found in 2D seismic matrix')
        sys.exit()

    # Get the basic information of the seismic survey
    seisinfo = getSeisInfoFrom2DMat(seis2dmat,
                                    inlcol=inlcol, xlcol=xlcol, zcol=zcol)

    inlnum = seisinfo['ILNum']
    xlnum = seisinfo['XLNum']
    znum = seisinfo['ZNum']

    seisdata = seis2dmat[:, datacol]

    seisdata = seisdata.transpose()
    seisdata = np.reshape(seisdata, [inlnum, xlnum, znum])
    seisdata = seisdata.transpose()

    return seisdata


def convertSeis3DMatTo2DMat(seis3dmat, seisinfo=None):
    """
    Convert seismic data in 3D matrix to 2D matrix
    Argus:
        seis3dmat:  3D matrix of seismic data [Z/XL/IL]
        seisinfo:   basic information of the seismic survey.
                    Auto-generated from 3D seismic matrix if not provided
                    A dictionary containing the following keys:
                        ILStart --- first inline No.
                        ILEnd   --- last inline No.
                        ILStep  --- step between two adjacent inlines
                        ILNum   --- number of inlines
                        ILRange --- array of all inlines
                        XLStart --- first crossline No.
                        XLEnd   --- last crossline No.
                        XLStep  --- step between two adjacent crosslines
                        XLNum   --- number of crosslines
                        XLRange --- array of all crosslines
                        ZStart  --- top z slice
                        ZEnd    --- bottom z slice
                        ZStep   --- step between two adjacent z slices
                        ZNum    --- number of z slices
                        ZRange  --- array of all z slices
    Return:
        seis2dmat:  2D seismic matrix of the datacontaining four columns [IL, XL, Z, Value]
    """

    # Check the dimension of input matrix
    if np.ndim(seis3dmat) != 3:
        print('ERROR in convertSeis3DMatTo2DMat: 3D seismic matrix expected')
        sys.exit()

    if seisinfo is None:
        print('WARNING in convertSeis3DMatTo2DMat: Survey info auto-generated from 3D seismic matrix')
        seisinfo = createSeisInfoFrom3DMat(seis3dmat)

    inlnum = seisinfo['ILNum']
    xlnum = seisinfo['XLNum']
    znum = seisinfo['ZNum']

    if (znum, xlnum, inlnum) != np.shape(seis3dmat):
        print('ERROR in convertSeis3DMatTo2DMat: Dimension not match between 3D matrix and survey info')
        sys.exit()

    tracenum = (inlnum * xlnum).astype(np.int64)
    samplenum = (tracenum * znum).astype(np.int64)

    seisdata = seis3dmat.transpose()
    seisdata = np.reshape(seisdata, [1, samplenum])
    seisdata = seisdata.transpose()

    # Add inline, crossline, and z information
    inlstart = seisinfo['ILStart']
    inlend = seisinfo['ILEnd']
    xlstart = seisinfo['XLStart']
    xlend = seisinfo['XLEnd']
    zstart = seisinfo['ZStart']
    zend = seisinfo['ZEnd']
    inl = np.linspace(inlstart, inlend, inlnum)
    inl = npmat.repmat(inl, znum * xlnum, 1)
    inl = inl.transpose()
    inl = np.reshape(inl, [samplenum, 1])
    xl = np.linspace(xlstart, xlend, xlnum)
    xl = npmat.repmat(xl, znum, 1)
    xl = xl.transpose()
    xl = np.reshape(xl, [xlnum * znum, 1])
    xl = npmat.repmat(xl, 1, inlnum)
    xl = xl.transpose()
    xl = np.reshape(xl, [samplenum, 1])
    z = np.linspace(zstart, zend, znum)
    z = npmat.repmat(z, 1, tracenum)
    z = np.reshape(z, [samplenum, 1])

    seis2dmat = np.concatenate((inl, xl, z, seisdata), axis=1)

    return seis2dmat


def convertSeisInfoTo2DMat(seisinfo):
    """
    Convert seismic info to 2D matrix
    Argus:
        seisinfo:   basic information of the seismic survey.
                    Auto-generated from 3D seismic matrix if not provided
                    A dictionary containing the following keys:
                        ILStart --- first inline No.
                        ILEnd   --- last inline No.
                        ILStep  --- step between two adjacent inlines
                        ILNum   --- number of inlines
                        ILRange --- array of all inlines
                        XLStart --- first crossline No.
                        XLEnd   --- last crossline No.
                        XLStep  --- step between two adjacent crosslines
                        XLNum   --- number of crosslines
                        XLRange --- array of all crosslines
                        ZStart  --- top z slice
                        ZEnd    --- bottom z slice
                        ZStep   --- step between two adjacent z slices
                        ZNum    --- number of z slices
                        ZRange  --- array of all z slices
    Return:
        seis2dmat:  2D seismic matrix of the datacontaining four columns [IL, XL, Z]
    """

    if checkSeisInfo(seisinfo) is False:
        print("Error in convertSeisInfoTo2DMat: Seisinfo not correct")
        sys.exit()

    inlnum = seisinfo['ILNum']
    xlnum = seisinfo['XLNum']
    znum = seisinfo['ZNum']

    tracenum = (inlnum * xlnum).astype(np.int64)
    samplenum = (tracenum * znum).astype(np.int64)

    # Add inline, crossline, and z information
    inlstart = seisinfo['ILStart']
    inlend = seisinfo['ILEnd']
    xlstart = seisinfo['XLStart']
    xlend = seisinfo['XLEnd']
    zstart = seisinfo['ZStart']
    zend = seisinfo['ZEnd']
    inl = np.linspace(inlstart, inlend, inlnum)
    inl = npmat.repmat(inl, znum * xlnum, 1)
    inl = inl.transpose()
    inl = np.reshape(inl, [samplenum, 1])
    xl = np.linspace(xlstart, xlend, xlnum)
    xl = npmat.repmat(xl, znum, 1)
    xl = xl.transpose()
    xl = np.reshape(xl, [xlnum * znum, 1])
    xl = npmat.repmat(xl, 1, inlnum)
    xl = xl.transpose()
    xl = np.reshape(xl, [samplenum, 1])
    z = np.linspace(zstart, zend, znum)
    z = npmat.repmat(z, 1, tracenum)
    z = np.reshape(z, [samplenum, 1])

    seis2dmat = np.concatenate((inl, xl, z), axis=1)

    return seis2dmat


def retrieveSeisSampleFrom2DMat(seis2dmat, samples=None, datacol=3,
                                inlcol=0, xlcol=1, zcol=2,
                                verbose=True):
    """
    Retrieve seismic data on specified samples from 2D matrix
    Argus:
        seis2dmat:  seismic data in 2D matrix of at least four columns [IL, XL, Z, Value, ...]
        samples:    list of samples in 2D matrix of three columns [IL, XL, Z]
                    All samples are retrieved if not specified
        datacol:    index of data column for retrieval (indexing from 0)
                    Default is the fourth column (3)
        inlcol:     index of inline column. Default is the first column (0)
        xlcol:      index of crossline column. Default is the second column (1)
        zcol:       index of z column. Default is the third column (2)
        verbose:    flag for message display. Default is True
    Return:
        seisdata:   seismic data on specified samples
                    2D matrix of four columns [IL, XL, Z, Value]
    Note:
        Negative z is used in the vertical direction
    """

    # Check input matrix
    if np.ndim(seis2dmat) != 2:
        print('ERROR in retrieveSeisSampleFrom2DMat: 2D seismic matrix expected')
        sys.exit()
    if datacol < 0 or len(seis2dmat[0,:]) <= datacol:
        print('ERROR in retrieveSeisSampleFrom2DMat: Not data column found in 2D seismic matrix')
        sys.exit()
    if inlcol < 0 or len(seis2dmat[0,:]) < inlcol:
        print('ERROR in retrieveSeisSampleFrom2DMat: No inline column found in 2D seismic matrix')
        sys.exit()
    if xlcol < 0 or len(seis2dmat[0,:]) < xlcol:
        print('ERROR in retrieveSeisSampleFrom2DMat: No crossline column found in 2D seismic matrix')
        sys.exit()
    if zcol < 0 or len(seis2dmat[0,:]) < zcol:
        print('ERROR in retrieveSeisSampleFrom2DMat: No z column found in 2D seismic matrix')
        sys.exit()

    if samples is None:
        print('WARNING in retrieveSeisSampleFrom2DMat: to retrieve all samples in 2D seismic matrix')
        inlloc = seis2dmat[:,inlcol]
        xlloc = seis2dmat[:,xlcol]
        zloc = seis2dmat[:,zcol]
        seisdata = seis2dmat[:, datacol]
        seisdata = np.reshape(seisdata, [len(seisdata), 1])
        seisdata = np.concatenate((inlloc, xlloc, zloc, seisdata), axis=1)
        return seisdata

    if np.ndim(samples) != 2:
        print('ERROR in retrieveSeisSampleFrom2DMat: 2D matrix of samples expected')
        sys.exit()
    if len(samples[0,:]) < 3:
        print('ERROR in retrieveSeisSampleFrom2DMat: 3 columns expected in 2D sample matrix')
        sys.exit()

    seisinfo = getSeisInfoFrom2DMat(seis2dmat,
                                    inlcol=inlcol, xlcol=xlcol, zcol=zcol)
    inlstart = seisinfo['ILStart']
    inlstep = seisinfo['ILStep']
    inlnum = seisinfo['ILNum']
    xlstart = seisinfo['XLStart']
    xlstep = seisinfo['XLStep']
    xlnum = seisinfo['XLNum']
    zstart = seisinfo['ZStart']
    zstep = seisinfo['ZStep']
    znum = seisinfo['ZNum']
    if inlnum == 1:
        inlstep = 1
    if xlnum == 1:
        xlstep = 1
    if znum == 1:
        zstep = -1

    nsample, _ = np.shape(samples)
    if verbose:
        print('Retrieve ' + str(nsample) + ' samples')

    seisdata = np.zeros([nsample, 4], np.float32)
    for i in range(nsample):
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nsample) * 100.0))
            sys.stdout.flush()
        #
        inl = samples[i, 0]
        xl = samples[i, 1]
        z = samples[i, 2]

        inlidx = np.round((inl-inlstart)/inlstep).astype(np.int32)
        xlidx = np.round((xl-xlstart)/xlstep).astype(np.int32)
        zidx = np.round((z-zstart)/zstep).astype(np.int32)

        if inlidx>=0 and inlidx<inlnum and xlidx>=0 and xlidx<xlnum \
            and zidx>=0 and zidx<znum :
            idx = inlidx*xlnum*znum+xlidx*znum+zidx
            seisdata[i, 0] = seis2dmat[idx, inlcol]
            seisdata[i, 1] = seis2dmat[idx, xlcol]
            seisdata[i, 2] = seis2dmat[idx, zcol]
            seisdata[i, 3] = seis2dmat[idx, datacol]
    #
    if verbose:
        sys.stdout.write(' Done\n')

    return seisdata


def retrieveSeisSampleFrom3DMat(seis3dmat, samples=None, seisinfo=None,
                                verbose=True):
    """
    Retrieve seismic data on specified samples from 3D matrix
    Argus:
        seis3dmat:  seismic data in 3D matrix [Z/XL/IL]
        samples:    list of samples in 2D matrix of three columns [IL, XL, Z]
                    All samples are retrieved if not specified
        seisinfo:   basic information of 3D seismic survey
                    Auto-generated from 3D seismic matrix if not specified
        verbose:    flag for message display. Default is True
    Return:
        seisdata:   seismic data on specified samples
                    2D matrix of four columns [IL, XL, Z, Value]
    Note:
        Negative z is used in the vertical direction
    """

    if np.ndim(seis3dmat) != 3:
        print('ERROR in retrieveSeisSampleFrom3DMat: 3D seismic matrix expected')
        sys.exit()

    if seisinfo is None:
        print('WARNING in retrieveSeisSampleFrom3DMat: Survey info auto-generated from 3D seismic matrix')
        seisinfo = createSeisInfoFrom3DMat(seis3dmat)

    if samples is None:
        print('WARNING in retrieveSeisSampleFrom3DMat: to retrieve all samples in 3D seismic matrix')
        return convertSeis3DMatTo2DMat(seis3dmat, seisinfo)

    if np.ndim(samples) != 2:
        print('ERROR in retrieveSeisSampleFrom3DMat: 2D matrix of samples expected')
        sys.exit()
    if len(samples[0, :]) < 3:
        print('ERROR in retrieveSeisSampleFrom3DMat: 3 columns expected in 2D sample matrix')
        sys.exit()

    inlstart = seisinfo['ILStart']
    inlstep = seisinfo['ILStep']
    inlnum = seisinfo['ILNum']
    xlstart = seisinfo['XLStart']
    xlstep = seisinfo['XLStep']
    xlnum = seisinfo['XLNum']
    zstart = seisinfo['ZStart']
    zstep = seisinfo['ZStep']
    znum = seisinfo['ZNum']
    if inlnum == 1:
        inlstep = 1
    if xlnum == 1:
        xlstep = 1
    if znum == 1:
        zstep = -1

    nsample, _ = np.shape(samples)
    if verbose:
        print('Retrieve ' + str(nsample) + ' samples')

    seisdata = np.zeros([nsample, 4], np.float32)
    for i in range(nsample):
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nsample) * 100.0))
            sys.stdout.flush()
        #
        inl = samples[i, 0]
        xl = samples[i, 1]
        z = samples[i, 2]

        inlidx = np.round((inl - inlstart) / inlstep).astype(np.int32)
        xlidx = np.round((xl - xlstart) / xlstep).astype(np.int32)
        zidx = np.round((z - zstart) / zstep).astype(np.int32)

        if inlidx >= 0 and inlidx < inlnum and xlidx >= 0 and xlidx < xlnum \
                and zidx >= 0 and zidx < znum:
            idx = inlidx * xlnum * znum + xlidx * znum + zidx
            seisdata[i, 0] = inlidx * inlstep + inlstart
            seisdata[i, 1] = xlidx * xlstep + xlstart
            seisdata[i, 2] = zidx * zstep + zstart
            seisdata[i, 3] = seis3dmat[zidx, xlidx, inlidx]
    #
    if verbose:
        sys.stdout.write(' Done\n')

    return seisdata


def retrieveSeisILSliceFrom2DMat(seis2dmat, inlsls=None, datacol=3,
                                 inlcol=0, xlcol=1, zcol=2,
                                 verbose=True):
    """
    Retrieve seismic data along specified inline slices from 2D matrix
    Argus:
        seis2dmat:  seismic data in 2D matrix of at least four columns [IL, XL, Z, Value, ...]
        inlsls:     list of inline slices in array [inl1, inl2, ...]
                    Retrieve all inline slices if not specified
        datacol:    index of data column for retrieval (indexing from 0)
                    Default is the fourth column (3)
        inlcol:     index of inline column. Default is the first column (0)
        xlcol:      index of crossline column. Default is the second column (1)
        zcol:       index of z column. Default is the third column (2)
        verbose:    flag for message display. Default is True
    Return:
        seisdata:   seismic data along specified inline slices
                    2D matrix of four columns [IL, XL, Z, Value]
    Note:
        Negative z is used in the vertical direction
    """

    # Check input matrix
    if np.ndim(seis2dmat) != 2:
        print('ERROR in retrieveSeisILSliceFrom2DMat: 2D seismic matrix expected')
        sys.exit()
    if datacol < 0 or len(seis2dmat[0, :]) <= datacol:
        print('ERROR in retrieveSeisILSliceFrom2DMat: No data columns found in 2D seismic matrix')
        sys.exit()
    if inlcol < 0 or len(seis2dmat[0,:]) < inlcol:
        print('ERROR in retrieveSeisILSliceFrom2DMat: No inline column found in 2D seismic matrix')
        sys.exit()
    if xlcol < 0 or len(seis2dmat[0,:]) < xlcol:
        print('ERROR in retrieveSeisILSliceFrom2DMat: No crossline column found in 2D seismic matrix')
        sys.exit()
    if zcol < 0 or len(seis2dmat[0,:]) < zcol:
        print('ERROR in retrieveSeisILSliceFrom2DMat: No z column found in 2D seismic matrix')
        sys.exit()

    if inlsls is None:
        print('WARNING in retrieveSeisILSliceFrom2DMat: to retrieve all inline slices in 2D seismic matrix')
        inlloc = seis2dmat[:, inlcol]
        xlloc = seis2dmat[:, xlcol]
        zloc = seis2dmat[:, zcol]
        seisdata = seis2dmat[:, datacol]
        seisdata = np.reshape(seisdata, [len(seisdata), 1])
        seisdata = np.concatenate((inlloc, xlloc, zloc, seisdata), axis=1)
        return seisdata

    if np.ndim(inlsls) != 1:
        print('ERROR in retrieveSeisILSliceFrom2DMat: 1D array of inline slices expected')
        sys.exit()

    seisinfo = getSeisInfoFrom2DMat(seis2dmat,
                                    inlcol=inlcol, xlcol=xlcol, zcol=zcol)

    inl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=inlcol,
                                       inlcol=inlcol, xlcol=xlcol, zcol=zcol)
    xl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=xlcol,
                                      inlcol=inlcol, xlcol=xlcol, zcol=zcol)
    z3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=zcol,
                                     inlcol=inlcol, xlcol=xlcol, zcol=zcol)
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=datacol,
                                        inlcol=inlcol, xlcol=xlcol, zcol=zcol)

    inlstart = seisinfo['ILStart']
    inlstep = seisinfo['ILStep']
    znum, xlnum, inlnum = np.shape(seis3dmat)
    if inlnum == 1:
        inlstep = 1

    ninlsls = len(inlsls)
    if verbose:
        print('Retrieve ' + str(ninlsls) + ' inline slices')

    seisinl = np.zeros([znum, xlnum, ninlsls], np.float32)
    seisxl = np.zeros([znum, xlnum, ninlsls], np.float32)
    seisz = np.zeros([znum, xlnum, ninlsls], np.float32)
    seisdata = np.zeros([znum, xlnum, ninlsls], np.float32)
    for i in range(ninlsls):
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(ninlsls) * 100.0))
            sys.stdout.flush()
        #
        inl = inlsls[i]
        idx = np.round((inl-inlstart)/inlstep).astype(np.int32)
        if idx>=0 and idx<inlnum:
            seisinl[:, :, i] = inl3dmat[:, :, idx]
            seisxl[:, :, i] = xl3dmat[:, :, idx]
            seisz[:, :, i] = z3dmat[:, :, idx]
            seisdata[:, :, i] = seis3dmat[:, :, idx]
    #
    if verbose:
        sys.stdout.write(' Done\n')

    seisinl = seisinl.transpose()
    seisinl = np.reshape(seisinl, [1, znum * xlnum * ninlsls])
    seisinl = seisinl.transpose()
    seisxl = seisxl.transpose()
    seisxl = np.reshape(seisxl, [1, znum * xlnum * ninlsls])
    seisxl = seisxl.transpose()
    seisz = seisz.transpose()
    seisz = np.reshape(seisz, [1, znum * xlnum * ninlsls])
    seisz = seisz.transpose()
    seisdata = seisdata.transpose()
    seisdata = np.reshape(seisdata, [1, znum*xlnum*ninlsls])
    seisdata = seisdata.transpose()

    seisdata = np.concatenate((seisinl, seisxl, seisz, seisdata), axis=1)

    return seisdata


def retrieveSeisILSliceFrom3DMat(seis3dmat, inlsls=None, seisinfo=None,
                                 verbose=True):
    """
    Retrieve seismic data along specified inline slices from 3D matrix
    Argus:
        seisddmat:  seismic data in 3D matrix [Z/XL/IL]
        inlsls:     list of inline slices in array [inl1, inl2, ...]
                    Retrieve all inline slices if not specified
        seisinfo:   basic information of 3D seismic survey
                    Auto-generated from 3D seismic matrix if not specified
        verbose:    flag for message display. Default is True
    Return:
        seisdata:   seismic data along specified inline slices
                    2D matrix of four columns [IL, XL, Z, Value]
    Note:
        Negative z is used in the vertical direction
    """

    if np.ndim(seis3dmat) != 3:
        print('ERROR in retrieveSeisILSliceFrom3DMat: 3D seismic matrix expected')
        sys.exit()

    if seisinfo is None:
        print('WARNING in retrieveSeisILSliceFrom3DMat: Survey info auto-generated from 3D seismic matrix')
        seisinfo = createSeisInfoFrom3DMat(seis3dmat)

    seis2dmat = convertSeis3DMatTo2DMat(seis3dmat, seisinfo)

    if inlsls is None:
        print('WARNING in retrieveSeisILSliceFrom3DMat: to retrieve all inline slices in 3D seismic matrix')
        seisloc = seis2dmat[:, 0:3]
        seisdata = seis2dmat[:, 3]
        seisdata = np.reshape(seisdata, [len(seisdata), 1])
        seisdata = np.concatenate((seisloc, seisdata), axis=1)
        return seisdata

    if np.ndim(inlsls) != 1:
        print('ERROR in retrieveSeisILSliceFrom3DMat: 1D array of inline slices expected')
        sys.exit()

    inl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=0)
    xl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=1)
    z3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=2)

    inlstart = seisinfo['ILStart']
    inlstep = seisinfo['ILStep']
    znum, xlnum, inlnum = np.shape(seis3dmat)
    if inlnum == 1:
        inlstep = 1

    ninlsls = len(inlsls)
    if verbose:
        print('Retrieve ' + str(ninlsls) + ' inline slices')

    seisinl = np.zeros([znum, xlnum, ninlsls], np.float32)
    seisxl = np.zeros([znum, xlnum, ninlsls], np.float32)
    seisz = np.zeros([znum, xlnum, ninlsls], np.float32)
    seisdata = np.zeros([znum, xlnum, ninlsls], np.float32)
    for i in range(ninlsls):
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(ninlsls) * 100.0))
            sys.stdout.flush()
        #
        inl = inlsls[i]
        idx = np.round((inl - inlstart) / inlstep).astype(np.int32)
        if idx >= 0 and idx < inlnum:
            seisinl[:, :, i] = inl3dmat[:, :, idx]
            seisxl[:, :, i] = xl3dmat[:, :, idx]
            seisz[:, :, i] = z3dmat[:, :, idx]
            seisdata[:, :, i] = seis3dmat[:, :, idx]
    #
    if verbose:
        sys.stdout.write(' Done\n')

    seisinl = seisinl.transpose()
    seisinl = np.reshape(seisinl, [1, znum * xlnum * ninlsls])
    seisinl = seisinl.transpose()
    seisxl = seisxl.transpose()
    seisxl = np.reshape(seisxl, [1, znum * xlnum * ninlsls])
    seisxl = seisxl.transpose()
    seisz = seisz.transpose()
    seisz = np.reshape(seisz, [1, znum * xlnum * ninlsls])
    seisz = seisz.transpose()
    seisdata = seisdata.transpose()
    seisdata = np.reshape(seisdata, [1, znum * xlnum * ninlsls])
    seisdata = seisdata.transpose()

    seisdata = np.concatenate((seisinl, seisxl, seisz, seisdata), axis=1)

    return seisdata


def cutSeisILSliceFrom2DMat(seis2dmat,inlsls=None,
                            imageheight=100, imagewidth=100,
                            xlstart=None, xlend=None, xlstep=None,
                            zstart=None, zend=None, zstep=None,
                            datacol=3, inlcol=0, xlcol=1, zcol=2,
                            verbose=True):
    seisinfo = getSeisInfoFrom2DMat(seis2dmat,
                                    inlcol=inlcol, xlcol=xlcol, zcol=zcol)
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=datacol,
                                        inlcol=inlcol, xlcol=xlcol, zcol=zcol)
    #
    if inlsls is None:
        print('WARNING in cutSeisILSliceFrom2DMat: to cut all inline slices in 2D seismic matrix')
        inlsls = seisinfo['ILRange']
    if xlstart is None:
        xlstart = seisinfo['XLStart']
    if xlend is None:
        xlend = seisinfo['XLEnd']
    if xlstep is None:
        xlstep = seisinfo['XLStep']
    if zstart is None:
        zstart = seisinfo['ZStart']
    if zend is None:
        zend = seisinfo['ZEnd']
    if zstep is None:
        zstep = seisinfo['ZStep']

    #
    xlidx = np.arange(xlstart, xlend+1, xlstep)
    xlidx = np.round((xlidx - seisinfo['XLStart'])/seisinfo['XLStep']).astype(np.int32)
    xlidx = np.unique(xlidx)
    outidx = []
    for i in range(len(xlidx)):
        if xlidx[i] < 0 or xlidx[i] + imagewidth > seisinfo['XLNum']:
            outidx.append(i)
    xlidx = np.delete(xlidx, outidx)
    #
    zidx = np.arange(zstart, zend, zstep)
    zidx = np.round((zidx - seisinfo['ZStart']) / seisinfo['ZStep']).astype(np.int32)
    zidx = np.unique(zidx)
    outidx = []
    for i in range(len(zidx)):
        if zidx[i] < 0 or zidx[i] + imageheight > seisinfo['ZNum']:
            outidx.append(i)
    zidx = np.delete(zidx, outidx)
    #
    ninlsls = len(inlsls)
    if verbose:
        print('Cut ' + str(ninlsls) + ' inline slices')
    nxlidx = len(xlidx)
    nzidx = len(zidx)
    #
    seisilslicepatch = np.zeros([ninlsls, nxlidx, nzidx, imageheight, imagewidth])
    #
    for i in range(ninlsls):
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(ninlsls) * 100.0))
            sys.stdout.flush()
        #
        inl = inlsls[i]
        idx = np.round((inl-seisinfo['ILStart'])/seisinfo['ILStep']).astype(np.int32)
        for j in range(nxlidx):
            for k in range(nzidx):
                seisilslicepatch[i, j, k, :, :] = \
                    seis3dmat[zidx[k]:zidx[k]+imageheight, xlidx[j]:xlidx[j]+imagewidth, idx]
    #
    if verbose:
        sys.stdout.write(' Done\n')

    return np.reshape(seisilslicepatch, [ninlsls, nxlidx, nzidx, imageheight*imagewidth])


def retrieveSeisXLSliceFrom2DMat(seis2dmat, xlsls=None, datacol=3,
                                 inlcol=0, xlcol=1, zcol=2,
                                 verbose=True):
    """
    Retrieve seismic data along specified crossline slices from 2D matrix
    Argus:
        seis2dmat:  seismic data in 2D matrix of at least four columns [IL, XL, Z, Value, ...]
        xlsls:      list of crossline slices in array [xl1, xl2, ...]
                    Retrieve all crossline slices if not specified
        datacol:    index of data column for retrieval (indexing from 0)
                    Default is the fourth column (3)
        inlcol:     index of inline column. Default is the first column (0)
        xlcol:      index of crossline column. Default is the second column (1)
        zcol:       index of z column. Default is the third column (2)
        verbose:    flag for message display. Default is True
    Return:
        seisdata:   seismic data along specified crossline slices
                    as 2D matrix of four columns [IL, XL, Z, Value]
    Note:
        Negative z is used in the vertical direction
    """

    # Check input matrix
    if np.ndim(seis2dmat) != 2:
        print('ERROR in retrieveSeisXLSliceFrom2DMat: 2D seismic matrix expected')
        sys.exit()
    if datacol < 0 or len(seis2dmat[0, :]) <= datacol:
        print('ERROR in retrieveSeisXLSliceFrom2Dmat: Not data column found in 2D seismic matrix')
        sys.exit()
    if inlcol < 0 or len(seis2dmat[0, :]) <= inlcol:
        print('ERROR in retrieveSeisXLSliceFrom2Dmat: Not inline column found in 2D seismic matrix')
        sys.exit()
    if xlcol < 0 or len(seis2dmat[0, :]) <= xlcol:
        print('ERROR in retrieveSeisXLSliceFrom2Dmat: Not crossline column found in 2D seismic matrix')
        sys.exit()
    if zcol < 0 or len(seis2dmat[0, :]) <= zcol:
        print('ERROR in retrieveSeisXLSliceFrom2Dmat: Not z column found in 2D seismic matrix')
        sys.exit()

    if xlsls is None:
        print('WARNING in retrieveSeisXLSliceFrom2DMat: to retrieve all crossline slices in 2D seismic matrix')
        inlloc = seis2dmat[:, inlcol]
        xlloc = seis2dmat[:, xlcol]
        zloc = seis2dmat[:, zcol]
        seisdata = seis2dmat[:, datacol]
        seisdata = np.reshape(seisdata, [len(seisdata), 1])
        seisdata = np.concatenate((inlloc, xlloc, zloc, seisdata), axis=1)
        return seisdata

    if np.ndim(xlsls) != 1:
        print('ERROR in retrieveSeisXLSliceFrom2DMat: 1D array of crossline slices expected')
        sys.exit()

    seisinfo = getSeisInfoFrom2DMat(seis2dmat,
                                    inlcol=inlcol, xlcol=xlcol, zcol=zcol)

    inl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=inlcol,
                                       inlcol=inlcol, xlcol=xlcol, zcol=zcol)
    xl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=xlcol,
                                      inlcol=inlcol, xlcol=xlcol, zcol=zcol)
    z3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=zcol,
                                     inlcol=inlcol, xlcol=xlcol, zcol=zcol)
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=datacol,
                                        inlcol=inlcol, xlcol=xlcol, zcol=zcol)

    xlstart = seisinfo['XLStart']
    xlstep = seisinfo['XLStep']
    znum, xlnum, inlnum = np.shape(seis3dmat)
    if xlnum == 1:
        xlstep = 1

    nxlsls = len(xlsls)
    if verbose:
        print('Retrieve ' + str(nxlsls) + ' crossline slices')

    seisinl = np.zeros([znum, nxlsls, inlnum], np.float32)
    seisxl = np.zeros([znum, nxlsls, inlnum], np.float32)
    seisz = np.zeros([znum, nxlsls, inlnum], np.float32)
    seisdata = np.zeros([znum, nxlsls, inlnum], np.float32)
    for i in range(nxlsls):
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nxlsls) * 100.0))
            sys.stdout.flush()
        #
        xl = xlsls[i]
        idx = np.round((xl - xlstart) / xlstep).astype(np.int32)
        if idx >= 0 and idx < xlnum:
            seisinl[:, i, :] = inl3dmat[:, idx, :]
            seisxl[:, i, :] = xl3dmat[:, idx, :]
            seisz[:, i, :] = z3dmat[:, idx, :]
            seisdata[:, i, :] = seis3dmat[:, idx, :]
    #
    if verbose:
        sys.stdout.write(' Done\n')

    seisinl = seisinl.transpose()
    seisinl = np.reshape(seisinl, [1, znum * nxlsls * inlnum])
    seisinl = seisinl.transpose()
    seisxl = seisxl.transpose()
    seisxl = np.reshape(seisxl, [1, znum * nxlsls * inlnum])
    seisxl = seisxl.transpose()
    seisz = seisz.transpose()
    seisz = np.reshape(seisz, [1, znum * nxlsls * inlnum])
    seisz = seisz.transpose()
    seisdata = seisdata.transpose()
    seisdata = np.reshape(seisdata, [1, znum * nxlsls * inlnum])
    seisdata = seisdata.transpose()

    seisdata = np.concatenate((seisinl, seisxl, seisz, seisdata), axis=1)

    return seisdata


def retrieveSeisXLSliceFrom3DMat(seis3dmat, xlsls=None, seisinfo=None,
                                 verbose=True):
    """
    Retrieve seismic data along specified crossline slices from 3D matrix
    Argus:
        seisddmat:  seismic data in 3D matrix [Z/XL/IL]
        inlsls:     list of crossline slices in array [xl1, xl2, ...]
                    Retrieve all crossline slices if not specified
        seisinfo:   basic information of 3D seismic survey
                    Auto-generated from 3D seismic matrix if not specified
        verbose:    flag for message display. Default is True
    Return:
        seisdata:   seismic data along specified inline slices
                    2D matrix of four columns [IL, XL, Z, Value]
    Note:
        Negative z is used in the vertical direction
    """

    if np.ndim(seis3dmat) != 3:
        print('ERROR in retrieveSeisXLSliceFrom3DMat: 3D seismic matrix expected')
        sys.exit()

    if seisinfo is None:
        print('WARNING in retrieveSeisXLSliceFrom3DMat: Survey info auto-generated from 3D seismic matrix')
        seisinfo = createSeisInfoFrom3DMat(seis3dmat)

    seis2dmat = convertSeis3DMatTo2DMat(seis3dmat, seisinfo)

    if xlsls is None:
        print('WARNING in retrieveSeisXLSliceFrom3DMat: to retrieve all crossline slices in 3D seismic matrix')
        seisloc = seis2dmat[:, 0:3]
        seisdata = seis2dmat[:, 3]
        seisdata = np.reshape(seisdata, [len(seisdata), 1])
        seisdata = np.concatenate((seisloc, seisdata), axis=1)
        return seisdata

    if np.ndim(xlsls) != 1:
        print('ERROR in retrieveSeisXLSliceFrom3DMat: 1D array of crossline slices expected')
        sys.exit()

    inl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=0)
    xl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=1)
    z3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=2)

    xlstart = seisinfo['XLStart']
    xlstep = seisinfo['XLStep']
    znum, xlnum, inlnum = np.shape(seis3dmat)
    if xlnum == 1:
        xlstep = 1

    nxlsls = len(xlsls)
    if verbose:
        print('Retrieve ' + str(nxlsls) + ' crossline slices')

    seisinl = np.zeros([znum, nxlsls, inlnum], np.float32)
    seisxl = np.zeros([znum, nxlsls, inlnum], np.float32)
    seisz = np.zeros([znum, nxlsls, inlnum], np.float32)
    seisdata = np.zeros([znum, nxlsls, inlnum], np.float32)
    for i in range(nxlsls):
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nxlsls) * 100.0))
            sys.stdout.flush()
        #
        xl = xlsls[i]
        idx = np.round((xl - xlstart) / xlstep).astype(np.int32)
        if idx >= 0 and idx < xlnum:
            seisinl[:, i, :] = inl3dmat[:, idx, :]
            seisxl[:, i, :] = xl3dmat[:, idx, :]
            seisz[:, i, :] = z3dmat[:, idx, :]
            seisdata[:, i, :] = seis3dmat[:, idx, :]
    #
    if verbose:
        sys.stdout.write(' Done\n')

    seisinl = seisinl.transpose()
    seisinl = np.reshape(seisinl, [1, znum * nxlsls * inlnum])
    seisinl = seisinl.transpose()
    seisxl = seisxl.transpose()
    seisxl = np.reshape(seisxl, [1, znum * nxlsls * inlnum])
    seisxl = seisxl.transpose()
    seisz = seisz.transpose()
    seisz = np.reshape(seisz, [1, znum * nxlsls * inlnum])
    seisz = seisz.transpose()
    seisdata = seisdata.transpose()
    seisdata = np.reshape(seisdata, [1, znum * nxlsls * inlnum])
    seisdata = seisdata.transpose()

    seisdata = np.concatenate((seisinl, seisxl, seisz, seisdata), axis=1)

    return seisdata


def cutSeisXLSliceFrom2DMat(seis2dmat,xlsls=None,
                            imageheight=100, imagewidth=100,
                            inlstart=None, inlend=None, inlstep=None,
                            zstart=None, zend=None, zstep=None,
                            datacol=3, inlcol=0, xlcol=1, zcol=2,
                            verbose=True):
    seisinfo = getSeisInfoFrom2DMat(seis2dmat,
                                    inlcol=inlcol, xlcol=xlcol, zcol=zcol)
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=datacol,
                                        inlcol=inlcol, xlcol=xlcol, zcol=zcol)
    #
    if xlsls is None:
        print('WARNING in cutSeisXLSliceFrom2DMat: to cut all crossline slices in 2D seismic matrix')
        inlsls = seisinfo['ILRange']
    if inlstart is None:
        inlstart = seisinfo['ILStart']
    if inlend is None:
        inlend = seisinfo['ILEnd']
    if inlstep is None:
        inlstep = seisinfo['ILStep']
    if zstart is None:
        zstart = seisinfo['ZStart']
    if zend is None:
        zend = seisinfo['ZEnd']
    if zstep is None:
        zstep = seisinfo['ZStep']

    #
    inlidx = np.arange(inlstart, inlend+1, inlstep)
    inlidx = np.round((inlidx - seisinfo['ILStart'])/seisinfo['ILStep']).astype(np.int32)
    inlidx = np.unique(inlidx)
    outidx = []
    for i in range(len(inlidx)):
        if inlidx[i] < 0 or inlidx[i] + imagewidth > seisinfo['ILNum']:
            outidx.append(i)
    inlidx = np.delete(inlidx, outidx)
    #
    zidx = np.arange(zstart, zend, zstep)
    zidx = np.round((zidx - seisinfo['ZStart']) / seisinfo['ZStep']).astype(np.int32)
    zidx = np.unique(zidx)
    outidx = []
    for i in range(len(zidx)):
        if zidx[i] < 0 or zidx[i] + imageheight > seisinfo['ZNum']:
            outidx.append(i)
    zidx = np.delete(zidx, outidx)
    #
    nxlsls = len(xlsls)
    if verbose:
        print('Cut ' + str(nxlsls) + ' crossline slices')
    ninlidx = len(inlidx)
    nzidx = len(zidx)
    #
    seisxlslicepatch = np.zeros([ninlidx, nxlsls, nzidx, imageheight, imagewidth])
    #
    for i in range(nxlsls):
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nxlsls) * 100.0))
            sys.stdout.flush()
        #
        xl = xlsls[i]
        idx = np.round((xl-seisinfo['XLStart'])/seisinfo['ILStep']).astype(np.int32)
        for j in range(ninlidx):
            for k in range(nzidx):
                seisxlslicepatch[j, i, k, :, :] = \
                    seis3dmat[zidx[k]:zidx[k]+imageheight, idx, inlidx[j]:inlidx[j]+imagewidth]
    #
    if verbose:
        sys.stdout.write(' Done\n')

    return np.reshape(seisxlslicepatch, [ninlidx, nxlsls, nzidx, imageheight*imagewidth])


def retrieveSeisZSliceFrom2DMat(seis2dmat, zsls=None, datacol=3,
                                inlcol=0, xlcol=1, zcol=2,
                                verbose=True):
    """
    Retrieve seismic data along specified z slices from 2D matrix
    Argus:
        seis2dmat:  seismic data in 2D matrix of at least four columns [IL, XL, Z, Value]
        zsls:       list of z slices in array [z1, z2, ...]
                    Retrieve all z slices if not specified
        datacol:    index of data column for retrieval (indexing from 0)
                    Default is the fourth column (3)
        inlcol:     index of inline column. Default is the first column (0)
        xlcol:      index of crossline column. Default is the second column (1)
        zcol:       index of z column. Default is the third column (2)
        verbose:    flag for message display. Default is True
    Return:
        seisdata:   seismic data along specified z slices
                    2D matrix of four columns [IL, XL, Z, Value]
    Note:
        Negative z is used in the vertical direction
    """

    # Check input matrix
    if np.ndim(seis2dmat) != 2:
        print('ERROR in retrieveSeisZSliceFrom2DMat: 2D seismic matrix expected')
        sys.exit()
    if datacol < 0 or len(seis2dmat[0, :]) <= datacol:
        print('ERROR in retrieveSeisZSliceFrom2DMat: Not data column found in 2D seismic matrix')
        sys.exit()
    if inlcol < 0 or len(seis2dmat[0, :]) <= inlcol:
        print('ERROR in retrieveSeisZSliceFrom2DMat: Not inline column found in 2D seismic matrix')
        sys.exit()
    if xlcol < 0 or len(seis2dmat[0, :]) <= xlcol:
        print('ERROR in retrieveSeisZSliceFrom2DMat: Not crossline column found in 2D seismic matrix')
        sys.exit()
    if zcol < 0 or len(seis2dmat[0, :]) <= zcol:
        print('ERROR in retrieveSeisZSliceFrom2DMat: Not z column found in 2D seismic matrix')
        sys.exit()

    if zsls is None:
        print('WARNING in retrieveSeisZSliceFrom2DMat: to retrieve all z slices in 2D seismic matrix')
        inlloc = seis2dmat[:, inlcol]
        xlloc = seis2dmat[:, xlcol]
        zloc = seis2dmat[:, zcol]
        seisdata = seis2dmat[:, datacol]
        seisdata = np.reshape(seisdata, [len(seisdata), 1])
        seisdata = np.concatenate((inlloc, xlloc, zloc, seisdata), axis=1)
        return seisdata

    if np.ndim(zsls) != 1:
        print('ERROR in retrieveSeisZSliceFrom2DMat: 1D array for z slices expected')
        sys.exit()

    seisinfo = getSeisInfoFrom2DMat(seis2dmat,
                                    inlcol=inlcol, xlcol=xlcol, zcol=zcol)

    inl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=inlcol,
                                       inlcol=inlcol, xlcol=xlcol, zcol=zcol)
    xl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=xlcol,
                                      inlcol=inlcol, xlcol=xlcol, zcol=zcol)
    z3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=2,
                                     inlcol=inlcol, xlcol=xlcol, zcol=zcol)
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=datacol,
                                        inlcol=inlcol, xlcol=xlcol, zcol=zcol)

    zstart = seisinfo['ZStart']
    zstep = seisinfo['ZStep']
    znum, xlnum, inlnum = np.shape(seis3dmat)
    if znum == 1:
        zstep = -1

    nzsls = len(zsls)
    if verbose:
        print('Retrieve ' + str(nzsls) + ' z slices')

    seisinl = np.zeros([nzsls, xlnum, inlnum], np.float32)
    seisxl = np.zeros([nzsls, xlnum, inlnum], np.float32)
    seisz = np.zeros([nzsls, xlnum, inlnum], np.float32)
    seisdata = np.zeros([nzsls, xlnum, inlnum], np.float32)
    for i in range(nzsls):
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nzsls) * 100.0))
            sys.stdout.flush()
        #
        z = zsls[i]
        idx = np.round((z - zstart) / zstep).astype(np.int32)
        if idx >= 0 and idx < znum:
            seisinl[i, :, :] = inl3dmat[idx, :, :]
            seisxl[i, :, :] = xl3dmat[idx, :, :]
            seisz[i, :, :] = z3dmat[idx, :, :]
            seisdata[i, :, :] = seis3dmat[idx, :, :]
    #
    if verbose:
        sys.stdout.write(' Done\n')

    seisinl = seisinl.transpose()
    seisinl = np.reshape(seisinl, [1, nzsls * xlnum * inlnum])
    seisinl = seisinl.transpose()
    seisxl = seisxl.transpose()
    seisxl = np.reshape(seisxl, [1, nzsls * xlnum * inlnum])
    seisxl = seisxl.transpose()
    seisz = seisz.transpose()
    seisz = np.reshape(seisz, [1, nzsls * xlnum * inlnum])
    seisz = seisz.transpose()
    seisdata = seisdata.transpose()
    seisdata = np.reshape(seisdata, [1, nzsls * xlnum * inlnum])
    seisdata = seisdata.transpose()

    seisdata = np.concatenate((seisinl, seisxl, seisz, seisdata), axis=1)

    return seisdata


def retrieveSeisZSliceFrom3DMat(seis3dmat, zsls=None, seisinfo=None,
                                verbose=True):
    """
    Retrieve seismic data along specified z slices from 3D matrix
    Argus:
        seisddmat:  seismic data in 3D matrix [Z/XL/IL]
        zlsls:      list of z slices in array [z1, z2, ...]
                    Retrieve all z slices if not specified
        seisinfo:   basic information of 3D seismic survey
                    Auto-generated from 3D seismic matrix if not specified
        verbose:    flag for message display. Default is True
    Return:
        seisdata:   seismic data along specified inline slices
                    2D matrix of four columns [IL, XL, Z, Value]
    Note:
        Negative z is used in the vertical direction
    """

    if np.ndim(seis3dmat) != 3:
        print('ERROR in retrieveSeisZSliceFrom3DMat: 3D seismic matrix expected')
        sys.exit()

    if seisinfo is None:
        print('WARNING in retrieveSeisZSliceFrom3DMat: Survey info auto-generated from 3D seismic matrix')
        seisinfo = createSeisInfoFrom3DMat(seis3dmat)

    seis2dmat = convertSeis3DMatTo2DMat(seis3dmat, seisinfo)

    if zsls is None:
        print('WARNING in retrieveSeisZSliceFrom3DMat: to retrieve all z slices')
        seisloc = seis2dmat[:, 0:3]
        seisdata = seis2dmat[:, 3]
        seisdata = np.reshape(seisdata, [len(seisdata), 1])
        seisdata = np.concatenate((seisloc, seisdata), axis=1)
        return seisdata

    if np.ndim(zsls) != 1:
        print('ERROR in retrieveSeisZSliceFrom3DMat: 1D array of z slices expected')
        sys.exit()

    inl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=0)
    xl3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=1)
    z3dmat = convertSeis2DMatTo3DMat(seis2dmat, datacol=2)

    zstart = seisinfo['ZStart']
    zstep = seisinfo['ZStep']
    znum, xlnum, inlnum = np.shape(seis3dmat)
    if znum == 1:
        zstep = -1

    nzsls = len(zsls)
    if verbose:
        print('Retrieve ' + str(nzsls) + ' z slices')

    seisinl = np.zeros([nzsls, xlnum, inlnum], np.float32)
    seisxl = np.zeros([nzsls, xlnum, inlnum], np.float32)
    seisz = np.zeros([nzsls, xlnum, inlnum], np.float32)
    seisdata = np.zeros([nzsls, xlnum, inlnum], np.float32)
    for i in range(nzsls):
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nzsls) * 100.0))
            sys.stdout.flush()
        #
        z = zsls[i]
        idx = np.round((z - zstart) / zstep).astype(np.int32)
        if idx >= 0 and idx < znum:
            seisinl[i, :, :] = inl3dmat[idx, :, :]
            seisxl[i, :, :] = xl3dmat[idx, :, :]
            seisz[i, :, :] = z3dmat[idx, :, :]
            seisdata[i, :, :] = seis3dmat[idx, :, :]
    #
    if verbose:
        sys.stdout.write(' Done\n')

    seisinl = seisinl.transpose()
    seisinl = np.reshape(seisinl, [1, nzsls * xlnum * inlnum])
    seisinl = seisinl.transpose()
    seisxl = seisxl.transpose()
    seisxl = np.reshape(seisxl, [1, nzsls * xlnum * inlnum])
    seisxl = seisxl.transpose()
    seisz = seisz.transpose()
    seisz = np.reshape(seisz, [1, nzsls * xlnum * inlnum])
    seisz = seisz.transpose()
    seisdata = seisdata.transpose()
    seisdata = np.reshape(seisdata, [1, nzsls * xlnum * inlnum])
    seisdata = seisdata.transpose()

    seisdata = np.concatenate((seisinl, seisxl, seisz, seisdata), axis=1)

    return seisdata


def retrieveSeisWindowFrom2DMat(seis2dmat, wdctrs, datacol=3,
                                inlcol=0, xlcol=1, zcol=2,
                                wdinl=0, wdxl=0, wdz=0,
                                verbose=True, qpgsdlg=None):
    """
    Retrieve seismic data in a specified window from 2D matrix
    Argus:
        seis2dmat:  seismic data in 2D matrix of at least four columns [IL, XL, Z, Value, ...]
        wdctrs:     list of window centers in 2D matrix of three columns [IL, XL, Z]
        datacol:    index of data column for retrieval (indexing from 0)
                    Default is the fourth column (3)
        inlcol:     index of inline column. Default is the first column (0)
        xlcol:      index of crossline column. Default is the second column (1)
        zcol:       index of z column. Default is the third column (2)
        wdinl:      window radius along inline direction. Default is 0
        wdxl:       window radius along crossline direction. Default is 0
        wdz:        window radius along z direction. Default is 0
        verbose:    flag for message display. Default is True
        qpgsdlg:    QProgressDialog for displaying progress. Default is None
    Return:
        seisdata:   seismic data in a specified window
                    2D matrix of four columns [IL, XL, Z, WD1, WD2, WD3, ...]
    Note:
        Negative z is used in the vertical direction
    """

    # Check input matrix
    if np.ndim(seis2dmat) != 2:
        print('ERROR in retrieveSeisWindowFrom2DMat: 2D seismic matrix expected')
        sys.exit()
    if datacol < 0 or len(seis2dmat[0, :]) <= datacol:
        print('ERROR in retrieveSeisWindowFrom2DMat: Not data column found in 2D seismic matrix')
        sys.exit()
    if inlcol < 0 or len(seis2dmat[0, :]) < inlcol:
        print('ERROR in retrieveSeisWindowFrom2DMat: No inline column found in 2D seismic matrix')
        sys.exit()
    if xlcol < 0 or len(seis2dmat[0, :]) < xlcol:
        print('ERROR in retrieveSeisWindowFrom2DMat: No crossline column found in 2D seismic matrix')
        sys.exit()
    if zcol < 0 or len(seis2dmat[0, :]) < zcol:
        print('ERROR in retrieveSeisWindowFrom2DMat: No z column found in 2D seismic matrix')
        sys.exit()

    if np.ndim(wdctrs) != 2:
        print('ERROR in retrieveSeisWindowFrom2DMat: 2D matrix of window centers expected')
        sys.exit()
    if len(wdctrs[0, :]) < 3:
        print('ERROR in retrieveSeisWindowFrom2DMat: 3 columns expected in 2D window-center matrix')
        sys.exit()

    if wdinl < 0 or wdxl < 0 or wdz < 0:
        print('ERROR in retrieveSeisWindowFrom2DMat: Wrong window size')
        sys.exit()

    seisinfo = getSeisInfoFrom2DMat(seis2dmat,
                                    inlcol=inlcol, xlcol=xlcol, zcol=zcol)
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat,
                                        datacol=datacol,
                                        inlcol=inlcol, xlcol=xlcol, zcol=zcol)
    inlstart = seisinfo['ILStart']
    inlstep = seisinfo['ILStep']
    inlnum = seisinfo['ILNum']
    xlstart = seisinfo['XLStart']
    xlstep = seisinfo['XLStep']
    xlnum = seisinfo['XLNum']
    zstart = seisinfo['ZStart']
    zstep = seisinfo['ZStep']
    znum = seisinfo['ZNum']
    if inlnum == 1:
        inlstep = 1
    if xlnum == 1:
        xlstep = 1
    if znum == 1:
        zstep = -1

    nwdctr, _ = np.shape(wdctrs)
    if verbose:
        print('Retrieve ' + str(nwdctr) + ' window centers')

    wdinlsize = 2 * wdinl + 1
    wdxlsize = 2 * wdxl + 1
    wdzsize = 2 * wdz + 1
    wdsize = wdinlsize * wdxlsize * wdzsize

    if qpgsdlg is not None:
        qpgsdlg.setMaximum(nwdctr)

    seisdata = np.zeros([nwdctr, 3+wdsize], np.float32)
    for i in range(nwdctr):
        #
        if qpgsdlg is not None:
            QtCore.QCoreApplication.instance().processEvents()
            qpgsdlg.setValue(i)
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nwdctr) * 100.0))
            sys.stdout.flush()
        #
        inl = wdctrs[i, 0]
        xl = wdctrs[i, 1]
        z = wdctrs[i, 2]

        inlidx = np.round((inl - inlstart) / inlstep).astype(np.int32)
        xlidx = np.round((xl - xlstart) / xlstep).astype(np.int32)
        zidx = np.round((z - zstart) / zstep).astype(np.int32)

        if inlidx >= wdinl and inlidx < inlnum-wdinl and xlidx >= wdxl and xlidx < xlnum-wdxl \
                and zidx >= wdz and zidx < znum-wdz:
            idx = inlidx * xlnum * znum + xlidx * znum + zidx
            seisdata[i, 0] = seis2dmat[idx, inlcol]
            seisdata[i, 1] = seis2dmat[idx, xlcol]
            seisdata[i, 2] = seis2dmat[idx, zcol]
            seiswd = seis3dmat[zidx-wdz:zidx+wdz+1, xlidx-wdxl:xlidx+wdxl+1 ,inlidx-wdinl:inlidx+wdinl+1]
            seisdata[i, 3:3+wdsize] = np.reshape(seiswd, [1, wdsize])

            # for a, b, c in [(a, b, c) for a in range(wdzsize) for b in range(wdxlsize) for c in range(wdinlsize)]:
            #     seisdata[i, 3+a*wdxlsize*wdinlsize+b*wdinlsize+c] = \
            #         seis2dmat[idx+(c-wdinl)*xlnum*znum+(b-wdxl)*znum+(a-wdz), datacol]
    #
    if qpgsdlg is not None:
        qpgsdlg.setValue(nwdctr)
    if verbose:
        sys.stdout.write(' Done\n')

    return seisdata


def assignSeisWindowTo2DMat(seis2dmat, seiswd, wdinl=0, wdxl=0, wdz=0, verbose=True):

    seisinfo = getSeisInfoFrom2DMat(seis2dmat)
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat)
    #
    inlstart = seisinfo['ILStart']
    inlstep = seisinfo['ILStep']
    inlnum = seisinfo['ILNum']
    xlstart = seisinfo['XLStart']
    xlstep = seisinfo['XLStep']
    xlnum = seisinfo['XLNum']
    zstart = seisinfo['ZStart']
    zstep = seisinfo['ZStep']
    znum = seisinfo['ZNum']
    #

    #
    nwd = np.shape(seiswd)[0]
    inlsize = 2 * wdinl + 1
    xlsize = 2 * wdxl + 1
    zsize = 2 * wdz + 1
    if verbose:
        print('Assign ' + str(nwd) + ' windows')
    for i in range(nwd):
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nwd) * 100.0))
            sys.stdout.flush()
        #
        inl = seiswd[i, 0]
        xl = seiswd[i, 1]
        z = seiswd[i, 2]
        inlidx = int((inl - inlstart) / inlstep)
        xlidx = int((xl-xlstart) / xlstep)
        zidx = int((z-zstart) / zstep)
        #
        # seisdata = retrieveSeisWindowFrom3DMat(seis3dmat, seiswd[i:i+1, 0:3],
        #                                        seisinfo=seisinfo,
        #                                        wdinl=wdinl, wdxl=wdxl, wdz=wdz,
        #                                        verbose=False)
        # for j in range(inlsize*xlsize*zsize):
        #     if seisdata[0, 3+j] == 0.0:
        #         seisdata[0, 3+j] = seiswd[i, 3+j]
        #     seisdata[0, 3+j] = 0.5 * (seisdata[0, 3+j]+seiswd[i, 3+j])
        # seisdata = np.reshape(seisdata[0, 3:], [zsize, xlsize, inlsize])
        #
        if inlidx >= wdinl and inlidx < inlnum - wdinl and xlidx >= wdxl and xlidx < xlnum - wdxl \
                and zidx >= wdz and zidx < znum - wdz:
            seisdata = seis3dmat[zidx-wdz:zidx+wdz+1, xlidx-wdxl:xlidx+wdxl+1, inlidx-wdinl:inlidx+wdinl+1]
            seisdata = np.reshape(seisdata, [inlsize*xlsize*zsize])
            #
            for j in range(inlsize * xlsize * zsize):
                if seisdata[j] == 0.0:
                    seisdata[j] = seiswd[i, 3 + j]
                seisdata[j] = 0.5 * (seisdata[j] + seiswd[i, 3 + j])
            seisdata = np.reshape(seisdata, [zsize, xlsize, inlsize])
            #
            seis3dmat[zidx-wdz:zidx+wdz+1, xlidx-wdxl:xlidx+wdxl+1, inlidx-wdinl:inlidx+wdinl+1] = seisdata
    #
    if verbose:
        sys.stdout.write(' Done\n')
    #
    return convertSeis3DMatTo2DMat(seis3dmat, seisinfo)


def retrieveSeisWindowFrom3DMat(seis3dmat, wdctrs, seisinfo=None,
                                wdinl=0, wdxl=0, wdz=0,
                                verbose=True, qpgsdlg=None):
    """
    Retrieve seismic data in a specified window from 3D matrix
    Argus:
        seis3dmat:  seismic data in 3D matrix [Z/XL/IL]
        wdctrs:     list of window centers in 2D matrix of three columns [IL, XL, Z]
        seisinfo:   basic information of 3D seismic survey
                    Auto-generated from 3D seismic matrix if not specified
        wdinl:      window radius along inline direction. Default is 0
        wdxl:       window radius along crossline direction. Default is 0
        wdz:        window radius along z direction. Default is 0
        verbose:    flag for message display. Default is True
        qpgsdlg:    QProgressDialog for displaying progress. Default is None
    Return:
        seisdata:   seismic data on specified samples
                    2D matrix of four columns [IL, XL, Z, Value]
    Note:
        Negative z is used in the vertical direction
    """

    if np.ndim(seis3dmat) != 3:
        print('ERROR in retrieveSeisWindowFrom3DMat: 3D seismic matrix expected')
        sys.exit()

    if seisinfo is None:
        print('WARNING in retrieveSeisWindowFrom3DMat: Survey info auto-generated from 3D seismic matrix')
        seisinfo = createSeisInfoFrom3DMat(seis3dmat)

    if np.ndim(wdctrs) != 2:
        print('ERROR in retrieveSeisWindowFrom3DMat: 2D matrix of window centers expected')
        sys.exit()
    if len(wdctrs[0, :]) < 3:
        print('ERROR in retrieveSeisWindowFrom3DMat: 3-column window-center list expected')
        sys.exit()

    if wdinl<0 or wdxl<0 or wdz<0:
        print('ERROR in retrieveSeisWindowFrom3DMat: Wrong window size')
        sys.exit()

    inlstart = seisinfo['ILStart']
    inlstep = seisinfo['ILStep']
    inlnum = seisinfo['ILNum']
    xlstart = seisinfo['XLStart']
    xlstep = seisinfo['XLStep']
    xlnum = seisinfo['XLNum']
    zstart = seisinfo['ZStart']
    zstep = seisinfo['ZStep']
    znum = seisinfo['ZNum']
    if inlnum == 1:
        inlstep = 1
    if xlnum == 1:
        xlstep = 1
    if znum == 1:
        zstep = -1

    nwdctr, _ = np.shape(wdctrs)
    if verbose:
        print('Retrieve ' + str(nwdctr) + ' window centers')

    wdinlsize = 2 * wdinl + 1
    wdxlsize = 2 * wdxl + 1
    wdzsize = 2 * wdz + 1
    wdsize = wdinlsize * wdxlsize * wdzsize

    if qpgsdlg is not None:
        qpgsdlg.setMaximum(nwdctr)

    seisdata = np.zeros([nwdctr, 3 + wdsize], np.float32)
    for i in range(nwdctr):
        #
        if qpgsdlg is not None:
            QtCore.QCoreApplication.instance().processEvents()
            qpgsdlg.setValue(i)
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(nwdctr) * 100.0))
            sys.stdout.flush()
        #
        inl = wdctrs[i, 0]
        xl = wdctrs[i, 1]
        z = wdctrs[i, 2]

        inlidx = np.round((inl - inlstart) / inlstep).astype(np.int32)
        xlidx = np.round((xl - xlstart) / xlstep).astype(np.int32)
        zidx = np.round((z - zstart) / zstep).astype(np.int32)

        if inlidx >= wdinl and inlidx < inlnum-wdinl and xlidx >= wdxl and xlidx < xlnum-wdxl \
                and zidx >= wdz and zidx < znum-wdz:
            idx = inlidx * xlnum * znum + xlidx * znum + zidx
            seisdata[i, 0] = inlidx * inlstep + inlstart
            seisdata[i, 1] = xlidx * xlstep + xlstart
            seisdata[i, 2] = zidx * zstep + zstart
            seiswd = seis3dmat[zidx-wdz:zidx+wdz+1, xlidx-wdxl:xlidx+wdxl+1 ,inlidx-wdinl:inlidx+wdinl+1]
            seisdata[i, 3:3+wdsize] = np.reshape(seiswd, [1, wdsize])

            # for a, b, c in [(a, b, c) for a in range(wdzsize) for b in range(wdxlsize) for c in range(wdinlsize)]:
            #     seisdata[i, 3+a*wdxlsize*wdinlsize+b*wdinlsize+c] = \
            #         seis2dmat[idx+(c-wdinl)*xlnum*znum+(b-wdxl)*znum+(a-wdz), datacol]
    #
    #
    if qpgsdlg is not None:
        qpgsdlg.setValue(nwdctr)
    if verbose:
        sys.stdout.write(' DOne\n')

    return seisdata


def retrieveSeisILTraceFrom2DMat(seis2dmat, trctrs, wdxl=0, wdz=0, verbose=False):
    #
    ntrace = np.shape(trctrs)[0]
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat)
    seisinfo = getSeisInfoFrom2DMat(seis2dmat)
    znum, xlnum, inlnum = np.shape(seis3dmat)
    #
    rst = np.zeros([ntrace, 2+ inlnum*(2*wdxl+1)*(2*wdz+1)])
    rst[:, 0:2] = trctrs
    #
    if verbose:
        print('Retrieve ' + str(ntrace) + ' z traces')
    #
    for i in range(ntrace):
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(ntrace) * 100.0))
            sys.stdout.flush()
        #
        xl = trctrs[i, 0]
        z = trctrs[i, 1]
        xl = (xl - seisinfo['XLStart']) / seisinfo['XLStep']
        xl = int(xl)
        z = (z - seisinfo['ZStart']) / seisinfo['ZStep']
        z = int(z)
        if (xl-wdxl)>=0 and (xl+wdxl)<seisinfo['XLNum'] and (z-wdz)>=0 and (z+wdz)<seisinfo['ZNum']:
            dat = seis3dmat[z-wdz:z+wdz+1, xl-wdxl:xl+wdxl+1, :]
            rst[i, 2:] = np.reshape(dat, [1, -1])
    #
    if verbose:
        sys.stdout.write(' Done\n')
    #
    return rst


def retrieveSeisILTraceFrom3DMat(seis3dmat, trctrs, wdxl=0, wdz=0, seisinfo=None, verbose=False):
    #
    if (seisinfo is None) or (checkSeisInfo(seisinfo) is False):
        print("Warning in retrieveSeisILTraceFrom3DMat: SeisInfo automatically generated")
    #
    ntrace = np.shape(trctrs)[0]
    znum, xlnum, inlnum = np.shape(seis3dmat)
    #
    rst = np.zeros([ntrace, 2+ inlnum*(2*wdxl+1)*(2*wdz+1)])
    rst[:, 0:2] = trctrs
    #
    if verbose:
        print('Retrieve ' + str(ntrace) + ' z traces')
    #
    for i in range(ntrace):
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(ntrace) * 100.0))
            sys.stdout.flush()
        #
        xl = trctrs[i, 0]
        z = trctrs[i, 1]
        xl = (xl - seisinfo['XLStart']) / seisinfo['XLStep']
        xl = int(xl)
        z = (z - seisinfo['ZStart']) / seisinfo['ZStep']
        z = int(z)
        if (xl-wdxl)>=0 and (xl+wdxl)<seisinfo['XLNum'] and (z-wdz)>=0 and (z+wdz)<seisinfo['ZNum']:
            dat = seis3dmat[z-wdz:z+wdz+1, xl-wdxl:xl+wdxl+1, :]
            rst[i, 2:] = np.reshape(dat, [1, -1])
    #
    if verbose:
        sys.stdout.write(' Done\n')
    #
    return rst


def retrieveSeisXLTraceFrom2DMat(seis2dmat, trctrs, wdinl=0, wdz=0, verbose=False):
    #
    ntrace = np.shape(trctrs)[0]
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat)
    seisinfo = getSeisInfoFrom2DMat(seis2dmat)
    znum, xlnum, inlnum = np.shape(seis3dmat)
    #
    rst = np.zeros([ntrace, 2+ xlnum*(2*wdinl+1)*(2*wdz+1)])
    rst[:, 0:2] = trctrs
    #
    if verbose:
        print('Retrieve ' + str(ntrace) + ' z traces')
    #
    for i in range(ntrace):
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(ntrace) * 100.0))
            sys.stdout.flush()
        #
        inl = trctrs[i, 0]
        z = trctrs[i, 1]
        inl = (inl - seisinfo['ILStart']) / seisinfo['ILStep']
        inl = int(inl)
        z = (z - seisinfo['ZStart']) / seisinfo['ZStep']
        z = int(z)
        if (inl-wdinl)>=0 and (inl+wdinl)<seisinfo['ILNum'] and (z-wdz)>=0 and (z+wdz)<seisinfo['ZNum']:
            dat = seis3dmat[z-wdz:z+wdz+1, :, inl-wdinl:inl+wdinl+1]
            rst[i, 2:] = np.reshape(dat, [1, -1])
    #
    if verbose:
        sys.stdout.write(' Done\n')
    #
    return rst


def retrieveSeisXLTraceFrom3DMat(seis3dmat, trctrs, wdinl=0, wdz=0, seisinfo=None, verbose=False):
    #
    if (seisinfo is None) or (checkSeisInfo(seisinfo) is False):
        print("Warning in retrieveSeisXLTraceFrom3DMat: SeisInfo automatically generated")
    #
    ntrace = np.shape(trctrs)[0]

    znum, xlnum, inlnum = np.shape(seis3dmat)
    #
    rst = np.zeros([ntrace, 2+ xlnum*(2*wdinl+1)*(2*wdz+1)])
    rst[:, 0:2] = trctrs
    #
    if verbose:
        print('Retrieve ' + str(ntrace) + ' z traces')
    #
    for i in range(ntrace):
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(ntrace) * 100.0))
            sys.stdout.flush()
        #
        inl = trctrs[i, 0]
        z = trctrs[i, 1]
        inl = (inl - seisinfo['ILStart']) / seisinfo['ILStep']
        inl = int(inl)
        z = (z - seisinfo['ZStart']) / seisinfo['ZStep']
        z = int(z)
        if (inl-wdinl)>=0 and (inl+wdinl)<seisinfo['ILNum'] and (z-wdz)>=0 and (z+wdz)<seisinfo['ZNum']:
            dat = seis3dmat[z-wdz:z+wdz+1, :, inl-wdinl:inl+wdinl+1]
            rst[i, 2:] = np.reshape(dat, [1, -1])
    #
    if verbose:
        sys.stdout.write(' Done\n')
    #
    return rst


def retrieveSeisZTraceFrom2DMat(seis2dmat, trctrs, wdinl=0, wdxl=0, verbose=False):
    #
    ntrace = np.shape(trctrs)[0]
    seis3dmat = convertSeis2DMatTo3DMat(seis2dmat)
    seisinfo = getSeisInfoFrom2DMat(seis2dmat)
    znum, xlnum, inlnum = np.shape(seis3dmat)
    #
    rst = np.zeros([ntrace, 2+ znum*(2*wdinl+1)*(2*wdxl+1)])
    rst[:, 0:2] = trctrs
    #
    if verbose:
        print('Retrieve ' + str(trctrs) + ' z traces')
    #
    for i in range(ntrace):
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(ntrace) * 100.0))
            sys.stdout.flush()
        #
        inl = trctrs[i, 0]
        xl = trctrs[i, 1]
        inl = (inl - seisinfo['ILStart']) / seisinfo['ILStep']
        inl = int(inl)
        xl = (xl - seisinfo['XLStart']) / seisinfo['XLStep']
        xl = int(xl)
        if (inl-wdinl)>=0 and (inl+wdinl)<seisinfo['ILNum'] and (xl-wdxl)>=0 and (xl+wdxl)<seisinfo['XLNum']:
            dat = seis3dmat[:, xl-wdxl:xl+wdxl+1, inl-wdinl:inl+wdinl+1]
            rst[i, 2:] = np.reshape(dat, [1, -1])
    #
    if verbose:
        sys.stdout.write(' Done\n')
    #
    return rst


def retrieveSeisZTraceFrom3DMat(seis3dmat, trctrs, seisinfo=None, wdinl=0, wdxl=0, verbose=False):
    if (seisinfo is None) or (checkSeisInfo(seisinfo) is False):
        print("Warning in retrieveSeisZTraceFrom3DMat: SeisInfo automatically generated")
    #
    ntrace = np.shape(trctrs)[0]
    znum, xlnum, inlnum = np.shape(seis3dmat)
    #
    rst = np.zeros([ntrace, 2 + znum*(2*wdinl+1)*(2*wdxl+1)])
    rst[:, 0:2] = trctrs
    #
    if verbose:
        print('Retrieve ' + str(ntrace) + ' z traces')
    #
    for i in range(ntrace):
        #
        if verbose:
            sys.stdout.write('\r>>> Process %.1f%%' % (float(i) / float(ntrace) * 100.0))
            sys.stdout.flush()
        #
        inl = trctrs[i, 0]
        xl = trctrs[i, 1]
        inl = (inl - seisinfo['ILStart']) / seisinfo['ILStep']
        inl = int(inl)
        xl = (xl - seisinfo['XLStart']) / seisinfo['XLStep']
        xl = int(xl)
        if (inl-wdinl)>=0 and (inl+wdinl)<seisinfo['ILNum'] and (xl-wdxl)>=0 and (xl+wdxl)<seisinfo['XLNum']:
            dat = seis3dmat[:, xl-wdxl:xl+wdxl+1, inl-wdinl:inl+wdinl+1]
            rst[i, 2:] = np.reshape(dat, [1, -1])
    #
    if verbose:
        sys.stdout.write(' Done\n')
    #
    return rst


def removeOutofSurveySample(pts, inlstart=0, inlend=100, xlstart=0, xlend=100, zstart=0, zend=-1000):
    pts_in = []
    npts = np.shape(pts)[0]
    for i in range(npts):
        if pts[i, 0] >= inlstart and pts[i, 0] <= inlend \
            and pts[i, 1] >= xlstart and pts[i, 1] <= xlend \
            and pts[i, 2] <= zstart and pts[i, 2] >= zend:
            pts_in.append(pts[i, :])
    return np.array(pts_in)


def removeOutofSurveyXLTrace(tcs, inlstart=0, inlend=100, zstart=0, zend=-1000):
    tcs_in = []
    ntc = np.shape(tcs)[0]
    for i in range(ntc):
        if tcs[i, 0] >= inlstart and tcs[i, 0] <= inlend \
            and tcs[i, 1] <= zstart and tcs[i, 1] >= zend:
            tcs_in.append(tcs[i, :])
    return np.array(tcs_in)


def removeOutofSurveyZTrace(tcs, inlstart=0, inlend=100, xlstart=0, xlend=100):
    tcs_in = []
    ntc = np.shape(tcs)[0]
    for i in range(ntc):
        if tcs[i, 0] >= inlstart and tcs[i, 0] <= inlend \
            and tcs[i, 1] >= xlstart and tcs[i, 1] <= xlend :
            tcs_in.append(tcs[i, :])
    return np.array(tcs_in)


def isOutOfSurvey(ixzlist, inlstart=0, inlend=100, xlstart=0, xlend=100, zstart=0, zend=-1000):
    """
    check if given sample out of seismic survey
    Args:
        ixzlist:    2D array of sample lists of 3 columns [IL, XL, Z]
        inlstart:   start inline number. Default is 0
        inlend:     end inline number. Default is 100
        xlstart:    start crossline number. Default is 0
        xlend:      end crossline number. Default is 100
        zstart:     start z in ms. Default is 0
        zend:       end z in ms. Default is -1000
    Return:
        1D array for the samples. positive for out of survey; 0 for on the boundary; negative for inside
    Note:
        Negative z is used in the vertical direction
    """

    if np.ndim(ixzlist) < 2 or np.shape(ixzlist)[1] < 3:
        print('ERROR in isOutOfSurvey: 2-D matrix of at least 3 columns expected')
        sys.exit()

    nsample = np.shape(ixzlist)[0]
    flags = np.zeros([nsample, 1])
    for i in range(nsample):
        il = ixzlist[i, 0]
        xl = ixzlist[i, 1]
        z = ixzlist[i, 2]
        # Out of survey
        if il < inlstart or il > inlend \
            or xl < xlstart or xl > xlend \
            or z > zstart or z < zend:
            flags[i] = 1
        # Inside survey
        if il > inlstart and il < inlend \
            and xl > xlstart and xl < xlend \
            and z < zstart and z > zend:
            flags[i] = -1
    #
    return flags


def convertIXZToIJK(ixz, inlstart=0, inlstep=1, xlstart=0, xlstep=1, zstart=0, zstep=-1):
    """
    Convert inline/crossline/z [IL, XL, Z] to index [I, J, K]
    Args:
        ixz:        2D matrix of inline/crossline/z
        inlstart:   start inline
        inlstep:    inline step
        xlstart:    start crossline
        xlstep:     crossline step
        zstart:     start z in ms
        zstep:      z step in ms
    Return:
        2D array for index [I, J, K]
    Note:
        Negative z is used in the vertical direction
    """
    if np.ndim(ixz) < 2 or np.shape(ixz)[1] < 3:
        print('ERROR in convertIXZToIJK: 2-D matrix of at least 3 columns expected')
        sys.exit()
    if inlstep <= 0 or xlstep <= 0 or zstep >= 0:
        print('ERROR in convertIXZToIJK: wrong inline/crossline/z step')
        sys.exit()

    ijk = ixz
    if np.shape(ijk)[0] > 0:
        ijk[:, 0] = (ixz[:, 0] - inlstart) / inlstep
        ijk[:, 1] = (ixz[:, 1] - xlstart) / xlstep
        ijk[:, 2] = (ixz[:, 2] - zstart) / zstep

    # ijk = ijk.astype(int)

    return ijk


def convertIJKToIXZ(ijk, inlstart=0, inlstep=1, xlstart=0, xlstep=1, zstart=0, zstep=-1):
    """
    Convert index [I, J, K] to inline/crossline/z [IL, XL, Z]
    Args:
        ijk:        2D matrix of [I, J, K]
        inlstart:   start inline
        inlstep:    inline step
        xlstart:    start crossline
        xlstep:     crossline step
        zstart:     start z in ms
        zstep:      z step in ms
    Return:
        2D array for [IL, XL, Z]
    Note:
        Negative z is used in the vertical direction
    """
    if np.ndim(ijk) < 2 or np.shape(ijk)[1] < 3:
        print('ERROR in convertIJKToIXZ: 2-D matrix of at least 3 columns expected')
        sys.exit()


    ixz = ijk
    if np.shape(ijk)[0] > 0:
        ixz[:, 0] = ijk[:, 0] * inlstep + inlstart
        ixz[:, 1] = ijk[:, 1] * xlstep + xlstart
        ixz[:, 2] = ijk[:, 2] * zstep + zstart

    # ijk = ijk.astype(int)

    return ixz


class analysis:
    # pack all functions as a class
    #
    getSeisInfoFrom2DMat = getSeisInfoFrom2DMat
    #
    checkSeisInfo = checkSeisInfo
    makeSeisInfo = makeSeisInfo
    #
    createSeisInfoFrom3DMat = createSeisInfoFrom3DMat
    convertSeis2DMatTo3DMat = convertSeis2DMatTo3DMat
    convertSeis3DMatTo2DMat = convertSeis3DMatTo2DMat
    convertSeisInfoTo2DMat = convertSeisInfoTo2DMat
    #
    retrieveSeisSampleFrom2DMat = retrieveSeisSampleFrom2DMat
    retrieveSeisSampleFrom3DMat = retrieveSeisSampleFrom3DMat
    retrieveSeisILSliceFrom2DMat = retrieveSeisILSliceFrom2DMat
    retrieveSeisILSliceFrom3DMat = retrieveSeisILSliceFrom3DMat
    retrieveSeisXLSliceFrom2DMat = retrieveSeisXLSliceFrom2DMat
    retrieveSeisXLSliceFrom3DMat = retrieveSeisXLSliceFrom3DMat
    retrieveSeisZSliceFrom2DMat = retrieveSeisZSliceFrom2DMat
    retrieveSeisZSliceFrom3DMat = retrieveSeisZSliceFrom3DMat
    retrieveSeisWindowFrom2DMat = retrieveSeisWindowFrom2DMat
    retrieveSeisWindowFrom3DMat = retrieveSeisWindowFrom3DMat
    retrieveSeisILTraceFrom2DMat = retrieveSeisILTraceFrom2DMat
    retrieveSeisILTraceFrom3DMat = retrieveSeisILTraceFrom3DMat
    retrieveSeisXLTraceFrom2DMat = retrieveSeisXLTraceFrom2DMat
    retrieveSeisXLTraceFrom3DMat = retrieveSeisXLTraceFrom3DMat
    retrieveSeisZTraceFrom2DMat = retrieveSeisZTraceFrom2DMat
    retrieveSeisZTraceFrom3DMat = retrieveSeisZTraceFrom3DMat
    cutSeisILSliceFrom2DMat = cutSeisILSliceFrom2DMat
    cutSeisXLSliceFrom2DMat = cutSeisXLSliceFrom2DMat
    assignSeisWindowTo2DMat = assignSeisWindowTo2DMat
    #
    removeOutofSurveySample = removeOutofSurveySample
    removeOutofSurveyXLTrace = removeOutofSurveyXLTrace
    removeOutofSurveyZTrace = removeOutofSurveyZTrace
    isOutOfSurvey = isOutOfSurvey
    convertIXZToIJK = convertIXZToIJK
    convertIJKToIXZ = convertIJKToIXZ

