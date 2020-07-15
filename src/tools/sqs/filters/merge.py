"""## filters.merge.py – SQS Filter Module that merges files

Merges multiple input files into a single output file.

Besides the standard filterFile() functions there is one API function:

1. mergeFiles(pathInList, pathOut, options, logger) – Merges files

### Filter File function

Options: 

* "out-name" [required, string] Specifies the file name to write the combined files to

* "file-separator" [optional, string] Specifies a string value to insert between each file

File Extensions: Any."""


copyright = """SquidSpace.js, the associated tooling, and the documentation are copyright 
Jack William Bell 2020 except where noted. All other content, including HTML files and 3D 
assets, are copyright their respective authors."""


import os
from common import forceFileExtension


def mergeFiles(pathInList, pathOut, options, logger):
    """Merges all files from the path in list to the path out. Returns the number
    of files successfully merged.
    
    Options: 

    * "file-separator" [optional, string] Specifies a string value to insert between each file
    """
    logger.debug("merge.mergeFiles() - Processing pathOut: {pathOut} options: %{options}.".format(pathOut=pathOut, options=options))
    
    # Setup
    chunkSize = 4096 # 4KB
    result = 0
    sep = None
    if "file-separator" in options:
        # We will be doing binary read/writes, so convert to a bytes object
        sep = bytes(options["file-separator"], 'utf-8')
    
    try:
        # Open output file
        outFile = open(pathOut, 'wb')

        # Process the input files.
        for pathIn in pathInList:
            
            try:
                # Open input file
                inFile = open(pathIn, 'rb')
            
                # Transfer data in chunks.
                chunk = inFile.read(chunkSize)
                while chunk:
                    outFile.write(chunk)
                    chunk = inFile.read(chunkSize)
            
                # Add separator?
                if sep:
                    outFile.write(sep)
                
                # Close the input file.
                inFile.close()
            
                # Increment the success count
                result = result + 1    
                        
            except:
                logger.exception("merge.mergeFiles() - Could not read input file '{0}', continuing processing.".format(pathIn))
        
        # Close the output file.
        outFile.close()
                
    except:
            logger.exception("merge.mergeFiles() - Could not open output file '{0}'.".format(pathOut))
        
    # Done!
    return result
    

def filterFiles(inputs, outputs, options, logger):
    """SQS filter files function that merges files."""
    
    logger.debug("merge.filterFiles().")
    
    # Setup
    result = 0
    outName = None
    if "out-name" in options:
        outName = options["out-name"]
        
    if not outName:
        logger.error("merge.filterFiles() - No or invalid 'out-name' option supplied.")
    else:
         result = mergeFiles(inputs, outputs(os.path.basename(outName)), options, logger)
    
    # Done.
    return result
    