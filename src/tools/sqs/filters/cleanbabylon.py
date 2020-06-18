"""## cleanbabylon.py – SQS Filter for cleaning .babylon files

Removes unhelpful or unneeded data sections from .babylon files. At this time 
there are no options supported.

Besides the standard filter() function there are two API functions:

* cleanData(data) - Cleans a dictionary containing a parsed .babylon file

* processDirectory(pathIn, pathOut, recurse) - Cleans all .babylon files in 
  the directory specified with pathIn, writing the files out to pathOut. If
  pathIn and pathOut are the same it will operate destructively, overwriting
  the files.
"""


copyright = """SquidSpace.js, the associated tooling, and the documentation are copyright 
Jack William Bell 2020 except where noted. All other content, including HTML files and 3D 
assets, are copyright their respective authors."""


import sys
import os
import json
from sqs.sqslogger import logger

    
def cleanData(data):
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


def processDirectory(pathIn, pathOut, recurse):
    logger.debug("cleanbabylon.processDirectory() - Processing pathIn: {pathIn} pathOut: {pathOut} recurse: {recurse}".format(pathIn, pathOut, recurse))

    for item in os.listdir(path):
        if os.path.isdir(item):
            if recurse:
                processDirectory(item, recurse)
        else:
            filter(os.path.join(pathIn, item), os.path.join(pathOut, item))

    # DEBUG: Comment out for production.
    #print("Path processing complete.")


def filter(pathIn, pathOut, options):
    # NOTE: Currently supports no options.
    logger.debug("cleanbabylon.filter() - Processing pathIn: {pathIn} pathOut: {pathOut} options: options".format(pathIn, pathOut, options))
    
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
            if cleanData(data):
                # DEBUG: Comment out for production.
                #print("Babylon was cleaned.");print("")
                pass
            else:
                # DEBUG: Comment out for production.
                #print("Babylon did not require cleaning.");print("")
                pass
            try:
                # Write it back out.
                # TODO: This writes it packed, do we want a 'pretty print' option?
                with open(pathOut, 'w') as babFile:
                    json.dump(data, babFile)
                    close(babFile)
                # DEBUG: Comment out for production.
                #print("Babylon file cleaned.");print("")
                return = True
            except Exception:
                logger.exception("shellexec.filter() - Command '{command}' failed to write output.".format(command)
        except json.JSONDecodeError:
            logger.error("shellexec.filter() - Command '{command}' failed to parse the .babylon file.".format(command)

    return result