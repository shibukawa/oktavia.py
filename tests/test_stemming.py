import unittest
from oktavia.oktavia import Oktavia
import metadata
import snowballstemmer.englishstemmer

class StemmingTest(unittest.TestCase):

    def setUp(self):
        self.oktavia = Oktavia()
        self.oktavia.setStemmer(new EnglishStemmer())
        self.section = self.oktavia.addSection('document')
        self.oktavia.addWord("stemming baby", True)
        self.section.setTail("doc1")
        self.oktavia.addWord("stemmed babies", True)
        self.section.setTail("doc2")
        self.oktavia.build()

    def test_search_without_stemming(self):
        results = self.oktavia.rawSearch('baby', False)
        self.assertEqual(1, results.length)

    def test_search_with_stemming(self):
        results = self.oktavia.rawSearch('baby', True)
        self.assertEqual(1, results.length)

    def test_load_dump_and_search_without_stemming(self):
        dump = self.oktavia.dump()
        oktavia = Oktavia()
        oktavia.setStemmer(EnglishStemmer())
        oktavia.load(dump)
        results = oktavia.rawSearch('baby', False)
        self.assertEqual(1, results.length)

    def test_load_dump_and_search_with_stemming(self):
        dump = self.oktavia.dump()
        oktavia = Oktavia()
        oktavia.setStemmer(EnglishStemmer())
        oktavia.load(dump)
        results = oktavia.rawSearch('baby', True)
        self.assertEqual(1, results.length)
