import unittest
from oktavia.bitvector import BitVector

class BitVectorTest(unittest.TestCase):

    def setUp(self):
        self.bv0 = BitVector()
        self.bv1 = BitVector()
        self.src_values = [0, 511, 512, 1000, 2000, 3000]

        for i in range(self.src_vlaues[-1]):
            self.bv0.set(i, true)

        for v in self.src_values:
            self.bv1.set(v, true)
            self.bv0.set(v, false)

        self.bv1.build()
        self.bv0.build()
'''
    def test_size(self):
        self.assertEqual(self.bv1.size()).toBe(self.src_values[self.src_values.length - 1] + 1) # == 3001
        self.assertEqual(self.bv1.size(true)).toBe(self.src_values.length) # == 6
        self.assertEqual(self.bv0.size()).toBe(self.src_values[self.src_values.length - 1] + 1) # == 3001
        self.assertEqual(self.bv0.size(false)).toBe(self.src_values.length) # == 6
    

    def test_get(self):
        for v in self.src_values:
            self.assertEqual(self.bv1.get(v)).toBe(true)
            self.assertEqual(self.bv0.get(v)).toBe(false)

    def test_rank(self):
        for v in self.src_values:
            self.assertEqual(self.bv1.rank(v, true)).toBe(i)
            self.assertEqual(self.bv0.rank(v, false)).toBe(i)

    def test_select(self):
        for v in self.src_values:
            self.assertEqual(self.bv1.select(i, true)).toBe(v)
            self.assertEqual(self.bv0.select(i, false)).toBe(v)

    def test_load_dump_and_size(self):
        dump1 = self.bv1.dump()
        dump0 = self.bv0.dump()
        self.bv1.load(dump1)
        self.bv0.load(dump0)

        self.assertEqual(self.bv1.size()).toBe(self.src_values[self.src_values.length - 1] + 1) # == 3001
        self.assertEqual(self.bv1.size(true)).toBe(self.src_values.length) # == 6
        self.assertEqual(self.bv0.size()).toBe(self.src_values[self.src_values.length - 1] + 1) # == 3001
        self.assertEqual(self.bv0.size(false)).toBe(self.src_values.length) # == 6
    

    def test_load_dump_and_get(self):
        dump1 = self.bv1.dump()
        dump0 = self.bv0.dump()
        self.bv1.load(dump1)
        self.bv0.load(dump0)

        for v in self.src_values:
            v = self.src_values[i]
            self.assertEqual(self.bv1.get(v)).toBe(true)
            self.assertEqual(self.bv0.get(v)).toBe(false)

    def test_load_dump_and_rank(self):
        dump1 = self.bv1.dump()
        dump0 = self.bv0.dump()
        self.bv1.load(dump1)
        self.bv0.load(dump0)

        for v in self.src_values:
            v = self.src_values[i]
            self.assertEqual(self.bv1.rank(v, true)).toBe(i)
            self.assertEqual(self.bv0.rank(v, false)).toBe(i)

    def test_load_dump_and_select(self):
        dump1 = self.bv1.dump()
        dump0 = self.bv0.dump()
        self.bv1.load(dump1)
        self.bv0.load(dump0)

        for v in self.src_values:
            v = self.src_values[i]
            self.assertEqual(self.bv1.select(i, true)).toBe(v)
            self.assertEqual(self.bv0.select(i, false)).toBe(v)
'''
