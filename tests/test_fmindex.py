import unittest
from oktavia.fmindex import FMIndex
from oktavia.binaryio import BinaryInput
from oktavia.binaryio import BinaryOutput

class FMIndexTest(unittest.TestCase):

    def setUp(self):
        self.str = ""
        self.sd = []
        self.rd = {}
        self.pd = []
        self.didd = []
        self.docd = []
        self.fm = FMIndex()

        self.docd.append("abracadabra")
        self.docd.append("mississippi")
        self.docd.append("abracadabra mississippi")

        did = 0
        for did, doc in enumerate(self.docd):
            self.str += doc
            for j in range(len(doc)):
                self.didd.append(did)
            self.fm.append(doc)

        self.didd.append(len(self.docd))
        #import cProfile
        #cProfile.runctx('self.fm.build(3)', globals(), locals())
        self.fm.build(3)
        self.str += chr(0) # end_marker
        for i in range(len(self.str)):
            for j in range(1, len(self.str) - i + 1):
                s = self.str[i:i + j]
                count = self.rd.get(s, 0)
                self.rd[s] = count + 1
        v = []
        for i in range(len(self.str)):
            s = self.str[i:] + self.str[0:i]
            v.append([s, i])
        v.sort()
        for rotatedstr, index in v:
            self.pd.append(index)
        for i in range(len(self.str)):
            self.sd.append(self.str[i:].replace(chr(0), ''))

    def test_size(self):
        self.assertEqual(len(self.str), self.fm.size())

    def test_get_rows(self):
        for i in range(self.fm.size()):
            for j in range(i + 1, self.fm.size()): 
                s = self.str[i:j]
                actual = self.fm.get_rows(s)
                expect = self.rd[s]
                self.assertEqual(expect, actual)

    def test_get_position(self):
        for i in range(len(self.pd)):
            self.assertEqual(self.pd[i], self.fm.get_position(i))

    def test_get_substring(self):
        for i, expect in enumerate(self.sd):
            actual = self.fm.get_substring(i, self.fm.size())
            self.assertEqual(expect, actual)

    def test_get_substring2(self):
        self.fm = FMIndex()
        self.fm.append("abracadabra")
        self.fm.append("mississippi")
        self.fm.append("abracadabra mississippi")
        self.fm.build(3)
        self.assertEqual('abracadabra', self.fm.get_substring(0, 11))
        self.assertEqual('mississippi', self.fm.get_substring(11, 11))
        self.assertEqual('abracadabra mississippi', self.fm.get_substring(22, 23))

    def test_get_position_boundary(self):
        try:
            self.fm.get_position(self.fm.size())
        except:
            pass
        else:
            self.fail("fm.get_position()")

    def test_get_substring_boundary(self):
        try:
            self.fm.get_substring(self.fm.size(), 0)
        except:
            pass
        else:
            self.fail("fm.get_substring()")

    def test_search(self):
        results = self.fm.search("ssi")
        self.assertEqual(4, len(results))
        for result in results:
            self.assertEqual('ssi', self.fm.get_substring(result, 3))

    def test_dump_load_and_size(self):
        dump = BinaryOutput()
        self.fm.dump(dump)
        self.fm.load(BinaryInput(dump.result()))

        self.assertEqual(len(self.str), self.fm.size())

    def test_dump_load_and_get_rows(self):
        dump = BinaryOutput()
        self.fm.dump(dump)
        self.fm.load(BinaryInput(dump.result()))

        for i in range(self.fm.size()):
            for j in range(i + 1, self.fm.size()): 
                s = self.str[i:j]
                self.assertEqual(self.rd[s], self.fm.get_rows(s))

    def test_dump_load_and_get_position(self):
        dump = BinaryOutput()
        self.fm.dump(dump)
        self.fm.load(BinaryInput(dump.result()))

        for i in range(len(self.pd)):
            self.assertEqual(self.pd[i], self.fm.get_position(i))

    def test_dump_load_and_get_substring(self):
        dump = BinaryOutput()
        self.fm.dump(dump)
        self.fm.load(BinaryInput(dump.result()))

        for i, expect in enumerate(self.sd):
            actual = self.fm.get_substring(i, self.fm.size())
            self.assertEqual(expect, actual)

    def test_dump_load_and_get_position_boundary(self):
        dump = BinaryOutput()
        self.fm.dump(dump)
        self.fm.load(BinaryInput(dump.result()))

        try:
            self.fm.get_position(self.fm.size())
        except:
            pass
        else:
            self.fail("fm.get_position()")

    def test_dump_load_and_get_substring_boundary(self):
        dump = BinaryOutput()
        self.fm.dump(dump)
        self.fm.load(BinaryInput(dump.result()))

        try:
            self.fm.get_substring(self.fm.size(), 0)
        except:
            pass
        else:
            self.fail("fm.get_substring()")
