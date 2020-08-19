"""## SquidSpace.js Pipeline Command

The SquidSpace.js 'pipeline' command reads in a 'module' file containing JSON data meeting the 
Module File Specification and using the SquidSpace.js Module File extensions. Then, with 
that data, it TODO: document.

For more information on Module Files and SquidSpace.js, please refer to the documentation 
located in the project repo at https://github.com/jackwilliambell/SquidSpace.js"""


copyright = """SquidSpace.js, the associated tooling, and the documentation are copyright 
Jack William Bell 2020 except where noted. All other content, including HTML files and 3D 
assets, are copyright their respective authors."""


import sys
import os
from urllib.parse import urlparse
import json

from sqslogger import logger
from common import ResourceFlavor, ModuleConfiguration, ScratchDirManager, getSourceURL, getSourceFile, getDestFile, copySourceToDestAndClose
from filtercommand import processFilterChain

    
def processPipelineForResource(resourceFlavor, elem, scratchDirMgr, modConfig):
    """Processes the pipeline for one resource file element. TODO: More docs."""
    logger.debug("pipeline.processPipelineForResource() - Processing pipeline for resource: " + elem["resource-name"])
    #logger.debug("pipeline.processPipelineForResource() - Processing pipeline for {0} resource: %{1}s".format( resourceFlavor, elem))
    
    # Get the element config.
    if not "config" in elem:
        # No need to process!
        logger.debug("pipeline.processPipelineForResource() - No 'config'; process abort with 'True'.")
        return True
    config = elem["config"]
    
    # Get the cache options from the config.
    if not "cache-options" in config:
        # No need to process!
        logger.debug("pipeline.processPipelineForResource() - No 'cache-options' in 'config'; process abort with 'True'.")
        return True
    cacheOptions = config["cache-options"]
    
    # Are there any cache options to process?
    if not bool(cacheOptions): # PYTHON TIP: Empty dictionaries evaluate to 'False'. 
        # No need to process!
        logger.warning("pipeline.processPipelineForResource() - Empty 'cache-options' in 'config'; process abort with 'True'.")
        return True
    
    # Try to get the destination file path.
    destPath = modConfig.makeResourceFilePath(resourceFlavor, config.get("file-name"))
    if not destPath:
        logger.error("pipeline.processPipelineForResource() - Could not determine output file path. Invalid or unspecified file name or configuration.")
        return False
    
    # Try to get the source file path, source file name, and open it as a file.
    sourcePath = cacheOptions.get("file-source")
    sourceFile = None
    if sourcePath:
        sourceFile = getSourceFile(sourcePath)
    else:
        # Try to get the source from a URL.
        sourcePath = cacheOptions.get("url-source")
        if sourcePath:
            url = urlparse(sourcePath)
            sourceFile = getSourceURL(sourcePath)
        else:
            logger.error("pipeline.processPipelineForResource() - Invalid or unspecified file or URL source in 'cache-options'.")
            return False
    
    # Did we get a source file?
    if not sourceFile:
        logger.error("pipeline.processPipelineForResource() - Could not open source file.")
        return False
    
    # Clear the scratch dir.
    # TODO: Determine if we really want to do this here.
    scratchDirMgr.clear()
    
    # Re-create the source path from the destination file name and the input file extension.
    # Also strip the name portion from the destination path, so we can use it as a pure path.
    # This way we are starting processing from the name we want to end up with and providing
    # a directory path for the result.
    # NOTE: If the filters change the name we will not have the expected result.
    # TODO: Need to make this more robust, but not sure how to handle filters which
    #       do odd things.
    sourceName, sourceExt = os.path.splitext(os.path.basename(sourcePath))
    destPath, destName = os.path.split(destPath)
    destName, destExt = os.path.splitext(destName)
    sourcePath = scratchDirMgr.makeFilePath(destName + sourceExt)
    
    # Copy the source to the scratch dir.
    scratchDest = getDestFile(sourcePath)
    if scratchDest:
        if not copySourceToDestAndClose(sourceFile, scratchDest):
            logger.error("pipeline.processPipelineForResource() - Unable to copy source file to scratch directory.")
            return False
    else:
        logger.error("pipeline.processPipelineForResource() - Unable to create source file in scratch directory.")
        return False
    
    # Filter the resource file.
    return processFilterChain([sourcePath], destPath, scratchDirMgr,
            modConfig.getFilters(cacheOptions.get("filters"), cacheOptions.get("filter-profile")))


def processModuleData(defaultConfig, moduleData):
    """Processes the Module Data to manage an asset pipeline."""
    
    #logger.debug("pipeline.processModuleData() - Processing module data %{0}s.".format(moduleData))
    logger.debug("pipeline.processModuleData() - Processing pipeline for module: " + moduleData["module-name"])
    
    # Get module configuration.
    moduleConfig = {} # Default config is empty dict.
    if "config" in moduleData:
        moduleConfig = moduleData["config"]
        
    # Create the module processing configuration.
    modConfig = ModuleConfiguration(defaultConfig, moduleConfig)
    
    # Create scratchDirMgr.
    scratchDirMgr = modConfig.getScratchDirManager()
    
    # Process resouces.
    if "resources" in moduleData:
        resources = moduleData["resources"]

        # TODO: Determine if we should check processPipelineForResource() return value and stop all 
        #       processing on failure. Currently will continue processing with next resource.
        
        # Process texture resouces.
        if "textures" in resources:
            for texture in resources["textures"]:
                processPipelineForResource(ResourceFlavor.TEXTURE, texture, scratchDirMgr, modConfig)
            
        # Process material resouces.
        if "materials" in resources:
            for material in resources["materials"]:
                processPipelineForResource(ResourceFlavor.MATERIAL, material, scratchDirMgr, modConfig)
    
        # Process object resouces.
        if "objects" in resources:
            for obj in resources["objects"]:
                processPipelineForResource(ResourceFlavor.OBJECT, obj, scratchDirMgr, modConfig)
        
        # Process mod resouces.
        if "mods" in resources:
            for mod in resources["mods"]:
                processPipelineForResource(ResourceFlavor.MOD, mod, scratchDirMgr, modConfig)
    
    # Cleanup.
    scratchDirMgr.remove()
    
    # Done.
    logger.debug("pipeline.processModuleData() - Processing complete.")


def processModuleString(defaultConfig, moduleDataString):
    """Loads JSON Module Data from a string and processes it."""

    # Assume failure.
    moduleData = None
    
    try:
        moduleData = json.loads(moduleDataString)
    except json.JSONDecodeError:
        logger.exception("pipeline.processModuleString() - Could not load pack string.")
        return
        
    if not moduleData is None:    
        processModuleData(defaultConfig, moduleData)
        

def processModuleFile(defaultConfig, moduleFile):
    """Loads JSON module data from a file-like object and processes it."""
        
    # Assume failure.
    moduleData = None
    
    try:
        moduleData = json.load(moduleFile)
    except json.JSONDecodeError:
        logger.exception("pipeline.processModuleFile() - Error loading Module File.")
        return
        
    if not moduleData is None:    
        processModuleData(defaultConfig, moduleData)


def runPipeline(defaultConfig, moduleFileNames):
    """SQS pipeline command."""
    # Assume Failure.
    moduleFile = None

    # We expect to process a list of file names.
    if not isinstance(moduleFileNames, list):
        moduleFileNames = [moduleFileNames] # Force list.
        
    for moduleFileName in moduleFileNames:
        if not moduleFileName is None and not moduleFileName == "":
            # Use passed Module File name.
            logger.debug("pipeline.runPipeline() - Module File: " + moduleFileName)
            try:
                moduleFile = open(moduleFileName)
            except:
                logger.exception("pipeline.runPipeline() - Error reading Module File.")
        else:
            # TODO: Fix here and elsewhere - this won't be reached because we are 
            #       iterating a possibly empty list.
            # TODO: Copy STDIN to scratch directory before starting?
            # Use stdin if no file name.
            #logger.info("pipeline.runPipeline() - Reading module data from STDIN.")
            logger.error("pipeline.runPipeline() - Currently STDIN not supported.")
            moduleFile = sys.stdin

        if not moduleFile is None:    
            processModuleFile(defaultConfig, moduleFile)
    