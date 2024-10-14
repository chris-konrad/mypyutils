# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 08:16:50 2024

A simple status logger

@author: Christoph M. Schmidt
"""

import os
from datetime import datetime, timezone, tzinfo

class LogfileNotAvailabelException(Exception):
    """ An execption thrown if the log file is not availe"""
    pass

class LoggerDevice:
    """ A simple logger device for logging informtion, warning and critical messages to outline and
    to file
    """
    
    TS_FORMAT = '%Y%m%d_%H%M%S'
    COL_SEP = '  '
    
    def __init__(self):
        """
        Create a logger object and set up some default settings.

        Returns
        -------
        None.

        """
        self.path_logfile = None
        self.retry_on_connection_error = False
        self.timezone = None
        self.to_file = False
        self.to_outline = True
        
    def init(self, to_outline=True, dir_out=None, filetag="log", timezone=None):
        """
        Initialize the logger device. This must be called to enable logging to file. Logging
        to outline works without calling logger.init()

        Parameters
        ----------
        to_outline : bool, optional
            If True, logging to outline is activated. The default is True.
        dir_out : str, optional
            If not None, logging to a logfile created in dir_out is activated. The default is None.
        filetag : str, optional
            A name tag for the logfile. The default is "log".
        timezone : TYPE, optional
            The timezone used for log timestamps. Must be either None (local time), 'UTC', or an 
            object of a datetime.tzinfo subclass. The default is None.

        Returns
        -------
        None.

        """
        
        #parse timezone
        self._parse_timezone(timezone)
        
        #init logging to outline
        self.to_outline = to_outline
        
        #init logging to file
        if dir_out is not None:
            self.to_file is True
            self._init_logfile(dir_out, filetag)
   
    
    def info(self, msg):
        """
        Log an info message with the INFO message type tag.

        Parameters
        ----------
        msg : str
            Message to be logged.
        """
        self._log('info', msg)
     
    def warning(self, msg):
        """
        Log a warning with the WARN message type tag.

        Parameters
        ----------
        msg : str
            Message to be logged.
        """
        self._log('warn', msg)
    
    def critical(self, msg):
        """
        Log a critical message with the CRIT message type tag.

        Parameters
        ----------
        msg : str
            Message to be logged.
        """
        self._log('crit', msg)
            
                
    def _init_logfile(self, dir_out, filetag):
        """Initialize logging to file"""
        
        assert(os.path.isdir(dir_out)), ("Can't find directory {dir_out}")
        
        
        ts = self._get_ts()
        filename = ts + "_" + filetag + ".log"
        
        self.path_logfile = os.path.join(dir_out, filename)
        
        #create file
        with open(self.path_logfile, 'w') as f:
            pass
        
        self._log('status', 'Logger initialised.')

    
    def _log(self, msg_type, content):
        """Log to file and/or outline"""
        
        content = content[0].upper() + content[1:]
        content = self._add_punctuation(content)
        
        #make message
        msg = self._mkmsg(msg_type, content)
        
        #write log to outline
        if self.to_outline:
            print(msg)
        
        #write log to file
        if self.to_file:
            self.logfile_is_ready()
            with open(self.path_logfile, 'a') as f:
                f.write(msg)
    
    def _add_punctuation(self, msg):
        """ Force punctuation of a message. """
        if not msg[-1] in ('.', '!', '?', ';', ';'):
            msg = msg + '.'
            
        return msg
    
    def _mkmsg(self, msg_type, content):
        """ Put a message together """
        return f"{self._get_ts()}{LoggerDevice.COL_SEP}{msg_type.upper()}{LoggerDevice.COL_SEP}{content}"
        
    
    def _get_ts(self):
        """ Get a timestamp string """
        return datetime.now(self.timezone).strftime(LoggerDevice.TS_FORMAT)
    
    def _parse_timezone(self, tz):
        """ Parse the timezone input given to init() """
        
        if tz is None:
            self.timezone = None
        if tz == 'UTC':
            self.tz = timezone.utc
        if isinstance(tz, tzinfo):
            self.timezone = tz
            
        msg = (f"The timezone parameter must be either None (local time), 'UTC', or an object of"
               f"a datetime.tzinfo subclass. Instead it was type <{type(tz)}> with value {tz}")
        
        raise ValueError(msg)    
        
    
    def logfile_is_ready(self):
        """Check if the logfile is ready to write
        
        Raises
        ------
        
        LogfileNotAvailableException 
           Raised if the logfile was not initialised yet of cannot be reached. 
        """
        
        if self.path_logfile is None:
            msg = (f"The logger has not been initialized for logging to file. Call logger.init() "
                   f"and provide an output directory!")
            raise LogfileNotAvailabelException(msg)
            
        if not os.path.isfile(self.path_logfile):
            msg = (f"The logfile does not exist or is not reachable after it was initialized. Can't"
                   f" find {self.path_logfile}")
            raise LogfileNotAvailabelException(msg)
                  
            
# --------------------------------------------------------------------------------------------------

# create a logger for easy import over multiple scripts
logger = LoggerDevice()