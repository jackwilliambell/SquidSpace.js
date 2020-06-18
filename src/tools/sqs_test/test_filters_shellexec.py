import unittest
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from sqs.filters.shellexec import filter

copyFilterOptions = {
    "command-template": "cp {pathIn} {pathOut}"
}

class TestFilterShellExec(unittest.TestCase):

    def test_copyfilter(self):
        # TODO: Create scratch dir and add file.
        self.assertTrue(filter("sqs_test/scratch/test.md", "sqs_test/scratch/test1.md", copyFilterOptions))
        # TODO: Double check the files are the same.
        # TODO: Clean up dir.

    def test_copyfilterNoDir(self):
        self.assertFalse(filter("sqs_test/scratch/test.md", "sqs_test/scratch/test1.md", copyFilterOptions))

    # TODO: More tests. Test 'command-arguments' option.

if __name__ == '__main__':
    unittest.main()

