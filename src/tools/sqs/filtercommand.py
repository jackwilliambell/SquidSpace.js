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


from common import ModuleConfiguration, ScratchDirManager, makeOutputFilesFuncForDir, copyFileToDir, lookAheadIterator
from filterhelpers import getFilterModule
from sqslogger import logger


def filterFilesFunctionSignature(inputs, outputs, options, logger):
    """## Filter Functions
    
    Filter functions process input data delivered in the form of one or more 
    file-like objects and write the processed data out to one or more file-like 
    objects. How any one filter function implementation does this is entirely 
    arbitrary, but it should be done in a stateless manner; using only the passed 
    arguments and no other state.
    
    Filter functions return the number of files successfully processed. 
    
    ### Arguments
    
    * inputs: A list of zero to many input file paths
    
    * outputs: A function that, when called with a file name, returns 
      a file path to write to
    
    * options: An options dictionary or None; options may or may not contain
      named values the implementation knows about
    
    * logger: A Python logger instance for the implementation to use as needed
    
    ### Pseudocode 
    
    A 'read a file, write a file' implementation:
    
            prepare internal state based on options, assume success
    
            for every input file path provided by inputs:
    
                open the file
    
                while reading file data:
                
                    process data:
                        
                        on success:
    
                            request an output file path from outputs
    
                            open the output file
    
                            write processed data to output file
    
                            close the output file
    
                            increment the files processed count
                        
                        on failure:
                    
                            log error
    
                close the input file
    
            return the files processed count
    
    A 'read many files, write one file' implementation:
    
            prepare internal state based on options, assume success
    
            request an output file path from outputs

            open the output file
        
            for every input file provided by inputs:    
    
                open the file
    
                while reading file data:
                
                    process data:
                        
                        on success:
    
                            write processed data to output file
    
                            increment the files processed count
                        
                        on failure:
                    
                            log error
    
                close the input file
    
            close the output file
    
            return the files processed count
    
    ### Notes
    
    1. Filter functions may read one file and write several or they may read multiple
       files and write one or none; everything is up to the implementation
    
    2. Filter functions are free to use the same name as the input file for the output 
       file or to rename the output file; whatever makes sense for the use case
    
    3. Every filter function should include a docstring with extensive documentation 
       covering how the filter works, what the options are, and giving examples.
    
    4. Unless an unrecoverable error occurs, filter functions should process every 
       input file until the generator is exhausted, unless there is a clear use 
       case for doing otherwise
    
    5. If an error or exception occurs the filter function should log detailed 
       information about the problem and then continue processing the next input file
    """
    pass


def processFilterChain(inFiles, outDir, scratchDirMgr, filterChain):
    """Accepts a list of input file paths, an output directory path, a scratch directory 
    manager object, and a list of filters. Executes each filter in turn, using the scratch 
    directory for intermediate files, with the result that all file in the input files list 
    are filtered and written out the output directory. Returns True on success, 
    otherwise returns False.
    
    NOTE: If no filters are supplied, the input files are simply copied to the output directory.
    
    NOTE: Unless an unrecoverable error occurs, all files and filters will be processed as best
    as possible. If a recoverable problem occurs errors and warnings will be logged and the 
    function will return False.
    
    NOTE: May add temporary files to the scratch directory without clearing them. Calling code
    is responsible for managing the scratch directory."""
    # Check args.
    # TODO: Type checking. Better error handling.
    if not inFiles:
        logger.error("filtercommand.processFilterChain() - Input file list required.")
        return False
    if not outDir:
        logger.error("filtercommand.processFilterChain() - Output Directory required.")
        return False
    if not scratchDirMgr:
        logger.error("filtercommand.processFilterChain() - Scratch Directory Manager required.")
        return False
        
    # Setup.
    result = True # Assume success
    
    # Do we have a filter chain?
    if filterChain is None:
        # No filters? Simply copy the files and get out.
        for filePath in inFiles:
            if not copyFileToDir(filePath, outDir):
                logger.error("filtercommand.processFilterChain() - Could not copy '{0}' to '{1}'.".format(filePath, outDir))
                result = False
    else:
        # Set up the scratch work areas.
        # NOTE: first time through the inFiles list is the passed in argument. Afterwards
        #       it is from the outdir.
        sdIn = scratchDirMgr.makeSubScratchDirManager("sd1")
        sdOut = scratchDirMgr.makeSubScratchDirManager("sd2")
        
        # Process the filter chain.
        for fd, isLastFD in lookAheadIterator(filterChain):
            #logger.debug("filtercommand.filterFile() - Lookahead: " + str(isLastFD) + " / " + str(fd))
            # Get the named filter module.
            filterFunc, filterDoc = getFilterModule(fd.get("filter"))
            if not filterFunc:
                logger.error("filtercommand.processFilterChain() - Could not load filter module for '{0}'.".format(fd.get("filter")))
                # We cannot continue without a valid filter.
                result = False
                break
            
            # For the last iteration, we want the output going to the output directory.
            outputs = sdOut.makeOutputFilesFunc()
            if isLastFD:
                outputs = makeOutputFilesFuncForDir(outDir) 
            
            # Execute the filter function
            cnt = filterFunc(inFiles, outputs, fd.get("options"), logger)
            if cnt < 1:
                logger.warning("filtercommand.processFilterChain() - filter module '{0}' processed zero files.".format(fd.get("filter")))
                result = False
            elif cnt != len(inFiles):
                logger.warning("filtercommand.processFilterChain() - filter module '{0}' processed {1} files out of {2}.".format(fd.get("filter"), cnt, len(inFiles)))
                result = False
            
            # Get the file list from the out for the next iteration.
            inFiles = sdOut.listFiles()
            
            # Swap the ins and outs.
            sdt = sdIn 
            sdIn = sdOut 
            sdOut = sdt
            
            # Clear the new out
            sdOut.clear()
        
    return result


def runFilter(defaultConfig, filterProfile, inFiles, outDir):
    """SQS filter command."""
    # Assume Failure.
    fileToFilter = None
    
    # We expect to process a list of file names.
    if not isinstance(inFiles, list):
        inFiles = [inFiles] # Force list.
        
    # Create the module processing configuration.
    modConfig = ModuleConfiguration(defaultConfig, {})
        
    # Create scratchDirMgr.
    sd = modConfig.getScratchDirManager()
    
    # Process the filters.
    if not processFilterChain(inFiles, outDir, sd, modConfig.getFilters(None, filterProfile)):
        logger.warning("filtercommand.runFilter() - Unable to completely process all files and filters.")
    
    # Cleanup.
    # TODO: If anything above fails with an exception the scratch dir is not cleaned up.
    sd.remove()
    
    # TODO: Support STDIN if inFiles is empty. See junk code below.
    # Use stdin if no file name.
    # TODO: Fix here and elsewhere - this won't be reached because we are 
    #       iterating a possibly empty list.
    # TODO: Copy STDIN to scratch directory before starting
    #logger.info("filtercommand.runFilter() - Reading file data from STDIN.")
    #logger.error("filtercommand.runFilter() - Currently STDIN not supported.")
    #source = sys.stdin
