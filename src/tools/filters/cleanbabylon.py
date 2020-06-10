"""Removes unhelpful or unneeded data sections from .babylon files.
"""


copyright = """SquidSpace.js, the associated tooling, and the documentation are copyright 
Jack William Bell 2020 except where noted. All other content, including HTML files and 3D 
assets, are copyright their respective authors."""


import sys
import os
import json


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


def processFile(pathIn, pathOut):
    # DEBUG: Comment out for production.
    #print("Processing file: " + filePath);print("")
    
    # Is it a .babylon file?
    name, ext = os.path.splitext(pathIn)
    if ext == ".babylon":
        # DEBUG: Comment out for production.
        #print("Babylon file: " + pathIn);print("")
        
        try:
            # Load Babylon file
            with open(pathIn, 'r') as babFile:
                data = json.load(babFile)
                close(babFile)
                
            # Try to clean the data.
            if cleanData(data):
                # DEBUG: Comment out for production.
                print("Babylon was cleaned.");print("")
                pass
            else:
                # DEBUG: Comment out for production.
                print("Babylon did not require cleaning.");print("")
                pass
            try:
                # Write it back out.
                # TODO: This writes it packed, do we want a 'pretty print' option?
                with open(pathOut, 'w') as babFile:
                    json.dump(data, babFile)
                    close(babFile)
                # DEBUG: Comment out for production.
                print("Babylon file cleaned.");print("")
            except Exception:
                # TODO: Upgrade error handling and pass exception up.
                print("Error writing .babylon file:", sys.exc_info()[1])
        except json.JSONDecodeError:
            # TODO: Pass exception up, do not handle here.
            print("Error loading .babylon file:", sys.exc_info()[1])


def processDirectory(pathIn, pathOut, recurse):
    # DEBUG: Comment out for production.
    print("Processing path: " + path);print("")

    for item in os.listdir(path):
        if os.path.isdir(item):
            if recurse:
                processDirectory(item, recurse)
        else:
            processFile(os.path.join(pathIn, item), os.path.join(pathOut, item))

    # DEBUG: Comment out for production.
    print("Path processing complete.")
    
def filter(pathIn, pathOut, options):
    # TODO: Make some processing optional, including 'recurse' and 'packed'.
    recurse = False
    
    # TODO: Error handling.
    if os.path.isdir(pathIn):
        if os.path.isdir(pathOut)
            processDirectory(pathIn, pathOut, recurse)
        else:
            # TODO: Upgrade error handling and pass exception up.
            pass
    else:
        processFile(pathIn, pathOut)
        