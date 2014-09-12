import unittest
from oktavia.oktavia import Oktavia
from oktavia.metadata import Section

class SectionTest(unittest.TestCase):

    def setUp(self):
        self.oktavia = Oktavia()
        self.section = self.oktavia.add_section(u'document')
        self.oktavia.add_word(u"abracadabra")
        self.section.set_tail(u"doc1")
        self.oktavia.add_end_of_block()
        self.oktavia.add_word(u"mississippi")
        self.section.set_tail(u"doc2")
        self.oktavia.add_end_of_block()
        self.oktavia.add_word(u"abracadabra2 mississippi2")
        self.section.set_tail(u"doc3")
        self.oktavia.add_end_of_block()
        self.oktavia.build(25)

    def test_doc_sizes(self):
        self.assertEqual(3, self.section.size())

    def test_get_section_index(self):
        self.assertEqual(0, self.section.get_section_index(0))
        self.assertEqual(0, self.section.get_section_index(10))
        self.assertEqual(1, self.section.get_section_index(12))
        self.assertEqual(1, self.section.get_section_index(22))
        self.assertEqual(2, self.section.get_section_index(24))
        self.assertEqual(2, self.section.get_section_index(48))

    def test_get_section_index_boundary(self):
        try:
            self.section.get_section_index(-1)
            self.fail("fm.get_section_index(): -1")
        except:
            pass
        try:
            self.section.get_section_index(49)
            self.fail("fm.get_section_index(): 49")
        except:
            pass

    def test_get_section_content(self):
        self.assertEqual(u"abracadabra", self.section.get_content(0))
        self.assertEqual(u"mississippi", self.section.get_content(1))
        self.assertEqual(u"abracadabra2 mississippi2", self.section.get_content(2))

    def test_get_section_content_boundary(self):
        try:
            self.section.get_content(3)
            self.fail("fm.get_content()")
        except:
            pass
        try:
            self.section.get_content(-1)
            self.fail("fm.get_content()")
        except:
            pass

    def test_get_section_name(self):
        self.assertEqual("doc1", self.section.get_name(0))
        self.assertEqual("doc2", self.section.get_name(1))
        self.assertEqual("doc3", self.section.get_name(2))

    def test_get_section_name_boundary(self):
        try:
            self.section.get_name(3)
            self.fail("fm.get_name()")
        except:
            pass
        try:
            self.section.get_name(-1)
            self.fail("fm.get_name()")
        except:
            pass

    def test_load_dump_and_doc_sizes(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.section = self.oktavia.get_section('document')
        self.assertEqual(3, self.section.size())

    def test_load_dump_and_get_section_index(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.section = self.oktavia.get_section('document')

        self.assertEqual(0, self.section.get_section_index(0))
        self.assertEqual(0, self.section.get_section_index(10))
        self.assertEqual(1, self.section.get_section_index(12))
        self.assertEqual(1, self.section.get_section_index(22))
        self.assertEqual(2, self.section.get_section_index(24))
        self.assertEqual(2, self.section.get_section_index(48))

    def test_load_dump_and_get_section_index_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.section = self.oktavia.get_section('document')

        try:
            self.section.get_section_index(-1)
            self.fail("fm.get_section_index()")
        except:
            pass
        try:
            self.section.get_section_index(49)
            self.fail("fm.get_section_index()")
        except:
            pass

    def test_load_dump_and_get_section_content(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.section = self.oktavia.get_section('document')
        self.assertEqual("abracadabra", self.section.get_content(0))
        self.assertEqual("mississippi", self.section.get_content(1))
        self.assertEqual("abracadabra2 mississippi2", self.section.get_content(2))

    def test_load_dump_and_get_section_content_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.section = self.oktavia.get_section('document')

        try:
            self.section.get_content(3)
            self.fail("fm.get_content()")
        except:
            pass
        try:
            self.section.get_content(-1)
            self.fail("fm.get_content()")
        except:
            pass

    def test_load_dump_and_get_section_name(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.section = self.oktavia.get_section('document')

        self.assertEqual("doc1", self.section.get_name(0))
        self.assertEqual("doc2", self.section.get_name(1))
        self.assertEqual("doc3", self.section.get_name(2))

    def test_load_dump_and_get_section_name_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.section = self.oktavia.get_section('document')

        try:
            self.section.get_name(3)
            self.fail("fm.get_name()")
        except:
            pass
        try:
            self.section.get_name(-1)
            self.fail("fm.get_name()")
        except:
            pass
