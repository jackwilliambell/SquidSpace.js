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

def processModuleFile(defaultConfig, moduleFile):
    pass

def runPipeline(defaultConfig, moduleFileNames):
    # Assume Failure.
    moduleFile = None

    # We expect to process a list of file names.
    if not isinstance(moduleFileNames, list):
        moduleFileNames = [moduleFileNames] # Force list.
        
    for moduleFileName in moduleFileNames:
        if not moduleFileName is None and not moduleFileName == "":
            # Use passed Module File name.
            print("Module File: " + moduleFileName);print("")
            try:
                moduleFile = open(moduleFileName)
            except:
                print("Error reading Module File:", sys.exc_info()[1])
        else:
            # Use stdin if no file name.
            print("Reading module data from STDIN.");print("")
            moduleFile = sys.stdin

        if not moduleFile is None:    
            processModuleFile(defaultConfig, moduleFile)
    