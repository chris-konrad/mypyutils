# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 10:17:32 2024

@author: Christoph M. Konrad
"""
import os
import yaml
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
                
            
def read_yaml(filepath):
    """
    Read a yaml config file and return config.

    Parameters
    ----------
    filepath : str
        The path of the yaml config file.

    Returns
    -------
    config : dict
        (Nested) dictionary of the configration.
    """
    
    #check path
    filepath = verify_existing_filepath(filepath, ['.yaml', '.yml'])
        
    with open(filepath, "r") as f:
        config = yaml.safe_load(f)

    return config


def write_yaml(filepath, dict):
    """
    Write a yaml config file from dict.

    Caution! Should not contain complex datatypes.

    Parameters
    ----------
    filepath : str
        The path of the yaml config file.
    dict : dict
        The dictionary to store as yaml file.
    """    

    filepath = verify_new_filepath(filepath, ['.yaml', 'yml'])

    # write 
    with open(filepath, 'w') as f:
        yaml.dump(dict, f)          


def verify_existing_filepath(filepath, permitted_filetypes):
    """ Check that filepath is of the permitted type.
    Check if the directory and file exists.

    Accepts filepaths like:
    //path//to//file//filename.filetype

    where filetype is any of permitted_filetypes. 
    
    Parameters
    ----------
    filepath : str
        Filepath to check
    permitted_filetypes : list
        List of permitted filetypes. 

    Returns
    -------
    filepath : str
        Unmodified filepath
    """
    
    # create output directory if necessary
    dir, filename, filetype = fileparts(filepath)

    # check if directory exists
    if not os.path.isdir(dir):
        raise FileNotFoundError(f"Directory {dir} not found!")
    
    # check if filename is provided
    if filename == '':
        raise ValueError(f"Filepath '{filepath}' does not include a filename!")
    
    # check filetype
    if filetype not in permitted_filetypes:
        raise ValueError((f"Filetype must be any of {permitted_filetypes}! "
                          f"Instead filepath '{filepath}' has type {filetype}."))

    # check if file exists
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File {dir} does not found!")

    return filepath


def verify_new_filepath(filepath, permitted_filetypes, makedir=True):
    """ Check that filepath is of the permitted type. Appends filetype
    if filetype is missing. Check if the directory exists and create 
    directory if requested.

    Accepts filepaths like:
    //path//to//file//filename.filetype

    where filetype is any of permitted_filetypes. 
    
    Parameters
    ----------
    filepath : str
        Filepath to check
    permitted_filetypes : list
        List of permitted filetypes. If filepath does not specify a 
        filetype, the first filetype from the list will be appended. 
    makedir : bool, optional
        Make a new directory if the specified directory does not exist.
        Default is True.

    Returns
    -------
    filepath : str
        Verified file path.    
    """
    
    # create output directory if necessary
    dir, filename, filetype = fileparts(filepath)
    if not os.path.isdir(dir):
        if makedir:
            os.makedirs(dir)
        else:
            msg = (f"Directory {dir} does not exist! Set makedir=True "
                   f"to automatically create a new directory with this name.")
            raise FileNotFoundError(msg)

    # check if filename is provided
    if filename == '':
        raise ValueError(f"Filepath '{filepath}' does not include a filename!")

    # check filetype
    if filetype == '':
        filetype = permitted_filetypes[0]

    if filetype not in permitted_filetypes:
        raise ValueError((f"Filetype must be any of {permitted_filetypes}! "
                          f"Instead filepath '{filepath}' has type {filetype}."))

    return os.path.join(dir, filename+filetype)
                
        
        
        