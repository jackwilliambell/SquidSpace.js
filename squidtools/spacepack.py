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


class ResourceFlavor(Enum):
    """Enumeration of supported resource types."""
    TEXTURE = 0
    MATERIAL = 1
    OBJECT = 2
    MOD = 3
    
class ResourceAction(Enum):
    """Enumeration of supported resource pack-options actions."""
    NONE = 0
    INSERT = 1
    LINK = 2
    
    
class ModuleConfiguration(object):
    """Contains a module configuration."""
    def __init__(self, worldConfigData, fileConfigData, moduleConfigData):
        """Sets the module configuration to match the passed configuration data."""
        
        # Start by setting defaults
        self.pp = True; 
        self.offset = " " * 3 # Default to three spaces.
        self.outDir = "build/"
        self.texDir = "assets/textures/"
        self.matDir = "assets/materials/"
        self.objDir = "assets/objects/"
        self.modDir = "assets/mods/"
        
        # TODO: make sure the 'dir' values are proper paths with a trailing slash and/or
        # use Python dir functions to generate full path. 
        
        # Override with values from passed world configuration, if any.
        if not worldConfigData is None and isinstance(worldConfigData, dict):
            if "pretty-print" in worldConfigData:
                self.pp = worldConfigData["pretty-print"]
            if "pretty-offset" in worldConfigData:
                # TODO: Verify "pretty-offset" is an integer.
                self.offset = " " * worldConfigData["pretty-offset"]
            if "out-dir" in worldConfigData:
                self.outDir = worldConfigData["out-dir"]
            if "texture-dir" in worldConfigData:
                self.texDir = worldConfigData["texture-dir"]
            if "material-dir" in worldConfigData:
                self.matDir = worldConfigData["material-dir"]
            if "object-dir" in worldConfigData:
                self.objDir = worldConfigData["object-dir"]
            if "mod-dir" in worldConfigData:
                self.modDir = worldConfigData["mod-dir"]   
        
        # Override with values from passed file configuration, if any.
        if not fileConfigData is None and isinstance(fileConfigData, dict):
            if "pretty-print" in fileConfigData:
                self.pp = fileConfigData["pretty-print"]
            if "pretty-offset" in fileConfigData:
                # TODO: Verify "pretty-offset" is an integer.
                self.offset = " " * fileConfigData["pretty-offset"]
            if "out-dir" in fileConfigData:
                self.outDir = fileConfigData["out-dir"]
            if "texture-dir" in fileConfigData:
                self.texDir = fileConfigData["texture-dir"]
            if "material-dir" in fileConfigData:
                self.matDir = fileConfigData["material-dir"]
            if "object-dir" in fileConfigData:
                self.objDir = fileConfigData["object-dir"]
            if "mod-dir" in fileConfigData:
                self.modDir = fileConfigData["mod-dir"]   
                         
        # Override with values from passed module configuration, if any.
        if not moduleConfigData is None and isinstance(moduleConfigData, dict):
            if "pretty-print" in moduleConfigData:
                self.pp = moduleConfigData["pretty-print"]
            if "pretty-offset" in moduleConfigData:
                # TODO: Verify "pretty-offset" is an integer.
                self.offset = " " * moduleConfigData["pretty-offset"]
            if "out-dir" in moduleConfigData:
                self.outDir = moduleConfigData["out-dir"]
            if "texture-dir" in moduleConfigData:
                self.texDir = moduleConfigData["texture-dir"]
            if "material-dir" in moduleConfigData:
                self.matDir = moduleConfigData["material-dir"]
            if "object-dir" in moduleConfigData:
                self.objDir = moduleConfigData["object-dir"]
            if "mod-dir" in moduleConfigData:
                self.modDir = moduleConfigData["mod-dir"]            


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

    
def insertReturnLinkLoaderFunc(func, link, outFile, modConfig, singleLine = True):
    """ TODO """
    pass


def insertValue(value, outFile, modConfig, baseOffset, singleLine = True):
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
        insertDict(value, outFile, modConfig, baseOffset + modConfig.offset)
    elif isinstance(value, list): # List
        insertList(value, outFile, modConfig, baseOffset + modConfig.offset)
    

def insertList(list, outFile, modConfig, baseOffset):
    """Insertes the contents of a list into the out file."""

    outFile.write("[")
    
    ft = False
    for value in list:
        if ft:
            outFile.write(",")
        else:
            ft = True
        if modConfig.pp: outFile.write("\n" + baseOffset + modConfig.offset)
        insertValue(value, outFile, modConfig, baseOffset, singleLine = True)

    if modConfig.pp: outFile.write("\n" + baseOffset)
    outFile.write("]")
    

def insertDict(dict, outFile, modConfig, baseOffset):
    """Insertes the contents of a dictionary into a Module file."""

    outFile.write("{")
    
    ft = False
    for key in dict:
        if ft:
            outFile.write(",")
        else:
            ft = True
        if modConfig.pp: outFile.write("\n" + baseOffset + modConfig.offset)
        outFile.write('"' + key + '": ')
        insertValue(dict[key], outFile, modConfig, baseOffset, singleLine = True)

    if modConfig.pp: outFile.write("\n" + baseOffset)
    outFile.write("}")
    
        
def insertResourceData(resourceFlavor, elem, outFile, modConfig, baseOffset):
    """Adds values based on the passed in resource values and the resource flavor; 
    handles data inserts if required."""
    
    # Get resource values.
    name = None # Default.
    if "name" in elem:
        name = elem["name"]
    config = None # Default.
    if "config" in elem:
        config = elem["config"]
    options = {} # Default is empty dict.
    if "options" in elem:
        options = elem["options"]
    data = None # Default.
    if "data" in elem:
        data = elem["data"]
        
    # Validate resource values.
    if not isinstance(name, str) and name != "":
        raise ValueError("Resource name is required.")
    if config != None and not isinstance(config, dict):
        raise ValueError("Resource config must be a JSON object or not provided.")
    if options != None and not isinstance(options, dict):
        raise ValueError("Resource options must be a JSON object or not provided.")
    
    # Get the data source values.
    urlVal = None
    if config != None and "url" in config:
        urlVal = config["url"]
    fileNameVal = None
    if config != None and "file-name" in config:
        fileNameVal = config["file-name"]
    dirVal = None
    if config != None and "dir" in config: 
        dirVal = config["dir"]
    elif resourceFlavor == ResourceFlavor.TEXTURE:
        dirVal = modConfig.texDir
    elif resourceFlavor == ResourceFlavor.MATERIAL:
        dirVal = modConfig.matDir
    elif resourceFlavor == ResourceFlavor.OBJECT:
        dirVal = modConfig.objDir
    elif resourceFlavor == ResourceFlavor.MOD:
        dirVal = modConfig.modDir
                
    # Determine pack action requested.
    action = ResourceAction.NONE
    if config != None and "pack-options" in config:
        popts = config["pack-options"]
        if popts["action"].lower() == "link":
            action = ResourceAction.LINK
        elif popts["action"].lower() == "insert":
            action = ResourceAction.INSERT
        elif popts["action"].lower() == "none":
            action = ResourceAction.NONE
        else:
            raise ValueError("Invalid Resource 'action' value: " + popts["action"])
    
    # Validate pack action and data source values.
    if not isinstance(dirVal, str):
        raise ValueError("Invalid 'dir' value.")
    if urlVal != None and fileNameVal != None:
        raise ValueError("Cannot specify both file name and URL.")
    if action == ResourceAction.NONE and (urlVal != None or fileNameVal != None):
        raise ValueError("File name and URL not allowed if resource action is 'none'.")
    if action == ResourceAction.LINK and urlVal == None and fileNameVal == None:
        raise ValueError("File name or URL required if resource action is 'link'.")
    if action == ResourceAction.INSERT and urlVal == None and fileNameVal == None:
        raise ValueError("File name or URL required if resource action is 'insert'.")
    
    # Write the prefix
    if modConfig.pp: outFile.write("\n" + baseOffset)
    outFile.write(name + ": {") 

    # Write options, if present.
    if options != None:
        if modConfig.pp: outFile.write("\n" + baseOffset + modConfig.offset + modConfig.offset)
        outFile.write('"options": ')
        insertDict(options, outFile, modConfig, baseOffset + modConfig.offset + modConfig.offset)
        outFile.write(",")

    # Write data based on the action and the source.
    if action == ResourceAction.NONE and data != None:
        if modConfig.pp: outFile.write("\n" + baseOffset + modConfig.offset + modConfig.offset)
        outFile.write('"data": ')
        insertValue(data, outFile, modConfig, baseOffset + modConfig.offset + modConfig.offset)
    elif action == ResourceAction.LINK and urlVal != None:
        if modConfig.pp: outFile.write("\n" + baseOffset + modConfig.offset + modConfig.offset)
        outFile.write('"data": ')
        insertText(urlVal, outFile)
    elif action == ResourceAction.LINK and fileNameVal != None:
        if modConfig.pp: outFile.write("\n" + baseOffset + modConfig.offset + modConfig.offset)
        outFile.write('"data": ')
        insertDict({"dir": dirVal, "file-name": fileNameVal}, outFile, 
                    modConfig, baseOffset + modConfig.offset + modConfig.offset)
    elif action == ResourceAction.INSERT and urlVal != None:
        # TODO: Implement.
        raise NotImplementedError("At this time 'insert' actions with 'url' sources are not supported.")
    elif action == ResourceAction.INSERT and fileNameVal != None:
        if modConfig.pp: outFile.write("\n" + baseOffset + modConfig.offset + modConfig.offset)
        outFile.write('"data": ')
        insertTextFile(dirVal + fileNameVal, outFile, singleLine = True)
            
    # Write the suffix. 
    if modConfig.pp: outFile.write("\n" + baseOffset)
    outFile.write("},") 
    
    
def insertLayoutData(elem, outFile, config, baseOffset):
    # TODO: Implement something more specific. 
    insertDict(elem, outFile, config, baseOffset)
    outFile.write(",")
    
    
def processModule(worldConfig, fileConfig, module):
    """Processes one module's elements and generates a module file."""
    
    # TODO: Improve error handling. Need to decide if we wrap everything in a try-catch or
    # do it line-by-line. 
    
    # DEBUG: Comment out for production.
    #print(module);print("")
    print("Writing module: " + module["name"]);print("")
    
    # Get module configuration.
    moduleConfig = {} # Default config is empty dict.
    if "config" in module:
        moduleConfig = module["config"]
        
    # Create the module processing configuration.
    modConfig = ModuleConfiguration(worldConfig, fileConfig, moduleConfig)
    
    # Open module output file.
    mf = open(modConfig.outDir + module["name"] + ".js", "w")
    
    # Write module start.
    mf.write("var " + module["name"] + " = (function(){")
    if modConfig.pp: mf.write("\n")
        
    # Write module publics.
    if modConfig.pp: mf.write("\n" + modConfig.offset)
    mf.write("return {")
    
    baseOffset = modConfig.offset + modConfig.offset
    
    # Process resouces.
    if "resources" in module:
        resources = module["resources"]
        
        # Process texture resouces.
        if "textures" in module:
            if modConfig.pp: mf.write("\n" + baseOffset)
            mf.write("textures: {")
            for texture in resources["textures"]:
                insertResourceData(ResourceFlavor.TEXTURE, texture, mf, modConfig, 
                                    baseOffset + modConfig.offset)
            mf.write("},")
            
        # Process material resouces.
        if "materials" in module:
            if modConfig.pp: mf.write("\n" + baseOffset)
            mf.write("materials: {")
            for material in resources["materials"]:
                insertResourceData(ResourceFlavor.MATERIAL, material, mf, 
                                    modConfig, baseOffset + modConfig.offset)
            mf.write("},")
    
        # Process object resouces.
        if "objects" in resources:
            if modConfig.pp: mf.write("\n" + baseOffset)
            mf.write("objects: {")
            for obj in resources["objects"]:
                insertResourceData(ResourceFlavor.OBJECT, obj, mf, modConfig, 
                                    baseOffset + modConfig.offset)
            if modConfig.pp: mf.write("\n" + baseOffset)
            mf.write("},")
        
        # Process mod resouces.
        if "mods" in resources:
            if modConfig.pp: mf.write("\n" + baseOffset)
            mf.write("mods: {")
            for mod in resources["mods"]:
                insertResourceData(ResourceFlavor.MOD, mod, mf, modConfig, 
                                    baseOffset + modConfig.offset)
            if modConfig.pp: mf.write("\n" + baseOffset)
            mf.write("},")
    
    # Process layouts.
    # TODO: Fix and uncomment.
    #if "layouts" in module:
    #    if modConfig.pp: mf.write("\n" + baseOffset)
    #    mf.write("layouts: {")
    #    for layout in module["layouts"]:
    #        if modConfig.pp: mf.write("\n" + baseOffset + offset)
    #        insertLayoutData(layout, mf, config, baseOffset + modConfig.offset)
    #    if modConfig.pp: mf.write("\n" + baseOffset)
    #    mf.write("}")
    
    # Write module end.
    if modConfig.pp: mf.write("\n" + modConfig.offset)
    mf.write("};")
    if modConfig.pp: mf.write("\n")
    mf.write("})();")
    
    # Clean up.
    mf.close()
    
    
def processPackData(worldConfig, packData):
    """Processes the Pack Data to generate module files."""
    # TODO: Document pack data.
    
    # DEBUG: Comment out for production.
    print("Processing Pack Data.");print("")
    #print(packData);print("")
    
    # Get file configuration and set up for processing.
    fileConfig = {} # Default config is empty dict.
    if "config" in packData:
        fileConfig = packData["config"]
            
    # Write Modules.
    if "modules" in packData:
        for module in packData["modules"]:
            processModule(worldConfig, fileConfig, module)

    # DEBUG: Comment out for production.
    print("Processing complete.");print("")


def processPackString(worldConfig, packString):
    """Loads JSON Pack Data from a string and processes it."""

    # Assume failure.
    packData = None
    
    try:
        packData = json.loads(processPackString)
    except json.JSONDecodeError:
        # TODO: Pass exception up, do not handle here.
        print("Could not load pack string.")
        
    if not packData is None:    
        processPackData(worldConfig, packData)


def processPackFile(worldConfig, packFile):
    """Loads JSON Pack Data from a file and processes it."""
        
    # Assume failure.
    packData = None
    
    try:
        packData = json.load(packFile)
    except json.JSONDecodeError:
        # TODO: Pass exception up, do not handle here.
        print("Error loading pack file:", sys.exc_info()[1])
        
    if not packData is None:    
        processPackData(worldConfig, packData)


def main(packFileName):
    # Assume Failure.
    packFile = None
    
    # TODO: Get world config when loading.
    worldConfig = {}
    
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
        processPackFile(worldConfig, packFile)
    
    
if __name__ == '__main__':
    # TODO: Support command line arguments for pack file name(s).
    main("squidhall.pack.json")
    #main("furniture.pack.json")