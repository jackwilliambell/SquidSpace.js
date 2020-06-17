"""                ====== SQS Common API ======

Shared code used by all SQS tools and APIs.
"""

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
        self.cacheFilters = {}
        self.packFilters = {}
        
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
            if "global-cache-filters" in defaultConfigData:
                self.cacheFilters.update(defaultConfigData["global-cache-filters"])   
            if "global-pack-filters" in defaultConfigData:
                self.packFilters.update(defaultConfigData["global-pack-filters"])   
        
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
            if "global-cache-filters" in moduleConfigData:
                self.cacheFilters.update(moduleConfigData["global-cache-filters"])   
            if "global-pack-filters" in moduleConfigData:
                self.packFilters.update(moduleConfigData["global-pack-filters"])   

