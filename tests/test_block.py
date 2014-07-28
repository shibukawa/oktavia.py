import unittest
from oktavia.oktavia import Oktavia
import metadata

class BlockTest(unittest.TestCase):

    def setUp(self):
        self.oktavia = new Oktavia()
        self.block = self.oktavia.addBlock('document')
        self.oktavia.addWord("abracadabra")
        self.block.startBlock("river")
        self.oktavia.addWord("mississippi")
        self.block.endBlock()
        self.oktavia.addWord("abracadabra mississippi")
        self.oktavia.build()

    def test_doc_sizes(self):
        self.assertEqual(1, self.block.size())

    def test_in_block(self):
        self.assertFalse(self.block.inBlock(0))
        self.assertFalse(self.block.inBlock(10))
        self.assertTrue(self.block.inBlock(11))
        self.assertTrue(self.block.inBlock(21))
        self.assertFalse(self.block.inBlock(22))
        self.assertFalse(self.block.inBlock(44))

    def test_in_block_boundary(self):
        try:
            self.block.inBlock(-1)
            self.fail("fm.inBlock() 1")
        except e:
            pass
        try:
            self.block.inBlock(45)
            self.fail("fm.inBlock() 2")
        except e:
            pass

    def test_get_block_content(self):
        self.assertEqual("mississippi", self.block.getBlockContent(11))

    def test_get_block_content_boundary(self):
        try:
            self.block.getBlockContent(45)
            self.fail("fm.getContent()")
        except e:
            pass
        try:
            self.block.getBlockContent(-1)
            self.fail("fm.getContent()")
        except e:
            pass

    def test_get_block_name(self):
        self.expect(self.block.getBlockName(11)).toBe("river")

    def test_get_block_name_boundary(self):
        try:
            self.block.getBlockName(45)
            self.fail("fm.getName()")
        except e:
            pass
        try: 
            self.block.getBlockName(-1)
            self.fail("fm.getName()")
        except e:
            pass

    def test_dump_load_and_doc_sizes(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.block = self.oktavia.getBlock('document')

        self.assertEqual(1, self.block.size())

    def test_load_dump_and_in_block(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.block = self.oktavia.getBlock('document')

        self.assertFalse(self.block.inBlock(0))
        self.assertFalse(self.block.inBlock(10))
        self.assertTrue(self.block.inBlock(11))
        self.assertTrue(self.block.inBlock(21))
        self.assertFalse(self.block.inBlock(22))
        self.assertFalse(self.block.inBlock(44))

    def test_load_dump_and_in_block_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.block = self.oktavia.getBlock('document')

        try:
            self.block.inBlock(-1)
            self.fail("fm.inBlock() 1")
        except e:
            pass
        try:
            self.block.inBlock(45)
            self.fail("fm.inBlock() 2")
        except e:
            pass

    def test_load_dump_and_get_block_content(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.block = self.oktavia.getBlock('document')

        self.assertEqual("mississippi", self.block.getBlockContent(11))

    def test_load_dump_and_get_block_content_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.block = self.oktavia.getBlock('document')

        try:
            self.block.getBlockContent(45)
            self.fail("fm.getContent()")
        except e:
            pass
        try:
            self.block.getBlockContent(-1)
            self.fail("fm.getContent()")
        except e:
            pass

    def test_load_dump_and_get_block_name(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.block = self.oktavia.getBlock('document')

        self.assertEqual("river", self.block.getBlockName(11))

    def test_load_dump_and_get_block_name_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.block = self.oktavia.getBlock('document')

        try:
            self.block.getBlockName(45)
            self.fail("fm.getName()")
        except e:
            pass
        try:
            self.block.getBlockName(-1)
            self.fail("fm.getName()")
        except e:
            pass
