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
import json

from common import ResourceFlavor, ResourceAction, ModuleConfiguration
from sqslogger import logger


def processPipelineForResource(resourceFlavor, elem, modConfig):
    """Processes the pipeline for one resource file element."""
    if not "cache-options" in elem:
        # No need to process!
        return true
        
    


def processModuleData(defaultConfig, moduleData):
    """Processes the Module Data to manage an asset pipeline."""
    
    #logger.debug("pipeline.processModuleData() - Processing module data %{0}s.".format(moduleData))
    logger.debug("pipeline.processModuleData() - Processing pipeline for module: " + module["module-name"])
    
    # Get module configuration.
    moduleConfig = {} # Default config is empty dict.
    if "config" in module:
        moduleConfig = module["config"]
        
    # Create the module processing configuration.
    modConfig = ModuleConfiguration(defaultConfig, moduleConfig)
    
    # Process resouces.
    if "resources" in module:
        resources = module["resources"]
        
        # Process texture resouces.
        if "textures" in resources:
            for texture in resources["textures"]:
                processPipelineForResource(ResourceFlavor.TEXTURE, texture, modConfig)
            
        # Process material resouces.
        if "materials" in resources:
            for material in resources["materials"]:
                processPipelineForResource(ResourceFlavor.MATERIAL, material, modConfig)
    
        # Process object resouces.
        if "objects" in resources:
            for obj in resources["objects"]:
                processPipelineForResource(ResourceFlavor.OBJECT, obj, modConfig)
        
        # Process mod resouces.
        if "mods" in resources:
            for mod in resources["mods"]:
                processPipelineForResource(ResourceFlavor.MOD, mod, modConfig)

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
    """Loads JSON module data from a file and processes it."""
        
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
            # Use stdin if no file name.
            logger.debug("pipeline.runPipeline() - Reading module data from STDIN.")
            moduleFile = sys.stdin

        if not moduleFile is None:    
            processModuleFile(defaultConfig, moduleFile)
    