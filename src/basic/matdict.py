#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
# Date:     March 2018                                                                      #
#                                                                                           #
#############################################################################################

# basic functions for processing python dictionary

import sys
import numpy as np


__all__ = ['matdict']


def isDictConstantRow(dict):
    """
    Check if the dictionary has the same number of rows in all keys
    Args:
        dict:   the given matrix dictionary
    Returns:
        True or false
    """

    # Check if the input dictionary be empty
    if len(dict.keys()) <= 0:
        print('ERROR in isDictConstantRow: Empty dictionary')
        sys.exit()

    firstkey = list(dict.keys())[0]
    nrow = len(dict[firstkey])

    for key in dict.keys():
        if nrow != len(dict[key]):
            print('ERROR in isDictConstantRow: ' + key + ' of inconstant row number')
            return False

    return True


def maxDictConstantRow(dict):
    """
    Return the maximum row number of a dictionary
    Args:
        dict:   the given dictionary
    Returns:
        Maximum row number
    """

    # Check if the input dictionary be empty
    if len(dict.keys()) <= 0:
        print('WARNING in maxMatDictConstantRow: Empty dictionary')
        return 0

    firstkey = list(dict.keys())[0]
    nrow = len(dict[firstkey])

    for key in dict.keys():
        if nrow > len(dict[key]):
            nrow = len(dict[key])

    return nrow


def filterDictByValue(dict, key, value=0, flag='=='):
    """
    Filter a dictionary by specified key value
    Args:
        dict:   input dictionary
        key:    key for filtering
        value:  filtering threshold. Default is 0
        flag:   threshold equation: '>=', '<=', '==', '>', '<', '!='. Default is '=='
    Returns:
        a dictionary of specified index
    """

    # Check if the input dictionary be empty
    if len(dict.keys()) <= 0:
        print('ERROR in filterDictByValue: Empty dictionary')
        sys.exit()
    if isDictConstantRow(dict) is False:
        print('ERROR in filterDictByValue: Inconstant row number found in input dictionary')
        sys.exit()

    # Check key
    if (key in dict.keys()) is False:
        print('ERROR in filterDictByValue: Specified key not found in input dictionary')
        sys.exit()

    if flag == '>=':
        idx = [k for k, v in enumerate(dict[key]) if v >= value]
    if flag == '<=':
        idx = [k for k, v in enumerate(dict[key]) if v <= value]
    if flag == '==':
        idx = [k for k, v in enumerate(dict[key]) if v == value]
    if flag == '>':
        idx = [k for k, v in enumerate(dict[key]) if v > value]
    if flag == '<':
        idx = [k for k, v in enumerate(dict[key]) if v < value]
    if flag == '!=':
        idx = [k for k, v in enumerate(dict[key]) if v != value]

    if len(idx) <= 0:
        print('WARNING in filterDictByValue: No data found')
        return {}

    batch = retrieveDictByIndex(dict, idx)

    return batch


def retrieveDictByKey(dict, key_list):
    """
    Retrieve a given dictionary by specified keys
    Args:
        dict:   input dictionary
        key_list:   list of keys for retrieval
    Returns:
        a dictionary with the specified keys
    """

    # Check if the input dictionary be empty
    if len(dict.keys()) <= 0:
        print('ERROR in retrieveDictByKeys: Empty dictionary')
        sys.exit()
    if len(key_list) <= 0:
        print('ERROR in retrieveDictByKeys: Empty key list for retrieval')
        sys.exit()

    batch = {}
    for key in key_list:
        if key in dict.keys():
            batch[key] = dict[key]
        else:
            print('WARNING in retrieveDictByKeys: ' + key + ' Not found in the input dictionary')

    return batch


def retrieveDictByIndex(dict, index_list):
    """
    Retrieve a dictionary by specified index
    Args:
        dict:       input dictionary, first row of index 0
        index_list: 1D array of index.
    Returns:
        a dictionary of specified index
    """

    # Check if the input dictionary be empty
    if len(dict.keys()) <= 0:
        print('ERROR in retrieveDictByIndex: Empty dictionary')
        sys.exit()
    if isDictConstantRow(dict) is False:
        print('ERROR in retrieveDictByIndex: Inconstant row number found in input dictionary')
        sys.exit()

    # Check if the index be empty
    if np.ndim(index_list) < 1:
        print('ERROR in retrieveDictByIndex: 1D index array expected')
        sys.exit()
    if len(index_list) <= 0:
        print('ERROR in retrieveDictByIndex: Empty index array')
        sys.exit()

    maxnrow = len(dict[list(dict.keys())[0]])
    if np.max(index_list) >= maxnrow:
        print('ERROR in retrieveDictByIndex: Index list out of bound')
        sys.exit()

    # Extract all keys
    batch = {}
    for key in dict.keys():
        data_batch = [dict[key][int(i)] for i in index_list]
        data_batch = np.asarray(data_batch)
        batch[key] = data_batch

    return batch


def retrieveDictRandom(dict, batch_size=10):
    """
    Retrieve a batch of a given dictionary randomly
    Args:
        dict:       input dictionary
        batch_size: size of dictionary batch. Default is 10
    Returns:
        dictionary batch
    """

    # Check if the input dictionary be empty
    if len(dict.keys()) <= 0:
        print('ERROR in retrieveDictBatchRandom: Empty dictionary')
        sys.exit()
    if isDictConstantRow(dict) is False:
        print('ERROR in retrieveDictBatchRandom: Inconstant row number found in input dictionary')
        sys.exit()

    maxnrow = len(dict[list(dict.keys())[0]])

    if batch_size > maxnrow:
        print('WARNING in retrieveDictBatchRandom: Batch size too large')
        batch_size = maxnrow

    # Random shuffle
    idx = np.arange(0, maxnrow)
    np.random.shuffle(idx)
    idx = idx[0:batch_size]

    # Extract all keys
    batch = {}
    for key in dict.keys():
        data_batch = [dict[key][i] for i in idx]
        data_batch = np.asarray(data_batch)
        batch[key] = data_batch

    return batch


def splitDictRandom(dict, fraction=0.9):
    """
    Split a dict randomly
    Args:
        dict:       input dictionary
        fraction:   Approximate fraction of the rows between 0 and 1
    Returns:
        Two new dictionaries
    """

    # Check if the input dictionary be empty
    if len(dict.keys()) <= 0:
        print('ERROR in splitDictRandom: Empty dictionary')
        sys.exit()
    if isDictConstantRow(dict) is False:
        print('ERROR in splitDictRandom: Inconstant row number found in input dictionary')
        sys.exit()

    if fraction <= 0.0 or fraction >= 1.0:
        print('ERROR in splitDictRandom: Fraction be (0.0, 1.0)')
        sys.exit()

    maxnrow = len(dict[list(dict.keys())[0]])

    nsplit = int(maxnrow * fraction)
    if nsplit <= 0:
        nsplit = 1
    if nsplit >= maxnrow:
        nsplit = maxnrow-1

    # Random shuffle
    idx = np.arange(0, maxnrow)
    np.random.shuffle(idx)
    idx_1 = idx[0:nsplit]
    idx_2 = idx[nsplit: maxnrow]

    # Extract all keys
    batch_1 = {}
    batch_2 = {}
    for key in dict.keys():
        data_batch = [dict[key][i] for i in idx_1]
        batch_1[key] = np.asarray(data_batch)
        data_batch = [dict[key][i] for i in idx_2]
        batch_2[key] = np.asarray(data_batch)

    return batch_1, batch_2


def truncateDict(dict, length=10):
    """
    Truncate a dictionary to a given length, and maximum truncation for the given length <= 0
    Args:
        dict:   input dictionary
        length: truncation length. Default is 10
                Maximum truncation if the given length <= 0
    Returns:
        Truncated dictionary
    """

    # Check if the input dictionary be empty
    if len(dict.keys()) <= 0:
        print('ERROR in truncateDict: Empty dictionary')
        sys.exit()

    firstkey = list(dict.keys())[0]
    maxlen = np.shape(dict[firstkey])[0]
    for key in dict.keys():
        len_key = np.shape(dict[key])[0]
        if maxlen > len_key:
            maxlen = len_key

    if length<=0 or length>maxlen:
        print('WARNING in truncateDict: Maximum truncation performed')
        length = maxlen

    idx = np.linspace(0, length-1, num=length, dtype=int)
    batch = {}
    for key in dict.keys():
        data_batch = [dict[key][i] for i in idx]
        data_batch = np.asarray(data_batch)
        batch[key] = data_batch

    return batch


def isMatDict(dict):
    """
    Check if all dictionary values are of type numpy.ndarray
    Args:
        dict:       the given dictionary
    Returns:
        True or false
    """

    # Check if the input dictionary be empty
    if len(dict.keys()) <= 0:
        print('ERROR in isMatDict: Empty input dictionary')
        sys.exit()

    for key in dict.keys():
        if type(dict[key]) != np.ndarray:
            return False

    return True


def extractMatDict(dict):
    """
    Extract the dictionary values of numpy.ndarray as a separate dictionary
    Args:
        dict:   a dictionary
    Returns:
        a dictionary with all values of type numpy.ndarray
    """

    if len(dict.keys()) <= 0:
        print('ERROR in extractNumDict: Empty input dictionary')
        sys.exit()

    numdict = {}
    for key in dict.keys():
        if type(dict[key]) == np.ndarray:
            numdict[key] = dict[key]

    return numdict


def mergeMatDict(dict1, dict2):
    """
    Merge two matrix dictionaries by their keys
    Args:
        dict1:  first matrix dictionary
        dict2: second matrix dictionary
    Returns:
        A new matrix dictionary
    """

    if (isMatDict(dict1) is False) or (isMatDict(dict2) is False):
        print('ERROR in mergeMatDict: Matrix dictionary expected')
        sys.exit()

    batch = dict1.copy()
    for key in dict2.keys():
        if (key in dict1.keys()):
            if np.shape(batch[key])[1] == np.shape(dict2[key])[1]:
                batch[key] = np.concatenate((batch[key], dict2[key]))
            else:
                print('WARNING: Inconstant matrix width in two dictionaries')
        else:
            batch[key] = dict2[key]

    return batch


def exportMatDict(dict, key_list=None):
    """
    Export a matrix dictionary as a numpy matrix
    Args:
        dict:       input matrix dictionary
        key_list:   list of keys for export. Default is None to export all keys
    Returns:
        matrix
    """

    # Check if the input dictionary be empty
    if len(dict.keys()) <= 0:
        print('ERROR in exportMatDict: Empty dictionary')
        sys.exit()
    if isMatDict(dict) is False:
        print('ERROR in exportMatDict: Matrix dictionary expected')
        sys.exit()

    if key_list is None:
        print('WARNING in exportMatDict: Export all keys')
        key_list = dict.keys()
    if len(key_list) <= 0:
        print('ERROR in exportMatDict: Empty key list for export')
        sys.exit()


    mat = []
    for key in key_list:
        if key in dict.keys():
            if len(mat) == 0:
                mat = dict[key]
            else:
                if np.shape(mat)[0] == np.shape(dict[key])[0]:
                    mat = np.concatenate((mat, dict[key]), axis=1)
                else:
                    print('ERROR in exportMatDict: ' + key + ' of inconstant row number')
                    sys.exit()

    return mat


def extendMatDict(dict, length=100):
    """
    Extend a matrix dictionary to a given length
    Args:
        dict:   input matrix dictionary
        length: extended length. Default is 100
    Returns:
        Extended dictionary
    """

    if isMatDict(dict) is False:
        print('ERROR in extendMatDict: Matrix dictionary expected')
        sys.exit()

    maxlen = maxDictConstantRow(dict)

    if length <= maxlen:
        print('WARNING in extendDict: No extension performed')
        length = maxlen

    batch = dict.copy()
    while maxDictConstantRow(batch) < length:
        lendiff = length - maxDictConstantRow(batch)
        if lendiff > maxlen:
            batch0 = dict.copy()
        else:
            batch0 = retrieveDictRandom(dict, lendiff)
        batch = mergeMatDict(batch, batch0)

    return batch


class matdict:
    # Pack all functions as a class
    #
    isDictConstantRow = isDictConstantRow
    maxDictConstantRow = maxDictConstantRow
    #
    filterDictByValue = filterDictByValue
    #
    retrieveDictByIndex = retrieveDictByIndex
    retrieveDictByKey = retrieveDictByKey
    retrieveDictRandom = retrieveDictRandom
    #
    splitDictRandom = splitDictRandom
    truncateDict = truncateDict
    #
    isMatDict = isMatDict
    extractMatDict = extractMatDict
    mergeMatDict = mergeMatDict
    exportMatDict = exportMatDict
    extendMatDict = extendMatDict