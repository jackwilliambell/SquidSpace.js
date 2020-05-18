#!/usr/bin/env python3
"""Removes unhelpful or unneeded data sections from .babylon files.

SquidSpace, the associated tooling, and the documentation are copyright Jack William Bell 2020. 
All other content, including HTML files and 3D assets, are copyright their respective
authors.
"""

import sys
import os
import json

def cleanData(data):
    dirty = False
    
    # Check for unwanted sections and clean them.
    
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

def processFile(filePath):
    # DEBUG: Comment out for production.
    #print("Processing file: " + filePath);print("")
    
    # Is it a .babylon file?
    name, ext = os.path.splitext(filePath)
    if ext == ".babylon":
        # DEBUG: Comment out for production.
        print("Babylon file: " + filePath);print("")
        
        try:
            # Load Babylon file
            with open(filePath, 'r') as babFile:
                data = json.load(babFile)
                
            # Try to clean the data.
            if cleanData(data):
                try:
                    # Write it back out.
                    # TODO: This writes it packed, do we want a 'pretty print' option?
                    with open(filePath, 'w') as babFile:
                        json.dump(data, babFile)
                    print("Babylon file cleaned.");print("")
                except Exception:
                    # TODO: Upgrade error handling and pass exception up.
                    pass
            else:
                print("Babylon did not require cleaning.");print("")
        except json.JSONDecodeError:
            # TODO: Pass exception up, do not handle here.
            print("Error loading .babylon file:", sys.exc_info()[1])        
        

def processDirectory(path, recurse):
    # DEBUG: Comment out for production.
    print("Processing path: " + path);print("")

    for item in os.listdir(path):
        if os.path.isdir(item):
            if recurse:
                processDirectory(item, recurse)
        else:
            processFile(os.path.join(path, item))

    # DEBUG: Comment out for production.
    print("Path processing complete.")
    

def main(path, recurse):
    # Is the path a file or a directory?
    if os.path.isdir(path):
        processDirectory(path, recurse)
    else:
        processFile(path)
    
    
if __name__ == '__main__':
    # TODO: Support command line arguments for path and directory recursion.
    main("objects", False)