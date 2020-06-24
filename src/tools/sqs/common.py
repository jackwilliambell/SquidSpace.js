"""## SQS Common API 

Shared code used by all SQS tools and APIs.
"""

from enum import Enum
import os 
import shutil
import urllib.request
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
        if isinstance(defaultConfigData, dict):
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
        if isinstance(moduleConfigData, dict):
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
    
    def getResourcePath(self, resourceFlavor):
        """Returns a resource path based on the resource flavor or None."""
        if resourceFlavor == ResourceFlavor.TEXTURE and len(self.texDir) > 0:
            return self.texDir
        elif resourceFlavor == ResourceFlavor.MATERIAL and len(self.matDir) > 0:
            return self.matDir
        elif resourceFlavor == ResourceFlavor.OBJECT and len(self.objDir) > 0:
            return self.objDir
        elif resourceFlavor == ResourceFlavor.MOD and len(self.modDir) > 0:
            return self.modDir
        
        return None
    
    def makeResourceFilePath(self, resourceFlavor, resourceFileName):
        """Returns a file path based on the resource flavor and the passed file name or 
        None."""
        resourcePath = self.getResourcePath(resourceFlavor)
        
        if resourcePath is not None and resourceFileName is not None and len(resourceFileName) > 0:
            return os.path.join(resourcePath, resourceFileName)
        
        return None
    
    def getFilters(self, filters, filterProfile):
        """If the filters argument is not 'None', the argument is returned. Otherwise 
        an attempt is made to return named filters for the filter profile argument. If no 
        valid filters could be located, 'None' is returned."""
        
        if filters != None and filterProfile == None:
            return filters
        if filterProfile != None:
            return self.filterProfiles.get(filterProfile)
        # We've got nothing.
        return None
    
    def getScratchDirManager(self):
        return ScratchDirManager(os.path.join(self.bldDir, "scratch/"))


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
    
    def makeTempFilePath(self, fileName):
        """Returns a file path using the file name for use by as a temp file 
        in the scratch directory. Does not create the file. Does not guarantee no
        collisions if two processes are using the same scratch directory."""
        return os.path.join(self.path, "temp_" + fileName)
    
    def getTempFilePath(self, fileExtension):
        """Returns a file path using the file extension for use by as a temp file 
        in the scratch directory. Does not create the file. Does not guarantee no
        collisions if two processes are using the same scratch directory."""
        # HACK! Fix this!
        # TODO: Better way to get the file name with less chance of collision. 
        #       (Use random and check if already exists?)
        self.ctr = self.ctr + 1
        return os.path.join(self.path, "temp_" + str(self.ctr) + fileExtension)
        

def getFilterModule(filterName):
    """Returns a tuple for the passed filter name containing filter extension 
    function, the filter function, and the filter doc string. Returns 'None' if  
    the filter could not be located and/or loaded.
    
    TODO: Support dynamic imports from a 'filters' directory."""
    
    # Is it a 'built-in' filter?
    if filterName == "shellexec":
        return (shellexec_filter_ext, shellexec_filter, shellexec_doc)
    elif filterName == "cleanbabylon":
        return (cleanbab_filter_ext, cleanbab_filter, cleanbab_doc)
    
    return (None, None, None)
    

def getSourceURL(urlSource): 
    """Opens and returns a file-like object from the fully qualified url contained 
    in the url source or None if no url source was specified or the file url not be 
    opened."""
    if urlSource != None and len(urlSource) > 0:
        try:
            sf = urllib.request.urlopen(urlSource)
            return sf
        except:
            logger.exception("common.getSourceURL() - Could not open URL '{0}'.".format(urlSource))

    # Failed!
    return None
    
    
def getSourceFile(fileSource):
    """Opens and returns the file with the path contained in the file source or 
    None if no file source was specified or the file could not be opened.
    
    NOTE: File is opened in 'rb' (read/binary) mode."""
    if fileSource: # PYTHON TIP: both None and an empty string evaluates to 'False'
        try:
            sf = open(fileSource, 'rb')
            return sf
        except:
            logger.exception("common.getSourceFile() - Could not open file '{0}'.".format(fileSource))

    # Failed!
    return None
    
    
def getDestFile(fileDest):
    """Opens and returns the file with the path contained in the file destination or 
    None if no file destination was specified or the file could not be opened.
    
    NOTE: File is opened in 'wb' (write/binary) mode."""
    if fileDest: # PYTHON TIP: both None and an empty string evaluates to 'False'
        try:
            sf = open(fileDest, 'wb')
            return sf
        except:
            logger.exception("common.getDestFile() - Could not open file '{0}'.".format(fileDest))

    # Failed!
    return None
    

def copySourceToDestAndClose(sourceFile, destFile):
    """Writes the contents of a source file-like object to a destination file-like object and then
    attempts to close both if they support a close() method. Returns True on success, otherwise 
    returns False.
    
    NOTE: Requires minimal memory because it doesn't read and write all of the source at one time.
    
    NOTE: Assumes both files were opened with the same text or binary mode. May still work otherwise."""
    # Assume failure.
    result = False
    
    try:
        # Prime the pump
        chunk = sourceFile.read(4096) # Read 4kb at a time.
        
        # Write the data.
        while chunk: # PYTHON TIP: an empty string or binary object evaluates to 'False'
            destFile.write(chunk)
            chunk = sourceFile.read(4096) # Get next 4kb.
            
        # We are good!
        result = True
    except:
        logger.exception("common.copySourceToDest() - Copy failed with exception.")
    finally:
        # Close the files.
        try: 
            sourceFile.close()
        except:
            pass
        try: 
            destFile.close()
        except:
            pass
            
    # Done!
    return result


def lookAheadIterator(iterable):
    """For each value in an iterable object, yield the value plus a 
    boolean indicating if this is the last item in the iterator or not."""
    # Get an iterator and grab the first value.
    it = iter(iterable)
    last = next(it)
    
    # Iterate, yielding the value and False.
    for val in it:
        yield last, False
        last = val
        
    # Yield the last value and True.
    yield last, True

    