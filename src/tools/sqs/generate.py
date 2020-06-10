"""                ====== SquidSpace.js Generate ======
The SquidSpace.js 'generate' command reads in a 'module' file containing JSON data meeting the 
Module File Specification and using the SquidSpace.js Module File extensions. Then, with 
that data, it generates a Javascript module containing the everything specified in the module
file, including external data files 'packed' into the Javascript module.

For more information on Module Files and SquidSpace.js, please refer to the documentation 
located in the project repo at https://github.com/jackwilliambell/SquidSpace.js"""


copyright = """SquidSpace.js, the associated tooling, and the documentation are copyright 
Jack William Bell 2020 except where noted. All other content, including HTML files and 3D 
assets, are copyright their respective authors."""


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
    def __init__(self, defaultConfigData, moduleConfigData):
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
        if not defaultConfigData is None and isinstance(defaultConfigData, dict):
            if "pretty-print" in defaultConfigData:
                self.pp = defaultConfigData["pretty-print"]
            if "pretty-offset" in defaultConfigData:
                # TODO: Verify "pretty-offset" is an integer.
                self.offset = " " * defaultConfigData["pretty-offset"]
            if "out-dir" in defaultConfigData:
                self.outDir = defaultConfigData["out-dir"]
            if "texture-dir" in defaultConfigData:
                self.texDir = defaultConfigData["texture-dir"]
            if "material-dir" in defaultConfigData:
                self.matDir = defaultConfigData["material-dir"]
            if "object-dir" in defaultConfigData:
                self.objDir = defaultConfigData["object-dir"]
            if "mod-dir" in defaultConfigData:
                self.modDir = defaultConfigData["mod-dir"]   
                                 
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
    """Adds values to the out file based on the passed in resource and the resource flavor; 
    handles data inserts if required."""
    
    # Get resource values.
    name = None # Default.
    if "resource-name" in elem:
        name = elem["resource-name"]
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
        # TODO: Implement differently based on file type (BASE64, etc.).
        raise NotImplementedError("At this time 'insert' actions with 'url' sources are not supported.")
    elif action == ResourceAction.INSERT and fileNameVal != None:
        if modConfig.pp: outFile.write("\n" + baseOffset + modConfig.offset + modConfig.offset)
        outFile.write('"data": "')
        # TODO: Implement differently based on file type (BASE64, etc.).
        insertTextFile(dirVal + fileNameVal, outFile, singleLine = True)
        outFile.write('"')
    else:
        raise ValueError("Unknown action/source combination.")
            
    # Write the suffix. 
    if modConfig.pp: outFile.write("\n" + baseOffset)
    outFile.write("},") 


def insertLayoutData(elem, outFile, modConfig, baseOffset):
    """Adds values to the out file based on the passed in layout."""
    
    # Get layout values.
    name = None # Default.
    if "layout-name" in elem:
        name = elem["layout-name"]
    options = {} # Default is empty dict.
    if "options" in elem:
        options = elem["options"]
    objPlacements = [] # Default is empty list.
    if "data" in elem:
        objPlacements = elem["data"]
        
    # Validate layout values.
    if not isinstance(name, str) and name != "":
        raise ValueError("Layout name is required.")
    if options != None and not isinstance(options, dict):
        raise ValueError("Layout options must be a JSON object or not provided.")
    if objPlacements != None and not isinstance(objPlacements, list):
        raise ValueError("Layout object placements must be a JSON array or not provided.")
    
    # Write the prefix.
    if modConfig.pp: outFile.write("\n" + baseOffset)
    outFile.write('"' + name+ '": {') 

    # Write options, if present.
    if options != None:
        if modConfig.pp: outFile.write("\n" + baseOffset + modConfig.offset)
        outFile.write('"options": ')
        insertDict(options, outFile, modConfig, baseOffset + modConfig.offset)
        outFile.write(",")
    
    # Write object placements, if present.
    if objPlacements != None:
        if modConfig.pp: outFile.write("\n" + baseOffset + modConfig.offset)
        outFile.write('"objectPlacements": [')
        for objPlacement in objPlacements:
            if modConfig.pp: outFile.write("\n" + baseOffset + modConfig.offset + modConfig.offset)
            insertDict(objPlacement, outFile, modConfig, baseOffset + modConfig.offset + modConfig.offset)
            outFile.write(",")
        if modConfig.pp: outFile.write("\n" + baseOffset + modConfig.offset)
        outFile.write("]")
            
    # Write the suffix. 
    if modConfig.pp: outFile.write("\n" + baseOffset)
    outFile.write("},") 
    
    
def processModule(defaultConfig, module):
    """Processes one module's elements and generates a module file."""
    
    # TODO: Improve error handling. Need to decide if we wrap everything in a try-catch or
    # do it line-by-line. 
    
    # DEBUG: Comment out for production.
    #print(module);print("")
    print("Writing module: " + module["module-name"]);print("")
    
    # Get module configuration.
    moduleConfig = {} # Default config is empty dict.
    if "config" in module:
        moduleConfig = module["config"]
        
    # Create the module processing configuration.
    modConfig = ModuleConfiguration(defaultConfig, moduleConfig)
    
    # Open module output file.
    mf = open(modConfig.outDir + module["module-name"].lower() + ".js", "w")
    
    # Write module start.
    mf.write("var " + module["module-name"] + " = (function(){")
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
    if "layouts" in module:
        if modConfig.pp: mf.write("\n" + baseOffset)
        mf.write("layouts: {")
        for layout in module["layouts"]:
            if modConfig.pp: mf.write("\n" + baseOffset +  modConfig.offset)
            insertLayoutData(layout, mf, modConfig, baseOffset + modConfig.offset)
        if modConfig.pp: mf.write("\n" + baseOffset)
        mf.write("}")
    
    # Write module end.
    if modConfig.pp: mf.write("\n" + modConfig.offset)
    mf.write("};")
    if modConfig.pp: mf.write("\n")
    mf.write("})();")
    
    # Clean up.
    mf.close()
    
    
def processModuleData(defaultConfig, moduleData):
    """Processes the Module Data to generate a module file."""
    # TODO: Document module data.
    
    # DEBUG: Comment out for production.
    print("Processing module data.");print("")
    #print(moduleData);print("")
                
    # Write Module.
    processModule(defaultConfig, moduleData)

    # DEBUG: Comment out for production.
    print("Processing complete.");print("")


def processModuleString(defaultConfig, moduleDataString):
    """Loads JSON Module Data from a string and processes it."""

    # Assume failure.
    moduleData = None
    
    try:
        moduleData = json.loads(moduleDataString)
    except json.JSONDecodeError:
        # TODO: Pass exception up, do not handle here.
        print("Could not load pack string.")
        
    if not moduleData is None:    
        processModuleData(defaultConfig, moduleData)


def processModuleFile(defaultConfig, moduleFile):
    """Loads JSON module data from a file and processes it."""
        
    # Assume failure.
    moduleData = None
    
    try:
        moduleData = json.load(moduleFile)
    except json.JSONDecodeError:
        # TODO: Pass exception up, do not handle here.
        print("Error loading Module File:", sys.exc_info()[1])
        
    if not moduleData is None:    
        processModuleData(defaultConfig, moduleData)


def runGenerate(defaultConfig, moduleFileNames):
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
    