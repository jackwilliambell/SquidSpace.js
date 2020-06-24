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


from common import getFilterModule, ModuleConfiguration, ResourceFlavor, ResourceAction, ScratchDirManager, lookAheadIterator
from sqslogger import logger


def filterFile(sourcePath, destPath, scratchDirMgr, filters):
    """Accepts a source path, and destination path, a scratch directory manager object,
    and a list of filters. Executes each filter in turn, using the scratch directory for
    intermediate files, with the result that the file referred to by the source path 
    is filtered and written out the destination path. Returns True on success, otherwise
    returns False.
    
    NOTE: If no filters are supplied, the source path is simply copied to the destination 
    path.
    
    NOTE: Adds temporary files to the scratch directory without clearing them. Calling code
    is responsible for managing the scratch directory."""
    
    # Check args.
    # TODO: Type checking. Better error handling.
    if not sourcePath:
        logger.error("filterfile.filterFile() - Source path required.")
        return False
    if not destPath:
        logger.error("filterfile.filterFile() - Destination path required.")
        return False
    if not scratchDirMgr:
        logger.error("filterfile.filterFile() - Scratch Directory Manager required.")
        return False
    
    # Do we have filters?
    if filters is None:
        # No filters? Simply copy the file and get out, unless the source and destination 
        # paths are the same.
        if os.path.realpath(sourcePath) != os.path.realpath(destPath):
            sourceFile = getSourceFile(sourcePath)
            destFile = getDestFile(destPath)
            return copySourceToDestAndClose(sourceFile, destFile)
        # They were the same file.
        return True
    
    # initialize the filter file paths.
    inFile = None
    outFile = sourcePath # This makes the source path the in file for the first iteration, see below.
    
    for fd, isLastFD in lookAheadIterator(filters):
        # Get the named filter module.
        logger.debug("filterfile.filterFile() - Lookahead: " + str(isLastFD) + " / " + str(fd))
        filterExt, filterFunc, filterDoc = getFilterModule(fd.get("filter"))
        if not filterExt or not filterFunc:
            logger.error("filterfile.filterFile() - Could not load filter module for '{0}'.".format(fd.get("filter")))
            return False
        
        # Get valid file extensions for the filter module.
        inExt, outExt = filterExt(fd.get("options"), fd.get("data"))
        
        # Set up filter file paths.
        inFile = outFile # Chain out to in.
        # TODO: Verify inFile has the same extension as inExt.
        # TODO: Determine how to handle the possibility of mulitple valid extensions or any extension.
        if isLastFD:
            outFile = destPath # For the last one, we want the output going to the destination path.
        else:
            outFile = scratchDirMgr.getTempFilePath(outExt)  
        
        # Execute the filter function
        result = filterFunc(inFile, outFile, fd.get("options"), fd.get("data"))
        if not result:
            logger.error("filterfile.filterFile() - filter module '{0}' failed, aborting.".format(fd.get("filter")))
            return False

    # Success!
    return True


def runFilter(defaultConfig, filterProfile, outDir, fileNames):
    """SQS filter command."""
    # Assume Failure.
    fileToFilter = None
    
    # We expect to process a list of file names.
    if not isinstance(fileNames, list):
        fileNames = [fileNames] # Force list.
        
    # Create the module processing configuration.
    modConfig = ModuleConfiguration(defaultConfig, {})
        
    # Create scratchDirMgr.
    scratchDirMgr = modConfig.getScratchDirManager()
        
    for sourcePath in fileNames:
        if not sourcePath is None and not sourcePath == "":
            # Use passed file name.
            logger.info("filterfile.runFilter() - Filtering '{0}'.".format(sourcePath))
            
            # Create the destination path.
            sourceFileName = os.path.basename(sourcePath)
            destPath = os.path.join(outDir, sourceFileName)
            
            # Filter the file.
            if not filterFile(sourcePath, destPath, scratchDirMgr, modConfig.getFilters(None, filterProfile)):
                logger.error("filterfile.runFilter() - Unable to filter '{0}'.".format(sourcePath))
        else:
            # Use stdin if no file name.
            # TODO: Fix here and elsewhere - this won't be reached because we are 
            #       iterating a possibly empty list.
            # TODO: Copy STDIN to scratch directory before starting
            #logger.info("filterfile.runFilter() - Reading file data from STDIN.")
            logger.error("filterfile.runFilter() - Currently STDIN not supported.")
            source = sys.stdin
    
    # Cleanup.
    # TODO: If anything above fails with an exception the scratch dir is not cleaned up.
    scratchDirMgr.remove()
