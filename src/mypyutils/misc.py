# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 08:21:26 2024

Miscellaneous helper functions

@author: Christoph M. Konrad
"""
import numpy as np

def is_in_range(val, limits, include_limits=(True,False)):
    """ Test if val is withing the range definied by limits = (upper, lower)
    """
    
    if include_limits == (True, True):
        return np.all(val >= limits [0] and val <= limits[1])
    
    if include_limits == (False, True):
        return np.all(val > limits [0] and val <= limits[1])
    
    if include_limits == (True, False):
        return np.all(val >= limits [0] and val < limits[1])
    
    if include_limits == (True, True):
        return np.all(val > limits [0] and val < limits[1])

def limits(x):
    """ Find the upper and lower bound of the data in x with one function calll.
    """
    
    return np.amin(x), np.amax(x)

def s2hms(s):
    """
    Convert a time in seconds into 'HH:MM:SS.ss hours'.

    Parameters
    ----------
    s : int
        Time in seconds.

    Returns
    -------
    hms : str
        Time string in the format 'HH:MM:SS.ss hours'.

    """
    
    h = int(s / 3600)
    m = int((s - h * 3600)/60)
    s = s - h * 3600 - m * 60
    sfull = int(s)
    sfrac = s - sfull
    sfrac = f'{sfrac:.2f}'
    
    hms = f"{h:02}:{m:02}:{sfull:02}.{sfrac[2:]} hours"
    
    return hms

def none_switch(value_a, value_b):
    """
    Return the value of a pair that is not None. If both are not None, return value_a
    
    Use for class property assignments of the style:
        
    ...
        kwarg1 = None):
    
    self.kwarg1 = none_switch(kwarg1, CLASS.KWARG1_DEFAULT)
    ...

    Parameters
    ----------
    value_a, value_b : any
        The value pair to be switched between.

    Raises
    ------
    ValueError
        Raised if both values are None.

    Returns
    -------
    TYPE
        The input value that is not None.

    """
    if value_a is not None:
        return value_a
    elif value_b is not None:
        return value_b
    raise ValueError('Both values of a none_switch are None!')