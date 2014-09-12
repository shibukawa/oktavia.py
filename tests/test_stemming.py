import unittest
from oktavia.oktavia import Oktavia
import snowballstemmer

class StemmingTest(unittest.TestCase):
    def setUp(self):
        self.oktavia = Oktavia()
        self.oktavia.set_stemmer(snowballstemmer.EnglishStemmer())
        self.section = self.oktavia.add_section(u'document')
        self.oktavia.add_word(u"stemming baby", stemming=True)
        self.section.set_tail(u"doc1")
        self.oktavia.add_word(u"stemmed babies", stemming=True)
        self.section.set_tail(u"doc2")
        self.oktavia.build()

    def test_search_without_stemming(self):
        results = self.oktavia.raw_search(u'baby', stemming=False)
        self.assertEqual(1, len(results))

    def test_search_with_stemming(self):
        results = self.oktavia.raw_search(u'baby', stemming=True)
        self.assertEqual(1, len(results))

    def test_load_dump_and_search_without_stemming(self):
        dump = self.oktavia.dump()
        oktavia = Oktavia()
        oktavia.set_stemmer(snowballstemmer.EnglishStemmer())
        oktavia.load(dump)
        results = oktavia.raw_search(u'baby', stemming=False)
        self.assertEqual(1, len(results))

    def test_load_dump_and_search_with_stemming(self):
        dump = self.oktavia.dump()
        oktavia = Oktavia()
        oktavia.set_stemmer(snowballstemmer.EnglishStemmer())
        oktavia.load(dump)
        results = oktavia.raw_search(u'baby', stemming=True)
        self.assertEqual(1, len(results))
