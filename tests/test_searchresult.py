import unittest
from oktavia.searchresult import SingleResult, SearchSummary

class SingleResultTest(unittest.TestCase):
    def test_simple_registration(self):
        result = SingleResult();
        section = result.get_search_unit(0);
        section.add_position('hello', 0, False);
        section.add_position('world', 7, False);
        self.assertEqual(2, len(section))

    def test_duplicate_longer_word_is_kept(self):
        result = SingleResult();
        section = result.get_search_unit(0);
        section.add_position('hello', 0, False);
        section.add_position('hello world', 0, False);
        position = section.get(0);

        self.assertEqual(1, len(section))
        self.assertEqual("hello world", position.word)

    def test_duplicate_no_stemmed_word_is_kept(self):
        result = SingleResult();
        section = result.get_search_unit(0);
        section.add_position('hello', 0, True);
        section.add_position('hello', 0, False);
        position = section.get(0);

        self.assertEqual(1, len(section))
        self.assertFalse(position.stemmed)

    def test_and_merge(self):
        result1 = SingleResult();
        result1.get_search_unit(0);
        result1.get_search_unit(1);

        result2 = SingleResult();
        result2.get_search_unit(0);

        result3 = result1.merge(result2);

        self.assertEqual(1, len(result3))

    def test_and_merge_2(self):
        result1 = SingleResult();
        result1.get_search_unit(0);
        result1.get_search_unit(1);

        result2 = SingleResult();
        result2.get_search_unit(2);

        result3 = result1.merge(result2);

        self.assertEqual(0, len(result3))

    def test_or_merge(self):
        result1 = SingleResult();
        result1.get_search_unit(0);
        result1.get_search_unit(1);

        result2 = SingleResult();
        result2.get_search_unit(0);
        result2.get_search_unit(2);
        result2.OR = True;

        result3 = result1.merge(result2);

        self.assertEqual(3, len(result3))

    def test_not_merge(self):
        result1 = SingleResult();
        result1.get_search_unit(0);
        result1.get_search_unit(1);
        result1.get_search_unit(2);

        result2 = SingleResult();
        result2.get_search_unit(0);
        result2.get_search_unit(2);
        result2.NOT = True;

        result3 = result1.merge(result2);
        print(result3)
        self.assertEqual(1, len(result3))

    def test_merge(self):
        summary = SearchSummary();
        singleresult1 = SingleResult();
        singleresult1.get_search_unit(0);
        singleresult1.get_search_unit(1);

        singleresult2 = SingleResult();
        singleresult2.get_search_unit(1);

        summary.add(singleresult1);
        summary.add(singleresult2);
        summary.merge_result();

        self.assertEqual(1, len(summary))

    def test_proposal(self):
        summary = SearchSummary();
        singleresult1 = SingleResult();
        singleresult1.get_search_unit(0);
        singleresult1.get_search_unit(1);

        singleresult2 = SingleResult();
        singleresult2.get_search_unit(2);

        summary.add(singleresult1);
        summary.add(singleresult2);

        proposals = summary.get_proposals();

        self.assertEqual(1, proposals[0].omit)
        self.assertEqual(2, proposals[0].expect)
        self.assertEqual(0, proposals[1].omit)
        self.assertEqual(1, proposals[1].expect)

    def test_sort(self):
        summary = SearchSummary();
        singleresult = SingleResult();
        section1 = singleresult.get_search_unit(0);
        section2 = singleresult.get_search_unit(1);
        section3 = singleresult.get_search_unit(2);
        self.assertEqual(0, section1.id)
        self.assertEqual(1, section2.id)
        self.assertEqual(2, section3.id)

        summary.add(singleresult);
        summary.merge_result();
        summary.result.get_search_unit(0).score = 100;
        summary.result.get_search_unit(1).score = 300;
        summary.result.get_search_unit(2).score = 200;

        result = summary.get_sorted_result();
        self.assertEqual(3, len(result))
        self.assertEqual(1, result[0].id)
        self.assertEqual(2, result[1].id)
        self.assertEqual(0, result[2].id)

