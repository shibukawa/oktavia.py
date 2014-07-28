import unittest
from oktavia.oktavia import Oktavia
import metadata

class SplitterTest(unittest.TestCase):

    def setUp(self):
        self.oktavia = Oktavia()
        self.splitter = self.oktavia.addSplitter('document')
        self.oktavia.addWord("abracadabra")
        self.splitter.split()
        self.oktavia.addWord("mississippi")
        self.splitter.split()
        self.oktavia.addWord("abracadabra mississippi")
        self.splitter.split()
        self.oktavia.build(5)

    def test_count(self):
        self.assertEqual(3, self.splitter.size())

    def test_get_splitter_index(self):
        self.assertEqual(0, self.splitter.getIndex(0))
        self.assertEqual(0, self.splitter.getIndex(10))
        self.assertEqual(1, self.splitter.getIndex(11))
        self.assertEqual(1, self.splitter.getIndex(21))
        self.assertEqual(2, self.splitter.getIndex(22))
        self.assertEqual(2, self.splitter.getIndex(44))

    def test_get_splitter_index_boundary(self):
        try:
            self.splitter.getIndex(-1)
            self.fail("fm.getIndex()")
        except:
            pass
        try:
            self.splitter.getIndex(45)
            self.fail("fm.getIndex()")
        except:
            pass

    def test_get_splitter_content(self):
        self.assertEqual("abracadabra mississippi", self.splitter.getContent(2))
        self.assertEqual("mississippi", self.splitter.getContent(1))
        self.assertEqual("abracadabra", self.splitter.getContent(0))

    def test_get_splitter_content_boundary(self):
        try:
            self.splitter.getContent(3)
            self.fail("fm.getContent()")
        except:
            pass
        try:
            self.splitter.getContent(-1)
            self.fail("fm.getContent()")
        except:
            pass

    def test_load_dump_and_count(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.splitter = self.oktavia.getSplitter('document')

        self.expect(self.splitter.size()).toBe(3)

    def test_load_dump_and_get_splitter_index(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.splitter = self.oktavia.getSplitter('document')

        self.assertEqual(0, self.splitter.getIndex(0))
        self.assertEqual(0, self.splitter.getIndex(10))
        self.assertEqual(1, self.splitter.getIndex(11))
        self.assertEqual(1, self.splitter.getIndex(21))
        self.assertEqual(2, self.splitter.getIndex(22))
        self.assertEqual(2, self.splitter.getIndex(44))

    def test_load_dump_and_get_splitter_index_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.splitter = self.oktavia.getSplitter('document')

        try:
            self.splitter.getIndex(-1)
            self.fail("fm.getIndex()")
        except:
            pass
        try:
            self.splitter.getIndex(45)
            self.fail("fm.getIndex()")
        except:
            pass

    def test_load_dump_and_get_splitter_content(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.splitter = self.oktavia.getSplitter('document')

        self.assertEqual("abracadabra mississippi", self.splitter.getContent(2))
        self.assertEqual("mississippi", self.splitter.getContent(1))
        self.assertEqual("abracadabra", self.splitter.getContent(0))

    def test_load_dump_and_get_splitter_content_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.splitter = self.oktavia.getSplitter('document')

        try:
            self.splitter.getContent(3)
            self.fail("fm.getContent()")
        except:
            pass
        try:
            self.splitter.getContent(-1)
            self.fail("fm.getContent()")
        except:
            pass
