import unittest
from oktavia.oktavia import Oktavia
from oktavia.metadata import Table


class TableTest(unittest.TestCase):

    def setUp(self):
        self.oktavia = Oktavia()
        self.table = self.oktavia.add_table('address book', ['zip', 'city', 'area code'])

        self.oktavia.add_word("94101") # 5
        self.table.set_column_tail_and_EOB()
        self.oktavia.add_word("San Francisco") # 13
        self.table.set_column_tail_and_EOB()
        self.oktavia.add_word("415") # 3
        self.table.set_column_tail_and_EOB()
        self.table.set_row_tail()

        self.oktavia.add_word("94607") # 5
        self.table.set_column_tail_and_EOB()
        self.oktavia.add_word("Oakland") # 7
        self.table.set_column_tail_and_EOB()
        self.oktavia.add_word("510") # 3
        self.table.set_column_tail_and_EOB()
        self.table.set_row_tail()

        self.oktavia.add_word("94401") # 5
        self.table.set_column_tail_and_EOB()
        self.oktavia.add_word("San Mateo") # 9
        self.table.set_column_tail_and_EOB()
        self.oktavia.add_word("650") # 3
        self.table.set_column_tail_and_EOB()
        self.table.set_row_tail()

        self.oktavia.build()

    def test_row_sizes(self):
        self.assertEqual(3, self.table.row_size())

    def test_column_sizes(self):
        self.assertEqual(3, self.table.column_size())

    def test_get_cell(self):
        self.assertEqual(0, self.table.get_cell(0)[0])
        self.assertEqual(0, self.table.get_cell(0)[1])
        self.assertEqual(0, self.table.get_cell(22)[0])
        self.assertEqual(2, self.table.get_cell(22)[1])
        self.assertEqual(1, self.table.get_cell(24)[0])
        self.assertEqual(0, self.table.get_cell(24)[1])
        self.assertEqual(1, self.table.get_cell(40)[0])
        self.assertEqual(2, self.table.get_cell(40)[1])
        self.assertEqual(2, self.table.get_cell(42)[0])
        self.assertEqual(0, self.table.get_cell(42)[1])
        self.assertEqual(2, self.table.get_cell(60)[0])
        self.assertEqual(2, self.table.get_cell(60)[1])

    def test_get_table_index_boundary(self):
        try:
            self.table.get_cell(-1)
            self.fail("fm.gettableIndex()")
        except:
            pass
        try:
            self.table.get_cell(62)
            self.fail("fm.gettableIndex()")
        except:
            pass

    def test_get_table_content(self):
        row = self.table.get_row_content(0)
        self.assertEqual('94101', row['zip'])
        self.assertEqual("San Francisco", row['city'])
        self.assertEqual('415', row['area code'])

    def test_get_table_content_boundary(self):
        try:
            self.table.get_content(3)
            self.fail("fm.get_content()")
        except:
            pass
        try:
            self.table.get_content(-1)
            self.fail("fm.get_content()")
        except:
            pass

    def test_load_dump_and_row_sizes(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.get_table('address book')
        self.assertEqual(3, self.table.row_size())

    def test_load_dump_and_column_sizes(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.get_table('address book')

        self.assertEqual(3, self.table.column_size())

    def test_load_dump_and_get_cell(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.get_table('address book')

        self.assertEqual(0, self.table.get_cell(0)[0])
        self.assertEqual(0, self.table.get_cell(0)[1])
        self.assertEqual(0, self.table.get_cell(22)[0])
        self.assertEqual(2, self.table.get_cell(22)[1])
        self.assertEqual(1, self.table.get_cell(24)[0])
        self.assertEqual(0, self.table.get_cell(24)[1])
        self.assertEqual(1, self.table.get_cell(40)[0])
        self.assertEqual(2, self.table.get_cell(40)[1])
        self.assertEqual(2, self.table.get_cell(42)[0])
        self.assertEqual(0, self.table.get_cell(42)[1])
        self.assertEqual(2, self.table.get_cell(60)[0])
        self.assertEqual(2, self.table.get_cell(60)[1])

    def test_load_dump_and_get_table_index_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.get_table('address book')

        try:
            self.table.get_cell(-1)
            self.fail("fm.gettableIndex()")
        except:
            pass
        try:
            self.table.get_cell(62)
            self.fail("fm.gettableIndex()")
        except:
            pass

    def test_load_dump_and_get_table_content(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.get_table('address book')

        row = self.table.get_row_content(0)
        self.assertEqual('94101', row['zip'])
        self.assertEqual('San Francisco', row['city'])
        self.assertEqual('415', row['area code'])

    def test_load_dump_and_get_table_content_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.get_table('address book')

        try:
            self.table.get_content(3)
            self.fail("fm.get_content()")
        except:
            pass
        try:
            self.table.get_content(-1)
            self.fail("fm.get_content()")
        except:
            pass
