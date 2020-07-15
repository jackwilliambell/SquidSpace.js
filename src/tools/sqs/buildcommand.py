"""## SquidSpace.js Build Command

The SquidSpace.js 'build' command reads in a 'build' file containing JSON data meeting the 
SquidSpace.js Build File Specification. Then, with that data, it TODO: document.

For more information on Build Files and SquidSpace.js, please refer to the documentation 
located in the project repo at https://github.com/jackwilliambell/SquidSpace.js"""


copyright = """SquidSpace.js, the associated tooling, and the documentation are copyright 
Jack William Bell 2020 except where noted. All other content, including HTML files and 3D 
assets, are copyright their respective authors."""


import sys
import os
import json


from common import ModuleConfiguration
from filtercommand import runFilter
from generatecommand import runGenerate
from sqslogger import logger

def processBuildData(defaultConfig, buildData):
    # TODO: Support checking if we need to perform steps because something has changed. 
    #       Need to think about how to do this, especially for input/output pairs and 
    #       overriding to force builds.
    
    # Basically build will execute the following SQS commands as steps: generate, build
    # package, filter, and pipeline. Special functionality (merge, minify, etc) are implemented
    # as filters and you can execute chains of filters with the filter command. Support for
    # all the use cases may require modifications to the filter command. 
    
    # Steps are executed in order and can (in the case of build and package) include executing
    # sub-build steps/files. 
    pass


def processBuildString(defaultConfig, buildDataString):
    """Loads JSON Build Data from a string and processes it."""

    # Assume failure.
    buildData = None
    
    try:
        buildData = json.loads(buildDataString)
    except json.JSONDecodeError:
        logger.exception("buildcommand.processBuildString() - Could not load Build string.")
        return
        
    if not buildData is None:    
        processBuildData(defaultConfig, buildData)


def processBuildFile(defaultConfig, buildFile):
    """Loads JSON Build data from a file-like object and processes it."""
        
    # Assume failure.
    buildData = None
    
    try:
        moduleData = json.load(buildFile)
    except json.JSONDecodeError:
        logger.exception("buildcommand.processBuildFile() - Error loading Build File.")
        return
        
    if not buildData is None:    
        processBuildData(defaultConfig, buildData)


def runBuild(defaultConfig, buildFileNames):
    """SQS build command."""
    # Assume Failure.
    buildFile = None

    # We expect to process a list of file names.
    if not isinstance(buildFileNames, list):
        buildFileNames = [buildFileNames] # Force list.
        
    for buildFileName in buildFileNames:
        if not buildFileName is None and not buildFileName == "":
            # Use passed Module File name.
            logger.debug("buildcommand.runBuild() - Build File: " + buildFileName)
            try:
                processBuildFile(buildFileName)
            except:
                logger.exception("generate.runBuild() - Error reading Build File.")
        else:
            # TODO: Fix here and elsewhere - this won't be reached because we are 
            #       iterating a possibly empty list.
            # TODO: Copy STDIN to scratch directory before starting?
            # Use stdin if no file name.
            logger.info("buildcommand.runBuild() - Reading module data from STDIN.")
            #logger.error("generate.runBuild() - Currently STDIN not supported.")
            buildFile = sys.stdin

        if not buildFile is None:    
            processBuildFile(defaultConfig, buildFile)
