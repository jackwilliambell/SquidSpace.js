import sys
from os import path
# NOTE: I needed to fix the sys.path to point up and over to sqs directory for imports. 
#       This is a huge hack that works under certain particular circumstances and will 
#       probably need modifying in the future.
#sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
#sys.path.append(  path.abspath("../sqs/") )
sys.path.append(  path.abspath("tools/sqs/") )
#import pprint;pprint.pprint(sys.path)

import os
import unittest
from filecmp import cmp
from common import ScratchDirManager, ModuleConfiguration
from filtercommand import processFilterChain, runFilter
from sqslogger import logger


testDir1 = "tools/sqs_test/scr/inDir"
testDir2 = "tools/sqs_test/scr/outDir"

copyFilterProfile = "testfilter1"
copyMergeFilterProfile = "testfilter2"

testConfig = {
    "build-dir": "tools/sqs_test/scr",
    "filter-profiles": {
        copyFilterProfile: [
            {
                "filter": "shellexec",
                "options": {
                    "command-template": "cp {pathIn} {pathOut}"
                }
            }
        ],
        copyMergeFilterProfile: [
            {
                "filter": "merge",
                "options": {
                    "out-name": "testmerged.txt",
                    "file-separator": "\n\n"
                }
            },
            {
                "filter": "shellexec",
                "options": {
                    "in-ext": "txt",
                    "out-ext": "md",
                    "command-template": "cp {pathIn} {pathOut}"
                }
            }
        ]
    }
}

fileData1 = "This is temporary test text file 1."
fileData2 = "This is temporary test text file 2."
fileData3 = "This is temporary test text file 3."
fileData4 = "This is temporary test text file 4."

combinedData = fileData1 + "\n\n" + fileData2 + "\n\n" + fileData3 + "\n\n" + fileData4 + "\n\n"

def makeTestFile(fp, fileData):
    file = open(fp, "w") 
    file.write(fileData) 
    file.close()
    return fp
    
class TestFilterCommand(unittest.TestCase):

    def test_filterChainBasic(self):
        # Create the module processing configuration.
        modConfig = ModuleConfiguration(testConfig, {})
        
        # Create scratch dir and add file.
        sd1 = ScratchDirManager(testDir1)
        sd2 = ScratchDirManager(testDir2)
        inFile = sd1.makeFilePath("temp_testfile.txt")
        makeTestFile(inFile, fileData1)
        outFile = sd2.makeFilePath("temp_testfile.txt")
        
        self.assertTrue(processFilterChain([inFile], testDir2, sd1, modConfig.getFilters(None, copyFilterProfile)))
        
        # Double check the files are the same.
        self.assertTrue(cmp(inFile, outFile), msg="The input and output files should be identical.")
        
        # Clean up dirs.
        sd1.remove()
        sd2.remove()

    def test_runFilterBasic(self):
        # Create scratch dir and add files.
        sd1 = ScratchDirManager(testDir1)
        sd2 = ScratchDirManager(testDir2)
        fp1 = sd1.makeFilePath("test1.txt")
        fp2 = sd1.makeFilePath("test2.txt")
        fp3 = sd1.makeFilePath("test3.txt")
        fp4 = sd1.makeFilePath("test4.txt")
        makeTestFile(fp1, fileData1)
        makeTestFile(fp2, fileData2)
        makeTestFile(fp3, fileData3)
        makeTestFile(fp4, fileData4)
        
        runFilter(testConfig, copyMergeFilterProfile, [fp1, fp2, fp3, fp4], testDir2)
        
        # Double check the merged file has the expected content.
        mergeFile = open(sd2.makeFilePath("testmerged.md"), 'r')
        fileData = mergeFile.read()
        mergeFile.close()
        self.assertEqual(fileData, combinedData)
        
        # Clean up dirs.
        sd1.remove()
        sd2.remove()

    # TODO: More tests.
    # TODO: Make sure to clean up any scratch dirs that might be left out there if a test fails.

if __name__ == '__main__':
    unittest.main()

