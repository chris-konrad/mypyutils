# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 10:17:32 2024

@author: Christoph M. Konrad
"""
import os
import keyboard
import numpy as np

from mypyutils.log import LogfileNotAvailableException, LoggerDevice
from time import sleep

def write_with_recovery(filename, message, write_mode ='a', logger='None', t_wait_s = 600):
    
    retry = True
    while retry:
        try:
            with open(filename, 'a') as f:
                f.write(message)
            retry = False
        except OSError:
            #log error
            if logger is not None:
                fname = filename.split('\\')[-1]
                msg = f"Failed to open {fname}. Will retry after {t_wait_s} s. Hold 'r' to retry now."
                try:
                    logger.critical(msg)
                except Exception as e:
                    if not isinstance(e, LogfileNotAvailableException):
                        print(msg)
                        
            for i in range(t_wait_s):
                sleep(1)
                if keyboard.is_pressed('r'):
                    break
            
            
def fileparts(path):
    """
    Return fileparts of a file path: Directory, filename and filetype.
    If path points to a directory rather then a file, filename and filetype will be an empty string.

    Parameters
    ----------
    path : path-like
        The path to be split in fileparts.

    Returns
    -------
    directory : path-like
        The directory of the file.
    filename : str
        The filename.
    filetype : str
        The filetype including '.', e.g. '.txt'.

    """


    directory, file = os.path.split(path)
    
    if '.' in file:
        filename, filetype = file.split('.')
        filetype = '.'+filetype
    else:
        directory += file
        filename = ''
        filetype = ''
    
    return directory, filename, filetype
                
            

                
        
        
        