#!/usr/bin/env python3
"""Reads in a 'pack' file containing JSON data and, using that data, generates
a Javascript module.

SquidSpace, the associated tooling, and the documentation are copyright Jack William Bell 2020. 
All other content, including HTML files and 3D assets, are copyright their respective
authors."""

import sys
import os
import json
from enum import Enum


class ElementAction(Enum):
    """Enumeration of supported pack actions."""
    INSERT = 1
    LINK = 2
    BUILTIN = 3


class ElementSource(Enum):
    """Enumeration of supported pack sources."""
    DATA = 1
    FILE = 2
    FILE_AND_ROOT = 3
    EMPTY = 99
    
    
class ModuleConfiguration(object):
    """Contains a module configuration."""
    def __init__(self, configData):
        """Sets the module configuration to match the passed configuration data."""
        # Set defaults
        self.pp = True; # TODO: Add 'pretty-print' to config.
        self.offset = "   " # TODO: Add 'offset' to config as number of chars.
        self.defaultFileLoader = "TODO: loader functions not currently supported." # TODO
        self.defaultUrlLoader = "TODO: loader functions not currently supported." # TODO
        
        # Get values from passed configuration, if any.
        if not configData is None and isinstance(configData, dict):
            if "pretty-print" in configData:
                self.pp = configData["pretty-print"]
            if "pretty-offset" in configData:
                self.offset = " " * configData["pretty-offset"]
            if "default-file-loader-func" in configData:
                self.defaultFileLoader = configData["default-file-loader-func"]
            if "default-url-loader-func" in configData:
                self.defaultUrlLoader = configData["default-url-loader-func"]


## TODO: insertBinary() and insertBinaryFile(), doing some kind of binary-to-text conversion.


def insertTextFile(inFilePath, outFile, singleLine = True):
    """Inserts the contents of a text file specified by the in file path into the out file."""
    
    inFile = open(inFilePath, "r")
    for line in inFile:
        if singleLine:
            outFile.write(line.replace('\n', '\\n').replace('"', '\\"'))
        else:
            outFile.write(line.replace('"', '\\"'))
    inFile.close()


def insertText(text, outFile, singleLine = True):
    """Inserts the passed text into the out file."""
    
    if singleLine:
        outFile.write(text.replace('\n', '\\n').replace('"', '\\"'))
    else:
        outFile.write(text.replace('"', '\\"'))

    
def insertReturnLinkLoaderFunc(func, link, outFile, config, singleLine = True):
    """ TODO """
    pass


def insertValue(value, outFile, config, baseOffset, singleLine = True):
    """Inserts a value into the out file."""
    
    if isinstance(value, str): # String
        outFile.write('"')
        outFile.write(value)
        outFile.write('"')
    elif isinstance(value, bool): # Boolean
        if value:
            outFile.write("true")
        else:
            outFile.write("false")
    elif isinstance(value, (int, float)): # Float
        outFile.write(str(value))
    elif isinstance(value, dict): # Dictionary
        insertDict(value, outFile, config, baseOffset + config.offset)
    elif isinstance(value, list): # List
        insertList(value, outFile, config, baseOffset + config.offset)
    

def insertList(list, outFile, config, baseOffset):
    """Insertes the contents of a list into the out file."""

    outFile.write("[")
    
    ft = False
    for value in list:
        if ft:
            outFile.write(",")
        else:
            ft = True
        if config.pp: outFile.write("\n" + baseOffset + config.offset)
        insertValue(value, outFile, config, baseOffset, singleLine = True)

    if config.pp: outFile.write("\n" + baseOffset)
    outFile.write("]")
    

def insertDict(dict, outFile, config, baseOffset):
    """Insertes the contents of a dictionary into a Module file."""

    outFile.write("{")
    
    ft = False
    for key in dict:
        if ft:
            outFile.write(",")
        else:
            ft = True
        if config.pp: outFile.write("\n" + baseOffset + config.offset)
        outFile.write('"' + key + '": ')
        insertValue(dict[key], outFile, config, baseOffset, singleLine = True)

    if config.pp: outFile.write("\n" + baseOffset)
    outFile.write("}")
    
        
def insertLoaderData(elem, outFile, config, baseOffset):
    """Inserts a function that fetches an element into the out file, where 
    the element returned is a dictionary consisting of the element data and configuration."""
    
    # Determine action requested.
    action = ElementAction.INSERT
    if "action" in elem:
        if elem["action"].lower() == "link":
            action = ElementAction.LINK
        elif elem["action"].lower() == "insert":
            action = ElementAction.INSERT
        elif elem["action"].lower() == "builtin":
            action = ElementAction.BUILTIN
        else:
            raise ValueError("Invalid 'action' value: " + elem["action"])
    else:
        raise ValueError("Action element required.")
            
    # Determine element source, based on the action.
    source = ElementSource.EMPTY
    if action == ElementAction.INSERT:
        if "data" in elem and not "file" in elem and not "root" in elem:
            source = ElementSource.DATA
        elif "file" in elem and not "data" in elem and not "root" in elem:
            source = ElementSource.FILE
        else:
            raise ValueError("Action 'insert' requires one of 'file' or 'data' element.")
    elif action == ElementAction.LINK:
        if "file" in elem and "root" in elem and not "data" in elem:
            source = ElementSource.FILE_AND_ROOT
        else:
            raise ValueError("Action 'link' requires one each of 'root' and 'file' element.")
    elif action == ElementAction.BUILTIN:
        if "data" in elem and not "file" in elem and not "root" in elem:
            source = ElementSource.DATA
        else:
            raise ValueError("Action 'builtin' requires one of 'data' element.")
    
    if source == ElementSource.EMPTY:
        raise ValueError("No valid source element supplied.")
    
    # Write the prefix
    if config.pp: outFile.write("\n" + baseOffset)
    outFile.write(elem["name"] + ": {") 

    # Write data.
    if config.pp: outFile.write("\n" + baseOffset + config.offset + config.offset)
    if (action == ElementAction.BUILTIN):
        outFile.write("\"builtin\": true,")
        if config.pp: outFile.write("\n" + baseOffset + config.offset + config.offset)
    
    if source == ElementSource.DATA:
        outFile.write("\"data\": ")
        if isinstance(elem["data"], str):
            outFile.write("\"")
            insertText(elem["data"], outFile, singleLine)
            outFile.write("\"")
        elif isinstance(elem["data"], dict):
            insertDict(elem["data"], outFile, config, baseOffset + config.offset + config.offset)
        else:
            raise ValueError("Data element must be a string for 'insert' actions or a dictionary for 'buitin' actions.")
    elif source == ElementSource.FILE:
        outFile.write("\"data\": \"")
        insertTextFile(elem["file"], outFile, singleLine = True)
        outFile.write("\"")
    elif source == ElementSource.FILE_AND_ROOT:
        outFile.write("\"root\": \"")
        insertText(elem["root"], outFile, singleLine = True)
        outFile.write("\"",)
        if config.pp: outFile.write("\n" + baseOffset + config.offset + config.offset)
        outFile.write("\"file\": \"")
        insertText(elem["file"], outFile, singleLine = True)
        outFile.write("\"")
    else:
        raise ValueError("Invalid source.")
                    
    # Write elem config, if present.
    if "config" in elem:
        outFile.write(",")
        if config.pp: outFile.write("\n" + baseOffset + config.offset + config.offset)
        outFile.write('"config": ')
        insertDict(elem["config"], outFile, config, baseOffset + config.offset + config.offset)
        
    # Write the suffix. 
    if config.pp: outFile.write("\n" + baseOffset)
    outFile.write("},") 
    
def insertLayoutData(elem, outFile, config, baseOffset):
    # TODO: Implement something more specific. 
    insertDict(elem, outFile, config, baseOffset)
    outFile.write(",")
    
    
def processModule(outDir, module):
    """Processes one module's elements and generates a module file."""
    
    # TODO: Improve error handling. Need to decide if we wrap everything in a try-catch or
    # do it line-by-line. 
    
    # DEBUG: Comment out for production.
    #print(module);print("")
    print("Writing module: " + module["name"]);print("")

    # Get configuration and set up for processing.     
    config = ModuleConfiguration(module["config"])
    offset = config.offset
    
    # TODO: make sure outdir is a proper path with a trailing slash and/or
    # use Python dir functions to generate full module path. Note that outdir
    # may be passed in as None, meaning use local dir.
    
    # Open module output file.
    mf = open(outDir + module["name"] + ".js", "w")
    
    # Write module start.
    mf.write("var " + module["name"] + " = (function(){")
    if config.pp: mf.write("\n")
        
    # Write module publics.
    if config.pp: mf.write("\n" + offset)
    mf.write("return {")
    
    baseOffset = offset + offset
    
    # Process objects.
    if "objects" in module:
        if config.pp: mf.write("\n" + baseOffset)
        mf.write("objects: {")
        for obj in module["objects"]:
            insertLoaderData(obj, mf, config, baseOffset + offset)
        if config.pp: mf.write("\n" + baseOffset)
        mf.write("},")
        
    # Process textures.
    if "textures" in module:
        if config.pp: mf.write("\n" + baseOffset)
        mf.write("textures: {")
        for texture in module["textures"]:
            insertLoaderData(texture, mf, config, baseOffset + offset)
        mf.write("},")
            
    # Process materials.
    if "materials" in module:
        if config.pp: mf.write("\n" + baseOffset)
        mf.write("materials: {")
        for material in module["materials"]:
            insertLoaderData(material, mf, config, baseOffset + offset)
        mf.write("},")
            
    # Process lights.
    if "lights" in module:
        if config.pp: mf.write("\n" + baseOffset)
        mf.write("lights: {")
        for light in module["lights"]:
            insertLoaderData(light, mf, config, baseOffset + offset)
        mf.write("},")
    
    # Process layouts.
    if "area-layouts" in module:
        if config.pp: mf.write("\n" + baseOffset)
        mf.write("layouts: [")
        for layout in module["area-layouts"]:
            if config.pp: mf.write("\n" + baseOffset + offset)
            insertLayoutData(layout, mf, config, baseOffset + offset)
        if config.pp: mf.write("\n" + baseOffset)
        mf.write("]")
    
    # Write module end.
    if config.pp: mf.write("\n" + offset)
    mf.write("};")
    if config.pp: mf.write("\n")
    mf.write("})();")
    
    # Clean up.
    mf.close()
    
    
def processPackData(packData):
    """Processes the Pack Data to generate module files."""
    # TODO: Document pack data.
    
    # DEBUG: Comment out for production.
    print("Processing Pack Data.");print("")
    #print(packData);print("")
    
    # Get configuration and set up for processing.
    outDir = None
    if "config" in packData:
        config = packData["config"]
        
        if "outdir" in config and not config["outdir"] == "":
            outDir = config["outdir"]
    
    # Write Modules.
    if "modules" in packData:
        for module in packData["modules"]:
            processModule(outDir, module)

    # DEBUG: Comment out for production.
    print("Processing complete.");print("")


def processPackString(packString):
    """Loads JSON Pack Data from a string and processes it."""

    # Assume failure.
    packData = None
    
    try:
        packData = json.loads(processPackString)
    except json.JSONDecodeError:
        # TODO: Pass exception up, do not handle here.
        print("Could not load pack string.")
        
    if not packData is None:    
        processPackData(packData)


def processPackFile(packFile):
    """Loads JSON Pack Data from a file and processes it."""
        
    # Assume failure.
    packData = None
    
    try:
        packData = json.load(packFile)
    except json.JSONDecodeError:
        # TODO: Pass exception up, do not handle here.
        print("Error loading pack file:", sys.exc_info()[1])
        
    if not packData is None:    
        processPackData(packData)


def main(packFileName):
    # Assume Failure.
    packFile = None
    
    if not packFileName is None and not packFileName == "":
        # Use passed packFile name.
        print("Pack File: " + packFileName);print("")
        try:
            packFile = open(packFileName)
        except:
            print("Error reading pack file:", sys.exc_info()[1])
    else:
        # Use stdin if no file name.
        print("Pack Data from STDIN.");print("")
        packFile = sys.stdin

    if not packFile is None:    
        processPackFile(packFile)
    
    
if __name__ == '__main__':
    # TODO: Support command line arguments for pack file name(s).
    main("squidhall.pack.json")
    main("furniture.pack.json")