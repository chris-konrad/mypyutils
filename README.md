MyPyUtils
==============================

A package collecting utility functions and classes that I like to use. 

### Modules

The package currently contains the following modules and functions.

#### Log

A simple status logger for logging to file and/or outline. To share a logger across the context of multiple modules, import the logger object initialized in the script.

```python
import mypyutils.log.logger
```

Otherwise, create an individual logger with.

```python
import mypyutils.log.loggerDevice
logger = LoggerDevice()
```

It is shares some aspects of the API and the log ouput format of the standard Cython logger 

##### Logging to File

Independednt of the initialisation of the LoggerDevice object, logging to file has to be initialised separately with a call to `logger.init()`

### Disclaimer

The package is research code under development. It may contain bugs and sections of unused or insensible code as well as undocumented features. Major changes to this package are planned for the time to come. A proper API documentation is still missing. Refer to the demos for examples how to use this model.

## Installation

1. Clone this repository. 
   
   ```
   git clone  https://github.com/chrismo-konrad/mypyutils.git
   ```

2. Install the package and it's dependencies. Refer to `pyproject.toml` for an overview of the dependencies. 
   
   ```
   cd ./mypyutils
   pip install . 
   ```

## 
