import sys
from os import path
# NOTE: I needed to fix the sys.path to point up and over to sqs directory for imports. 
#       This is a huge hack that works under certain particular circumstances and will 
#       probably need modifying in the future.
#sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
#sys.path.append(  path.abspath("../sqs/") )
sys.path.append(  path.abspath("tools/sqs/") )
#import pprint;pprint.pprint(sys.path)

import unittest
from common import ScratchDirManager, forceFileExtension, makeOutputFilesFuncForDir
from sqslogger import logger
from filterhelpers import getFilterModule

filterOptions = {
    "out-name": "testmerged.txt",
    "file-separator": "\n\n"
}

fileData1 = "This is temporary test text file 1."
fileData2 = "This is temporary test text file 2."
fileData3 = "This is temporary test text file 3."
fileData4 = "This is temporary test text file 4."

combinedData = fileData1 + "\n\n" + fileData2 + "\n\n" + fileData3 + "\n\n" + fileData4 + "\n\n"

def makeTestFile(sd, fileData):
    fp = sd.makeTempFilePathForExt(".txt")
    file = open(fp, "w") 
    file.write(fileData) 
    file.close()
    return fp

class TestFilterShellExec(unittest.TestCase):

    def test_mergefilter(self):
        # Get filter function
        filterMod = getFilterModule("merge")
        
        self.assertIsNotNone(filterMod)
        self.assertIsNotNone(filterMod[0])
        self.assertIsNotNone(filterMod[1])
        
        filterFunc = filterMod[0]
        
        # Create scratch dir and add files.
        sd = ScratchDirManager("tools/tools/sqs_test/scr/scratch")
        outputs = sd.makeOutputFilesFunc()
        fp1 = makeTestFile(sd, fileData1)
        fp2 = makeTestFile(sd, fileData2)
        fp3 = makeTestFile(sd, fileData3)
        fp4 = makeTestFile(sd, fileData4)
        
        # Execute the filter. It should return '4' to indicate four files were processed.
        self.assertEqual(filterFunc([fp1, fp2, fp3, fp4], outputs, filterOptions, logger), 4)
        
        # Double check the merged file has the expected content.
        mergeFile = open(sd.makeFilePath("testmerged.txt"), 'r')
        fileData = mergeFile.read()
        mergeFile.close()
        self.assertEqual(fileData, combinedData)
        
        # Clean up scratch dir.
        sd.remove()

    # TODO: More tests. 

if __name__ == '__main__':
    unittest.main()

