"""## SquidSpace.js Filter Command

The SquidSpace.js 'filter' command reads in a 'module' file containing JSON data meeting the 
Module File Specification and using the SquidSpace.js Module File extensions. Then, with 
that data, it TODO: document.

For more information on Module Files and SquidSpace.js, please refer to the documentation 
located in the project repo at https://github.com/jackwilliambell/SquidSpace.js"""


copyright = """SquidSpace.js, the associated tooling, and the documentation are copyright 
Jack William Bell 2020 except where noted. All other content, including HTML files and 3D 
assets, are copyright their respective authors."""


import sys
import os
import json


from common import getFilterFunction, ResourceFlavor, ResourceAction, ScratchDirManager
from sqslogger import logger


def filterFile(filters, pathIn, pathOut, scratchDirMgr):
    """ TODO """
    # TODO: Use ScratchDirManager for in/out files
    inFile = None
    outFile = pathIn
    
    for fd in filters:
        # Get file names.
        inFile = outfile
        outFile = '' # from scratch.
        
        # Get filter function
        filterFunc = getFilterFunction(fd["filter"])
        
        # Execute the filter function
        if filterFunc != None:
            result = filterFunc(inFile, outFile, fd["options"], fd["data"])
            if not result:
                # TODO: Error message.
                return False
        else:
            # TODO: Error message.
            return False
    
    # TODO: Copy last 'outFile' to pathOut
    # TODO: Clear the scratch?

    # Success!
    return True


def filterFileWithConfig(defaultConfig, filters, filterProfile, pathIn, pathOut, scratchDirMgr):
    """ TODO """
    # Were we passed a set of filters?
    if filters == None:
        # Is the filter profile useful?
        if filterProfile in defaultConfig.filterProfiles:
            # Use the default filters for the filter profile.
            filters = defaultConfig.filterProfiles[filterProfile]
        else:
            logger.error(
                "filterfile.filterFileWithConfig() - Could not find filter declarations for filter profile: {0}.".format(filterProfile))
            return False
    
    # Do we have filters now?
    if filters == None
        logger.error("filterfile.filterFileWithConfig() = Invalid or no filters supplied.")
        return False
    
    # Filter the file.
    return filterFile(filters, pathIn, pathOut, scratchDir)


def filterResourceFile(defaultConfig, resourceOptions, fileName):
    # TODO Do we need this? Probably need to start implementing pipeline to see how it would be used.
    pass 


def runFilter(defaultConfig, filterProfile, outDir, fileNames):
    """ TODO """
    # Assume Failure.
    fileToFilter = None
    
    # We expect to process a list of file names.
    if not isinstance(fileNames, list):
        fileNames = [fileNames] # Force list.
        
    for fileName in fileNames:
        if not resourceFileName is None and not moduleFileName == "":
            # Use passed Module File name.
            logger.info("filterfile.runFilter() - Filtering File: " + moduleFileName)
            try:
                moduleFile = open(moduleFileName)
            except:
                logger.exception("filterfile.runFilter() - Error reading Module File:")
        else:
            # Use stdin if no file name.
            # TODO: Fix here and elsewhere - this won't be reached because we are 
            #       iterating a possibly empty list.
            logger.info("filterfile.runFilter() - Reading module data from STDIN.")
            moduleFile = sys.stdin

        if not moduleFile is None:    
            processModuleFile(defaultConfig, moduleFile, filterProfile)
