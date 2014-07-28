import unittest
from oktavia.oktavia import Oktavia
import metadata

class SectionTest(unittest.TestCase):

    def setUp(self):
        self.oktavia = Oktavia()
        self.section = self.oktavia.addSection('document')
        self.oktavia.addWord("abracadabra")
        self.section.setTail("doc1")
        self.oktavia.addEndOfBlock()
        self.oktavia.addWord("mississippi")
        self.section.setTail("doc2")
        self.oktavia.addEndOfBlock()
        self.oktavia.addWord("abracadabra2 mississippi2")
        self.section.setTail("doc3")
        self.oktavia.addEndOfBlock()
        self.oktavia.build(25)

    def test_doc_sizes(self):
        self.assertEqual(3, self.section.size())

    def test_get_section_index(self):
        self.assertEqual(0, self.section.getSectionIndex(0))
        self.assertEqual(0, self.section.getSectionIndex(10))
        self.assertEqual(1, self.section.getSectionIndex(12))
        self.assertEqual(1, self.section.getSectionIndex(22))
        self.assertEqual(2, self.section.getSectionIndex(24))
        self.assertEqual(2, self.section.getSectionIndex(48))

    def test_get_section_index_boundary(self):
        try:
            self.section.getSectionIndex(-1)
            self.fail("fm.getSectionIndex(): -1")
        except:
            pass
        try:
            self.section.getSectionIndex(49)
            self.fail("fm.getSectionIndex(): 49")
        except:
            pass

    def test_get_section_content(self):
        self.assertEqual("abracadabra", self.section.getContent(0))
        self.assertEqual("mississippi", self.section.getContent(1))
        self.assertEqual("abracadabra2 mississippi2", self.section.getContent(2))

    def test_get_section_content_boundary(self):
        try:
            self.section.getContent(3)
            self.fail("fm.getContent()")
        except:
            pass
        try:
            self.section.getContent(-1)
            self.fail("fm.getContent()")
        except:
            pass

    def test_get_section_name(self):
        self.assertEqual("doc1", self.section.getName(0))
        self.assertEqual("doc2", self.section.getName(1))
        self.assertEqual("doc3", self.section.getName(2))

    def test_get_section_name_boundary(self):
        try:
            self.section.getName(3)
            self.fail("fm.getName()")
        except:
            pass
        try:
            self.section.getName(-1)
            self.fail("fm.getName()")
        except:
            pass

    def test_load_dump_and_doc_sizes(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.section = self.oktavia.getSection('document')
        self.assertEqual(3, self.section.size())

    def test_load_dump_and_get_section_index(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.section = self.oktavia.getSection('document')

        self.assertEqual(0, self.section.getSectionIndex(0))
        self.assertEqual(0, self.section.getSectionIndex(10))
        self.assertEqual(1, self.section.getSectionIndex(12))
        self.assertEqual(1, self.section.getSectionIndex(22))
        self.assertEqual(2, self.section.getSectionIndex(24))
        self.assertEqual(2, self.section.getSectionIndex(48))

    def test_load_dump_and_get_section_index_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.section = self.oktavia.getSection('document')

        try:
            self.section.getSectionIndex(-1)
            self.fail("fm.getSectionIndex()")
        except:
            pass
        try:
            self.section.getSectionIndex(49)
            self.fail("fm.getSectionIndex()")
        except:
            pass

    def test_load_dump_and_get_section_content(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.section = self.oktavia.getSection('document')
        self.assertEqual("abracadabra", self.section.getContent(0))
        self.assertEqual("mississippi", self.section.getContent(1))
        self.assertEqual("abracadabra2 mississippi2", self.section.getContent(2))

    def test_load_dump_and_get_section_content_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.section = self.oktavia.getSection('document')

        try:
            self.section.getContent(3)
            self.fail("fm.getContent()")
        except:
            pass
        try:
            self.section.getContent(-1)
            self.fail("fm.getContent()")
        except:
            pass

    def test_load_dump_and_get_section_name(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.section = self.oktavia.getSection('document')

        self.assertEqual("doc1", self.section.getName(0))
        self.assertEqual("doc2", self.section.getName(1))
        self.assertEqual("doc3", self.section.getName(2))

    def test_load_dump_and_get_section_name_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.section = self.oktavia.getSection('document')

        try:
            self.section.getName(3)
            self.fail("fm.getName()")
        except:
            pass
        try:
            self.section.getName(-1)
            self.fail("fm.getName()")
        except:
            pass
