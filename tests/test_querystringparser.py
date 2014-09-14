import unittest
from oktavia.queryparser import QueryStringParser

class QueryStringParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = QueryStringParser()

    def test_single_string_and(self):
        self.parser.parse('word1 word2')
        self.assertEqual(2, len(self.parser.queries))

        self.assertEqual('word1', self.parser.queries[0].word)
        self.assertFalse(self.parser.queries[0].OR)
        self.assertFalse(self.parser.queries[0].NOT)
        self.assertFalse(self.parser.queries[0].RAW)

        self.assertEqual('word2', self.parser.queries[1].word)
        self.assertFalse(self.parser.queries[1].OR)
        self.assertFalse(self.parser.queries[1].NOT)
        self.assertFalse(self.parser.queries[1].RAW)

    def test_single_string_or(self):
        self.parser.parse('word1 OR word2')
        self.assertEqual(2, len(self.parser.queries))

        self.assertEqual('word1', self.parser.queries[0].word)
        self.assertFalse(self.parser.queries[0].OR)
        self.assertFalse(self.parser.queries[0].NOT)
        self.assertFalse(self.parser.queries[0].RAW)

        self.assertEqual('word2', self.parser.queries[1].word)
        self.assertTrue(self.parser.queries[1].OR)
        self.assertFalse(self.parser.queries[1].NOT)
        self.assertFalse(self.parser.queries[1].RAW)

    def test_single_string_not(self):
        self.parser.parse('word1 -word2')
        self.assertEqual(2, len(self.parser.queries))

        self.assertEqual('word1', self.parser.queries[0].word)
        self.assertFalse(self.parser.queries[0].OR)
        self.assertFalse(self.parser.queries[0].NOT)
        self.assertFalse(self.parser.queries[0].RAW)

        self.assertEqual('word2', self.parser.queries[1].word)
        self.assertFalse(self.parser.queries[1].OR)
        self.assertTrue(self.parser.queries[1].NOT)
        self.assertFalse(self.parser.queries[1].RAW)

    def test_single_string_raw(self):
        self.parser.parse('word1 "word2"')
        self.assertEqual(2, len(self.parser.queries))

        self.assertEqual('word1', self.parser.queries[0].word)
        self.assertFalse(self.parser.queries[0].OR)
        self.assertFalse(self.parser.queries[0].NOT)
        self.assertFalse(self.parser.queries[0].RAW)

        self.assertEqual('word2', self.parser.queries[1].word)
        self.assertFalse(self.parser.queries[1].OR)
        self.assertFalse(self.parser.queries[1].NOT)
        self.assertTrue(self.parser.queries[1].RAW)

    def test_single_string_raw_not(self):
        self.parser.parse('word1 -"word2"')
        self.assertEqual(2, len(self.parser.queries))

        self.assertEqual('word1', self.parser.queries[0].word)
        self.assertFalse(self.parser.queries[0].OR)
        self.assertFalse(self.parser.queries[0].NOT)
        self.assertFalse(self.parser.queries[0].RAW)

        self.assertEqual('word2', self.parser.queries[1].word)
        self.assertFalse(self.parser.queries[1].OR)
        self.assertTrue(self.parser.queries[1].NOT)
        self.assertTrue(self.parser.queries[1].RAW)
