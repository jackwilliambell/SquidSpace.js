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
from filterfile import filterFile, runFilter


testDir1 = "test/sqs_test/scratch1"
testDir2 = "test/sqs_test/scratch2"

copyFilterProfile = "testfilter"

testConfig = {
    "build-dir": "test/sqs_test/build",
    "filter-profiles": {
        copyFilterProfile: [
            {
                "filter": "shellexec",
                "options": {
                    "command-template": "cp {pathIn} {pathOut}"
                }
            }
        ]
    }
}

class TestFilterFile(unittest.TestCase):

    def test_filterFuncBasic(self):
        # Create the module processing configuration.
        modConfig = ModuleConfiguration(testConfig, {})
        
        # Create scratch dir and add file.
        sd = ScratchDirManager(testDir1)
        inFile = sd.getTempFilePath(".txt")
        outFile = sd.getTempFilePath(".txt")
        file = open(inFile, "w") 
        file.write("This is a temporary test text file.") 
        file.close()
        
        self.assertTrue(filterFile(inFile, outFile, sd, modConfig.getFilters(None, copyFilterProfile)))
        
        # Double check the files are the same.
        self.assertTrue(cmp(inFile, outFile), msg="The input and output files should be identical.")
        
        # Clean up dir.
        sd.remove()

    def test_runFilterBasic(self):
        # Create scratch dir and add file.
        sd1 = ScratchDirManager(testDir1)
        sd2 = ScratchDirManager(testDir2)
        inFile = sd1.makeTempFilePath("temp_testfile.txt")
        file = open(inFile, "w") 
        file.write("This is a temporary test text file.") 
        file.close()
        outFile = sd2.makeTempFilePath("temp_testfile.txt")
        
        runFilter(testConfig, copyFilterProfile, testDir2, inFile)
        
        # Double check the files are the same.
        self.assertTrue(cmp(inFile, outFile), msg="The input and output files should be identical.")
        
        # Clean up dirs.
        sd1.remove()
        sd2.remove()

    # TODO: More tests. Test 'command-arguments' option.
    # TODO: Make sure to clean up any scratch dirs that might be left out there if a test fails.

if __name__ == '__main__':
    unittest.main()

