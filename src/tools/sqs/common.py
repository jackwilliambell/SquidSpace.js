"""## SQS Common API 

Shared code used by all SQS tools and APIs.
"""

from enum import Enum
import os 
import shutil
from sqslogger import logger
from filters.shellexec import filterFileExtensions as shellexec_filter_ext, filter as shellexec_filter, __doc__ as shellexec_doc
from filters.cleanbabylon import filterFileExtensions as cleanbab_filter_ext, filter as cleanbab_filter, __doc__ as cleanbab_doc


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
        self.bldDir = "build/"
        self.genDir = "libs/modules/"
        self.texDir = "assets/textures/"
        self.matDir = "assets/materials/"
        self.objDir = "assets/objects/"
        self.modDir = "assets/mods/"
        self.filterProfiles = {}
        
        # TODO: make sure the 'dir' values are proper paths with a trailing slash and/or
        # use Python dir functions to generate full path. 
        
        # Override with values from passed world configuration, if any.
        if not defaultConfigData is None and isinstance(defaultConfigData, dict):
            if "pretty-print" in defaultConfigData:
                self.pp = defaultConfigData["pretty-print"]
            if "pretty-offset" in defaultConfigData:
                # TODO: Verify "pretty-offset" is an integer.
                self.offset = " " * defaultConfigData["pretty-offset"]
            if "build-dir" in defaultConfigData:
                self.bldDir = defaultConfigData["build-dir"]
            if "generate-dir" in defaultConfigData:
                self.genDir = defaultConfigData["generate-dir"]
            if "texture-dir" in defaultConfigData:
                self.texDir = defaultConfigData["texture-dir"]
            if "material-dir" in defaultConfigData:
                self.matDir = defaultConfigData["material-dir"]
            if "object-dir" in defaultConfigData:
                self.objDir = defaultConfigData["object-dir"]
            if "mod-dir" in defaultConfigData:
                self.modDir = defaultConfigData["mod-dir"]   
            if "filter-profiles" in defaultConfigData:
                self.filterProfiles.update(defaultConfigData["filter-profiles"])    
        
        # Override with values from passed module configuration, if any.
        if not moduleConfigData is None and isinstance(moduleConfigData, dict):
            if "pretty-print" in moduleConfigData:
                self.pp = moduleConfigData["pretty-print"]
            if "pretty-offset" in moduleConfigData:
                # TODO: Verify "pretty-offset" is an integer.
                self.offset = " " * moduleConfigData["pretty-offset"]
            if "build-dir" in moduleConfigData:
                self.bldDir = moduleConfigData["build-dir"]
            if "generate-dir" in moduleConfigData:
                self.genDir = moduleConfigData["generate-dir"]
            if "texture-dir" in moduleConfigData:
                self.texDir = moduleConfigData["texture-dir"]
            if "material-dir" in moduleConfigData:
                self.matDir = moduleConfigData["material-dir"]
            if "object-dir" in moduleConfigData:
                self.objDir = moduleConfigData["object-dir"]
            if "mod-dir" in moduleConfigData:
                self.modDir = moduleConfigData["mod-dir"]            
            if "filter-profiles" in moduleConfigData:
                self.filterProfiles.update(moduleConfigData["filter-profiles"])    


class ScratchDirManager(object):
    """Manages a scratch directory used by pipeline and other processing."""
    def __init__(self, scratchDirPath):
        """Sets up the scratch directory based on a path. If the directory does not 
        exist it is created. If the directory exists, it is cleared; deleting all
        files in the directory.
        
        WARNING: Two processes using the same temp directory name at the same time will
                 result in undefined, but almost certainly bad, behavior.
        
        NOTE: The Python tempfile library doesn't create file names that can be passed
              to functions opening those files, only file-like objects. Also it doesn't 
              let us control the extension. This is easier to implement for our use case
              even if it isn't as robust as I would like."""
        self.ctr = 0;
        self.path = scratchDirPath
        self.create()
        
    def create(self):
        """Creates the scratch directory if it doesn't exist, otherwise it clears it."""
        # TODO: This is kind of a brute-force method. Might want to revisit it.
        self.remove()
        os.makedirs(self.path)
        self.ctr = 0;
        
    def remove(self):
        """Clears the scratch directory and removes it."""
        try:
            shutil.rmtree(self.path)
        except:
            pass
        
    def clear(self):
        """Clears the scratch directory."""
        # TODO: This is kind of a brute-force method. Might want to revisit it.
        self.create()
    
    def getTempFilePath(self, fileExtension):
        """Returns a file path using the file extension for use by as a temp file 
        in the scratch directory. Does not create the file. Does not guarantee no
        collisions if two processes are using the same scratch directory."""
        # HACK! Fix this!
        # TODO: Better way to get the file name with less chance of collision. 
        #       (Use random and check if already exists?)
        self.ctr = self.ctr + 1
        return os.path.join(self.path, "temp_" + str(self.ctr) + fileExtension)
        

def getFilterFunction(filterName):
    """Returns a tuple for the passed filter name containing filter extension 
    function, the filter function, and the filter doc string. Returns 'None' if  
    the filter could not be located and/or loaded.
    
    TODO: Support dynamic imports from a 'filters' directory."""
    
    # Is it a 'built-in' filter?
    if filterName == "shellexec":
        return (shellexec_filter_ext, shellexec_filter, shellexec_doc)
    elif filterName == "cleanbabylon":
        return (cleanbab_filter_ext, cleanbab_filter, cleanbab_doc)
    
    return None
    

def resourceOutPath(defaultConfig, resourceType, resourceFileName):
    logger.error("common.resourceOutPath() - Not implemented.")
    pass


def getRemoteResourceFile(defaultConfig, resourceType, url):
    logger.error("common.getRemoteResourceFile() - Not implemented.")
    pass


def getResourceFile(defaultConfig, resourceType, options):
    logger.error("common.getResourceFile() - Not implemented.")
    pass


    