"""## cleanbabylon.py – SQS Filter Module for cleaning .babylon files

Removes unhelpful or unneeded data sections from .babylon files. 

Besides the standard filterFile() functions there are two API functions:

1. cleanBabylonData(data) - Cleans a Python dictionary containing a parsed .babylon file

2. cleanBabylonFile(pathIn, pathOut, options, logger) – Cleans the data of a .babylon 
  file specified in pathIn and writes it to pathOut

### Filter File function

Options: None.

File Extensions supported:

* in – .babylon

* out – .babylon"""


copyright = """SquidSpace.js, the associated tooling, and the documentation are copyright 
Jack William Bell 2020 except where noted. All other content, including HTML files and 3D 
assets, are copyright their respective authors."""


import sys
import os
import json
    
    
def cleanBabylonData(data):
    """Cleans the data of a parsed .babylon file. Returns True if there was something 
    to clean, otherwise returns False to indicate the data was not 'dirty'."""
    dirty = False
    
    # Check for other unwanted sections and clean them.
    
    if "cameras" in data:
        #del data["cameras"]
        if len(data["cameras"]) > 0:
            data["cameras"] = [] # Make it an empty list.
            dirty = True
        
    if "activeCameraID" in data:
        del data["activeCameraID"]
        dirty = True

    if "gravity" in data:
        del data["gravity"]
        dirty = True

    if "lights" in data:
        #del data["lights"]
        if len(data["lights"]) > 0:
            data["lights"] = [] # Make it an empty list.
            dirty = True
        
    # Add other sections we want to remove here.
    
    # Done!
    return dirty
    

def cleanBabylonFile(pathIn, pathOut, options, logger):
    """Cleans the data of a .babylon file specified in pathIn and writes it to
    pathOut. Returns True on success, otherwise returns False.
    
    NOTE: Currently supports no options."""
    
    logger.debug("cleanbabylon.cleanBabylonFile() - Processing pathIn: {pathIn} pathOut: {pathOut}".format(pathIn, pathOut))
    
    # Assume failure.
    result = False
    
    # Is it a .babylon file?
    name, ext = os.path.splitext(pathIn)
    if ext == ".babylon":
        try:
            # Load Babylon file
            with open(pathIn, 'r') as babFile:
                data = json.load(babFile)
                close(babFile)
            
            # Try to clean the data.
            if cleanBabylonData(data):
                logger.debug("cleanbablyon.cleanBabylonFile() - Babylon file was cleaned.")
            else:
                logger.debug("cleanbablyon.cleanBabylonFile() - Babylon file did not require cleaning.")
            try:
                # Write it back out. (We do this even if the clean did nothing, because 
                # output and input may be/should be different files.)
                # TODO: This writes it packed, do we want a 'pretty print' option?
                with open(pathOut, 'w') as babFile:
                    json.dump(data, babFile)
                    close(babFile)
                logger.debug("Babylon file written out.")
                result = True
            except:
                logger.exception("cleanbablyon.cleanBabylonFile() - Could not write output file '{0}', continuing processing.".format(pathOut))
        except:
                logger.exception("cleanbablyon.cleanBabylonFile() - Could not read input file '{0}', continuing processing.".format(pathIn))
    else:
        logger.error("cleanbablyon.cleanBabylonFile() - Input file '{0}' is not a .babylon file.".format(pathIn))
    
    return result
    

def filterFiles(inputs, outputs, options, logger):
    """SQS filter files function that 'cleans' Babylon files.
    
    NOTE: Currently supports no options."""
    
    logger.debug("cleanbablyon.filterFiles().")
    
    # Setup
    result = 0

    # Process input files.
    for pathIn in inputs:
        if cleanBabylonFile(pathIn, outputs(os.path.basename(pathIn)), options, logger):
            result = result + 1
            
    # Done.
    return result
    