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
from common import ScratchDirManager, getFilterFunction

copyFilterOptions = {
    "command-template": "cp {pathIn} {pathOut}"
}

class TestFilterShellExec(unittest.TestCase):

    def test_copyfilter(self):
        # Get filter function
        filterMod = getFilterFunction("shellexec")
        
        self.assertIsNotNone(filterMod)
        self.assertIsNotNone(filterMod[0])
        self.assertIsNotNone(filterMod[1])
        self.assertIsNotNone(filterMod[2])
        
        filterFunc = filterMod[1]
        
        # Create scratch dir and add file.
        sd = ScratchDirManager("sqs_test/scratch")
        fp1 = sd.getTempFilePath(".txt")
        fp2 = sd.getTempFilePath(".txt")
        file = open(fp1, "w") 
        file.write("This is a temporary test text file.") 
        file.close()
        
        # Execute the filter.
        self.assertTrue(filterFunc(fp1, fp2, copyFilterOptions))
        
        # Double check the files are the same.
        self.assertTrue(cmp(fp1, fp2))
        
        # Clean up scratch dir.
        sd.remove()

    def test_copyfilterNoFile(self):
        # Get filter function
        filterMod = getFilterFunction("shellexec")
        
        self.assertIsNotNone(filterMod)
        self.assertIsNotNone(filterMod[0])
        self.assertIsNotNone(filterMod[1])
        self.assertIsNotNone(filterMod[2])
        
        filterFunc = filterMod[1]
        
        # Apply filter to non-existent files.
        self.assertFalse(filterFunc("sqs_test/scratch/test.md", "sqs_test/scratch/test1.md", copyFilterOptions))

    # TODO: More tests. Test 'command-arguments' option.

if __name__ == '__main__':
    unittest.main()

