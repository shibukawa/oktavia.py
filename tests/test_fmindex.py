import struct
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

        for did, doc in enumerate(self.docd):
            self.str += doc
            for j in range(len(doc)):
                self.didd.append(did)
            self.fm.append(doc)

        self.didd.append(len(self.docd))
        #import cProfile
        #cProfile.runctx('self.fm.build(3)', globals(), locals())
        self.fm.build(25, 256)
        self.str += chr(0) # end_marker
        for i in range(len(self.str)):
            for j in range(1, len(self.str) - i + 1):
                s = self.str[i:i + j]
                self.rd[s] = self.rd.get(s, 0) + 1
        v = []
        for i in range(len(self.str)):
            s = self.str[i:] + self.str[0:i]
            v.append((s, i))
        v.sort()
        for rotatedstr, index in v:
            self.pd.append(index)
        for i in range(len(self.str)):
            self.sd.append(self.str[i:].replace(chr(0), ''))

    def test_size(self):
        print("test_size")
        self.assertEqual(len(self.str), self.fm.size())

    def test_get_rows(self):
        print("test_get_rows")
        for i in range(self.fm.size()):
            for j in range(i + 1, self.fm.size()): 
                s = self.str[i:j]
                actual = self.fm.get_rows(s)
                expect = self.rd[s]
                self.assertEqual(expect, actual)

    def test_get_position(self):
        print("test_get_position")
        for i, expect in enumerate(self.pd):
            self.assertEqual(expect, self.fm.get_position(i))

    def test_get_substring(self):
        print("test_get_substring")
        for i, expect in enumerate(self.sd):
            actual = self.fm.get_substring(i, self.fm.size())
            self.assertEqual(expect, actual)

    def test_get_substring2(self):
        print("test_get_substring2")
        self.fm = FMIndex()
        self.fm.append("abracadabra")
        self.fm.append("mississippi")
        self.fm.append("abracadabra mississippi")
        self.fm.build(3, 256)
        self.assertEqual('abracadabra', self.fm.get_substring(0, 11))
        self.assertEqual('mississippi', self.fm.get_substring(11, 11))
        self.assertEqual('abracadabra mississippi', self.fm.get_substring(22, 23))

    def test_get_substring_with_compressed_word(self):
        print("test_get_substring_with_compressed_word")
        codes = ['\x00', '\x01', '\x03', 'a', 'b', 'r', 'c', 'd', 'm', 'i', 's', 'p', ' ']
        def encode(string):
            return [codes.index(c) for c in string]

        def decode(rawcodes):
            return "".join((codes[rawcode] for rawcode in rawcodes))

        self.fm = FMIndex(rawmode=True)
        print type(encode("abracadabra"))
        self.fm.append(encode("abracadabra"))
        self.fm.append([1])
        self.fm.append(encode("mississippi"))
        self.fm.append([1])
        self.fm.append(encode("abracadabra mississippi"))
        self.fm.append([1])
        self.fm.build(3, 256)
        self.assertEqual('abracadabra', decode(self.fm.get_substring(0, 11)))
        self.assertEqual('mississippi', decode(self.fm.get_substring(12, 11)))
        self.assertEqual('abracadabra mississippi', decode(self.fm.get_substring(24, 23)))

    def test_get_substring_before_build(self):
        print("test_get_substring_before_build")
        self.fm = FMIndex()
        self.fm.append("abracadabra")
        self.fm.append('\x01')
        self.fm.append("mississippi")
        self.fm.append('\x01')
        self.fm.append("abracadabra mississippi")
        self.fm.append('\x01')
        self.assertEqual('abracadabra', self.fm.get_substring(0, 11))
        self.assertEqual('mississippi', self.fm.get_substring(12, 11))
        self.assertEqual('abracadabra mississippi', self.fm.get_substring(24, 23))

    def test_get_position_boundary(self):
        print("test_get_position_boundary")
        try:
            self.fm.get_position(self.fm.size())
        except:
            pass
        else:
            self.fail("fm.get_position()")

    def test_get_substring_boundary(self):
        print("test_get_substring_boundary")
        try:
            self.fm.get_substring(self.fm.size(), 0)
        except:
            pass
        else:
            self.fail("fm.get_substring()")

    def test_search(self):
        print("test_search")
        results = self.fm.search("ssi")
        self.assertEqual(4, len(results))
        for result in results:
            self.assertEqual('ssi', self.fm.get_substring(result, 3))

    def test_dump_load_and_size(self):
        print("test_dump_load_and_size")
        dump = BinaryOutput()
        self.fm.dump(dump)
        self.fm.load(BinaryInput(dump.result()))

        self.assertEqual(len(self.str), self.fm.size())

    def test_dump_load_and_get_rows(self):
        print("test_dump_load_and_get_rows")
        dump = BinaryOutput()
        self.fm.dump(dump)
        fm = FMIndex()
        fm.load(BinaryInput(dump.result()))

        for i in range(fm.size()):
            for j in range(i + 1, fm.size()): 
                s = self.str[i:j]
                self.assertEqual(self.rd[s], fm.get_rows(s))

    '''def test_dump_load_and_get_position(self):
        print("test_dump_load_and_get_position")
        dump = BinaryOutput()
        print("@1")
        self.fm.dump(dump)
        print("@2")
        fm = FMIndex()
        fm.load(BinaryInput(dump.result()))

        for i, expect in enumerate(self.pd):
            print(i)
            self.assertEqual(expect, fm.get_position(i))
        print("@4")'''

    def test_dump_load_and_get_substring(self):
        print("test_dump_load_and_get_substring")
        dump = BinaryOutput()
        self.fm.dump(dump)
        fm = FMIndex()
        fm.load(BinaryInput(dump.result()))

        for i, expect in enumerate(self.sd):
            actual = fm.get_substring(i, fm.size())
            self.assertEqual(expect, actual)

    def test_dump_load_and_get_position_boundary(self):
        print("test_dump_load_and_get_position_boundary")
        dump = BinaryOutput()
        self.fm.dump(dump)
        fm = FMIndex()
        fm.load(BinaryInput(dump.result()))

        try:
            fm.get_position(fm.size())
        except:
            pass
        else:
            self.fail("fm.get_position()")

    def test_dump_load_and_get_substring_boundary(self):
        print("test_dump_load_and_get_substring_boundary")
        dump = BinaryOutput()
        self.fm.dump(dump)
        fm = FMIndex()
        fm.load(BinaryInput(dump.result()))

        try:
            fm.get_substring(fm.size(), 0)
        except:
            pass
        else:
            self.fail("fm.get_substring()")
