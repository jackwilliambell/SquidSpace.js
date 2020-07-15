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
from common import ScratchDirManager, forceFileExtension, makeOutputFilesFuncForDir
from sqslogger import logger
from filterhelpers import getFilterModule

copyFilterOptions = {
    "in-ext": "txt",
    "out-ext": "md",
    "command-template": "cp {pathIn} {pathOut}"
}

class TestFilterShellExec(unittest.TestCase):

    def test_copyfilter(self):
        # Get filter function
        filterMod = getFilterModule("shellexec")
        
        self.assertIsNotNone(filterMod)
        self.assertIsNotNone(filterMod[0])
        self.assertIsNotNone(filterMod[1])
        
        filterFunc = filterMod[0]
        
        # Create scratch dir and add file.
        sd = ScratchDirManager("tools/sqs_test/scr/scratch")
        fp1 = sd.makeTempFilePathForExt(".txt")
        fp2 = forceFileExtension(fp1, ".md")
        outputs = sd.makeOutputFilesFunc()
        file = open(fp1, "w") 
        file.write("This is a temporary test text file.") 
        file.close()
        
        # Execute the filter. It should return '1' to indicate one file was processed.
        self.assertEqual(filterFunc([fp1], outputs, copyFilterOptions, logger), 1)
        
        # Double check the files are the same.
        self.assertTrue(cmp(fp1, fp2))
        
        # Clean up scratch dir.
        sd.remove()

    def test_copyfilterNoFile(self):
        # Get filter function
        filterMod = getFilterModule("shellexec")
        
        self.assertIsNotNone(filterMod)
        self.assertIsNotNone(filterMod[0])
        self.assertIsNotNone(filterMod[1])
        
        filterFunc = filterMod[0]
        
        # Apply filter to non-existent files.
        fp1 = "tools/sqs_test/scratch/test.text"
        outputs = makeOutputFilesFuncForDir("tools/sqs_test/scr/scratch")
        self.assertEqual(filterFunc([fp1], outputs, copyFilterOptions, logger), 0)

    # TODO: More tests. Test 'command-arguments' option.

if __name__ == '__main__':
    unittest.main()

