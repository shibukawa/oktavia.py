import unittest
from oktavia.bwt import bwt
from oktavia.bwt import BWT

class BWTTest(unittest.TestCase):
    def test_get(self):
        bwt = BWT('abracadabra')
        self.assertEqual("ard$rcaaaabb", bwt.get(replace="$"))
        self.assertEqual(len('abracadabra') + 1, bwt.size())
        self.assertEqual(3, bwt.head())

    def test_shortcut_method(self):
        result = bwt('abracadabra', '$')
        self.assertEqual("ard$rcaaaabb", result)
