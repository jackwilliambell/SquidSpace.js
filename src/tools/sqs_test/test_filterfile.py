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
from filecmp import cmp
from common import ScratchDirManager
from filterfile import filterFile


testDir = "sqs_test/scratch"

copyFilterOptions = {
    "command-template": "cp {pathIn} {pathOut}"
}

copyConfig = {}

class TestFilterFile(unittest.TestCase):

    def test_copyfilter(self):
        # Create scratch dir and add file.
        sd = ScratchDirManager(testDir)
        inFile = sd.getTempFilePath(".txt")
        outFile = sd.getTempFilePath(".txt")
        file = open(fp1, "w") 
        file.write("This is a temporary test text file.") 
        file.close()
        
        filterFile(copyConfig, pathIn, pathOut, filterProfile)
        
        # Double check the files are the same.
        self.assertTrue(cmp(fp1, fp2), msg="The input and output files should be identical.")
        
        # Clean up dir.
        sd.remove()

    # TODO: More tests. Test 'command-arguments' option.

if __name__ == '__main__':
    unittest.main()

