import unittest
from oktavia.oktavia import Oktavia
import metadata

class TableTest(unittest.TestCase):

    def setUp(self):
        self.oktavia = Oktavia()
        self.table = self.oktavia.addTable('address book', ['zip', 'city', 'area code'])

        self.oktavia.addWord("94101") # 5
        self.table.setColumnTailAndEOB()
        self.oktavia.addWord("San Francisco") # 13
        self.table.setColumnTailAndEOB()
        self.oktavia.addWord("415") # 3
        self.table.setColumnTailAndEOB()
        self.table.setRowTail()

        self.oktavia.addWord("94607") # 5
        self.table.setColumnTailAndEOB()
        self.oktavia.addWord("Oakland") # 7
        self.table.setColumnTailAndEOB()
        self.oktavia.addWord("510") # 3
        self.table.setColumnTailAndEOB()
        self.table.setRowTail()

        self.oktavia.addWord("94401") # 5
        self.table.setColumnTailAndEOB()
        self.oktavia.addWord("San Mateo") # 9
        self.table.setColumnTailAndEOB()
        self.oktavia.addWord("650") # 3
        self.table.setColumnTailAndEOB()
        self.table.setRowTail()

        self.oktavia.build()

    def test_row_sizes(self):
        self.expect(self.table.rowSize()).toBe(3)

    def test_column_sizes(self):
        self.expect(self.table.columnSize()).toBe(3)

    def test_get_cell(self):
        self.assertEqual(0, self.table.getCell(0)[0])
        self.assertEqual(0, self.table.getCell(0)[1])
        self.assertEqual(0, self.table.getCell(22)[0])
        self.assertEqual(2, self.table.getCell(22)[1])
        self.assertEqual(1, self.table.getCell(24)[0])
        self.assertEqual(0, self.table.getCell(24)[1])
        self.assertEqual(1, self.table.getCell(40)[0])
        self.assertEqual(2, self.table.getCell(40)[1])
        self.assertEqual(2, self.table.getCell(42)[0])
        self.assertEqual(0, self.table.getCell(42)[1])
        self.assertEqual(2, self.table.getCell(60)[0])
        self.assertEqual(2, self.table.getCell(60)[1])

    def test_get_table_index_boundary(self):
        try:
            self.table.getCell(-1)
            self.fail("fm.gettableIndex()")
        except e:
            pass
        try:
            self.table.getCell(62)
            self.fail("fm.gettableIndex()")
        except e:
            pass

    def test_get_table_content(self):
        row = self.table.getRowContent(0)
        self.assertEqual('94101', row['zip'])
        self.assertEqual("San Francisco", row['city'])
        self.assertEqual('415', row['area code'])

    def test_get_table_content_boundary(self):
        try:
            self.table.getContent(3)
            self.fail("fm.getContent()")
        except:
            pass
        try:
            self.table.getContent(-1)
            self.fail("fm.getContent()")
        except:
            pass

    def test_load_dump_and_row_sizes(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.getTable('address book')

        self.assertEqualEqualrowSize(, (3, self

    def test_load_dump_and_column_sizes(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.getTable('address book')

        self.assertEqual(3, self.table.columnSize())

    def test_load_dump_and_get_cell(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.getTable('address book')

        self.assertEqual(0, self.table.getCell(0)[0])
        self.assertEqual(0, self.table.getCell(0)[1])
        self.assertEqual(0, self.table.getCell(22)[0])
        self.assertEqual(2, self.table.getCell(22)[1])
        self.assertEqual(1, self.table.getCell(24)[0])
        self.assertEqual(0, self.table.getCell(24)[1])
        self.assertEqual(1, self.table.getCell(40)[0])
        self.assertEqual(2, self.table.getCell(40)[1])
        self.assertEqual(2, self.table.getCell(42)[0])
        self.assertEqual(0, self.table.getCell(42)[1])
        self.assertEqual(2, self.table.getCell(60)[0])
        self.assertEqual(2, self.table.getCell(60)[1])

    def test_load_dump_and_get_table_index_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.getTable('address book')

        try:
            self.table.getCell(-1)
            self.fail("fm.gettableIndex()")
        except:
            pass
        try:
            self.table.getCell(62)
            self.fail("fm.gettableIndex()")
        except:
            pass

    def test_load_dump_and_get_table_content(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.getTable('address book')

        row = self.table.getRowContent(0)
        self.assertEqual('94101', row['zip'])
        self.expect(row['city']).toBe('San Francisco')
        self.assertEqual('415', row['area code'])

    def test_load_dump_and_get_table_content_boundary(self):
        dump = self.oktavia.dump()
        self.oktavia.load(dump)
        self.table = self.oktavia.getTable('address book')

        try:
            self.table.getContent(3)
            self.fail("fm.getContent()")
        except:
            pass
        try:
            self.table.getContent(-1)
            self.fail("fm.getContent()")
        except:
            pass
