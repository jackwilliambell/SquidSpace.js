"""## sqslogger.py - SQS Logging helper functions

Provides basic logging services for the SQS tool, including an initialize
function that should only be called once per process. See initSqsLogger().

Aside from initialization, which should be done only when the process is starting, 
the most common usage pattern is:

    from sqslogger import logger

    logger.info('You can now log normally.') 
"""

import logging


SQS_LOGGER_NAME = 'SQS_LOGGER'


def makeLogger(lName, consoleLevel, fileLevel, logFilePath):
    """Makes a named logger with two formatters, each of which can have different
    log levels. If a log file path is not provided only a console formatter is 
    used, otherwise both a console and a file logger formatter are created."""
    # Create logger.
    logr = logging.getLogger(lName)
    logr.setLevel(consoleLevel)
    
    if logFilePath != None and len(logFilePath) > 0:
        # Create file handler which logs everything.
        fh = logging.FileHandler(logFilePath)
        fh.setLevel(fileLevel)
        fh.setFormatter(logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s'))
        logr.addHandler(fh)
    
    # Create console handler.
    ch = logging.StreamHandler()
    ch.setLevel(consoleLevel)
    ch.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    logr.addHandler(ch)
    
    return logr
    
    
def initSqsLogger(consoleVerbose, fileVerbose, logFilePath):
    """Initializes and returns a logger for SQS. This will be the same
    logger returned by the getSqsLogger() function, but it will be properly
    prepared by the makeLogger() function.
    
    WARNING: Do not call twice in one process. All calls to this function after
             the first one are ignored, aside from a warning message."""
    logr = getSqsLogger()
    
    # We only want to initialize one time. After that it's an error.
    if (not logr.hasHandlers()):
        consoleLevel = logging.INFO
        if consoleVerbose:
            consoleLevel = logging.DEBUG
        fileLevel = logging.INFO
        if fileVerbose:
            fileLevel = logging.DEBUG
        return makeLogger(SQS_LOGGER_NAME, consoleLevel, fileLevel, logFilePath)
    else:
        logr.warning("sqslogger.initSqsLogger() Cannot initialize twice. Use getSqsLogger().")
    
    return logr


def getSqsLogger():
    """Returns the logger for SQS. If initSqsLogger() has not been called it is the 
    same as the default logger. This logger is also available via the variable 
    sqslogger.logger."""
    return logging.getLogger(SQS_LOGGER_NAME)
    
logger = getSqsLogger()
