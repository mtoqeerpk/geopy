#############################################################################################
#                                                                                           #
# Author:   Haibin Di                                                                       #
#                                                                                           #
#############################################################################################

# basic functions for keyboard

import sys, os


__all__ = ['keyboard']


LetterKeyList = ['A', 'B', 'C', 'D', 'E',
                 'F', 'G', 'H', 'I', 'J',
                 'K', 'L', 'M', 'N', 'O',
                 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z']
NumberKeyList = ['0', '1', '2', '3', '4',
                 '5', '6', '7', '8', '9']


class keyboard:
    # Pack all functions as a class
    #
    LetterKeyList = LetterKeyList
    NumberKeyList = NumberKeyList
