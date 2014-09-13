import unittest
from oktavia.binaryio import BinaryInput
from oktavia.binaryio import BinaryOutput

class BinaryIOTest(unittest.TestCase):
    def test_16bit_number(self):
        output1 = BinaryOutput()
        output1.dump_16bit_number(0)
        input1 = BinaryInput(output1.result())
        self.assertEqual(0, input1.load_16bit_number())

        output2 = BinaryOutput()
        output2.dump_16bit_number(65535)
        input2 = BinaryInput(output2.result())
        self.assertEqual(65535, input2.load_16bit_number())

        output3 = BinaryOutput()
        output3.dump_16bit_number(65536)
        input3 = BinaryInput(output2.result())
        self.assertNotEqual(65536, input3.load_16bit_number())

    def test_32bit_number(self):
        output1 = BinaryOutput()
        output1.dump_32bit_number(0)
        input1 = BinaryInput(output1.result())
        self.assertEqual(0, input1.load_32bit_number())

        output2 = BinaryOutput()
        output2.dump_32bit_number(4294967295)
        input2 = BinaryInput(output2.result())
        self.assertEqual(4294967295, input2.load_32bit_number())

        output3 = BinaryOutput()
        output3.dump_32bit_number(4294967296)
        input3 = BinaryInput(output3.result())
        self.assertNotEqual(4294967296, input3.load_32bit_number())

    def test_string(self):
        output1 = BinaryOutput()
        output1.dump_string('hello world')
        input1 = BinaryInput(output1.result())
        self.assertEqual('hello world', input1.load_string())

        # 7bit safe charactes will be compressed
        self.assertTrue(len(output1.result()) / 2 <= len('hello world'))

        output2 = BinaryOutput()
        output2.dump_string('')
        self.assertEqual(len('') + 1, len(output2.result()) / 2)

        # 7bit unsafe charactes will not be compressed
        output3 = BinaryOutput()
        output3.dump_string(u'\u1111\u1111')
        self.assertEqual(len(output3.result()) / 2, len(u'\u1111\u1111') + 1)

    def test_string_list(self):
        output1 = BinaryOutput()
        output1.dump_string_list(['hello', 'world'])
        input1 = BinaryInput(output1.result())
        result1 = input1.load_string_list()
        self.assertEqual('hello', result1[0])
        self.assertEqual('world', result1[1])

        output2 = BinaryOutput()
        output2.dump_string_list(['\u1112', '\u1113'])
        input2 = BinaryInput(output2.result())
        result2 = input2.load_string_list()
        self.assertEqual('\u1112', result2[0])
        self.assertEqual('\u1113', result2[1])

    def test_string_list_map(self):
        src = {'hello': ['HELLO'], 'world': ['WORLD']}

        output = BinaryOutput()
        output.dump_string_list_map(src)
        input = BinaryInput(output.result())
        result = input.load_string_list_map()
        self.assertEqual('HELLO', result['hello'][0])
        self.assertEqual('WORLD', result['world'][0])

    def test_32bit_number_list_blank(self):
        list = [0, 0, 0, 0, 0, 0]

        output = BinaryOutput()
        output.dump_32bit_number_list(list)
        self.assertEqual((2 + 1) * 2, len(output.result()))

        input = BinaryInput(output.result())
        result = input.load_32bit_number_list()
        self.assertEqual(6, len(result))
        self.assertEqual(0, result[0])
        self.assertEqual(0, result[5])
        self.assertEqual((2 + 1) * 2, input._offset)

    def test_32bit_number_list_non_blank(self):
        list = [1, 1, 1, 1, 1, 1]

        output = BinaryOutput()
        output.dump_32bit_number_list(list)
        self.assertEqual(2 * (2 * 6 + 2 + 1), len(output.result()))

        input = BinaryInput(output.result())
        result = input.load_32bit_number_list()
        self.assertEqual(6, len(result))
        self.assertEqual(1, result[0])
        self.assertEqual(1, result[5])
        self.assertEqual(2 * (2 * 6 + 2 + 1), input._offset)

    def test_32bit_number_list_zebra(self):
        list = [1, 0, 1, 0, 1, 0]

        output = BinaryOutput()
        output.dump_32bit_number_list(list)
        self.assertEqual(2 * (2 * 3 + 2 + 1), len(output.result()))

        input = BinaryInput(output.result())
        result = input.load_32bit_number_list()
        self.assertEqual(6, len(result))
        self.assertEqual(1, result[0])
        self.assertEqual(0, result[1])
        self.assertEqual(1, result[2])
        self.assertEqual(0, result[3])
        self.assertEqual(1, result[4])
        self.assertEqual(0, result[5])
        self.assertEqual(2 * (2 * 3 + 2 + 1), input._offset)

    def test_32bit_number_list_combo1(self):
        # non-blank + blank
        list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]

        output = BinaryOutput()
        output.dump_32bit_number_list(list)
        self.assertEqual(2 * (2 + 1 + 2 * 17 + 1), len(output.result()))

        input = BinaryInput(output.result())
        result = input.load_32bit_number_list()
        self.assertEqual(len(list), len(result))
        self.assertEqual(1, result[0])
        self.assertEqual(1, result[15])
        self.assertEqual(0, result[17])
        self.assertEqual(0, result[19])
        self.assertEqual(2 * (2 + 1 + 2 * 17 + 1), input._offset)

    def test_32bit_number_list_combo2(self):
        # blank + non-blank
        list = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


        output = BinaryOutput()
        output.dump_32bit_number_list(list)
        self.assertEqual(2 * (2 + 1 + 1 + 2 * 17), len(output.result()))

        input = BinaryInput(output.result())
        result = input.load_32bit_number_list()
        self.assertEqual(len(list), len(result))
        self.assertEqual(0, result[0])
        self.assertEqual(0, result[2])
        self.assertEqual(1, result[3])
        self.assertEqual(1, result[19])
        self.assertEqual(2 * (2 + 1 + 1 + 2 * 17), input._offset)

    def test_32bit_number_list_combo3(self):
        # non-blank + zebra
        list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0]

        output = BinaryOutput()
        output.dump_32bit_number_list(list)
        self.assertEqual(2 * (2 + 1 + 2 * 16 + 1 + 1 + 2 * 3), len(output.result()))

        input = BinaryInput(output.result())
        result = input.load_32bit_number_list()
        self.assertEqual(len(list), len(result))
        self.assertEqual(1, result[0])
        self.assertEqual(1, result[9])
        self.assertEqual(0, result[16])
        self.assertEqual(1, result[18])
        self.assertEqual(2 * (2 + 1 + 2 * 16 + 1 + 1 + 2 * 3), input._offset)

    def test_32bit_number_list_combo4(self):
        # zebra + non-block
        list = [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]

        output = BinaryOutput()
        output.dump_32bit_number_list(list)
        self.assertEqual(2 * (2 + 1 + 2 * 11 + 1 + 2 * 16), len(output.result()))

        input = BinaryInput(output.result())
        result = input.load_32bit_number_list()
        self.assertEqual(len(list), len(result))
        self.assertEqual(1, result[0])
        self.assertEqual(0, result[14])
        self.assertEqual(1, result[15])
        self.assertEqual(2, result[30])
        self.assertEqual(2 * (2 + 1 + 2 * 11 + 1 + 2 * 16), input._offset)

    def test_32bit_number_list_combo5(self):
        # zero + zebra
        list = [0, 0, 0, 0, 0, 0, 1]

        output = BinaryOutput()
        output.dump_32bit_number_list(list)
        self.assertEqual(2 * (2 + 1 + 1 + 2), len(output.result()))

        input = BinaryInput(output.result())
        result = input.load_32bit_number_list()
        self.assertEqual(len(list), len(result))
        self.assertEqual(0, result[0])
        self.assertEqual(1, result[6])
        self.assertEqual(2 * (2 + 1 + 1 + 2), input._offset)

    def test_32bit_number_list_combo6(self):
        # zebra + zero
        list = [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        output = BinaryOutput()
        output.dump_32bit_number_list(list)
        self.assertEqual(2 * (2 + 1 + 2 * 12 + 1), len(output.result()))

        input = BinaryInput(output.result())
        result = input.load_32bit_number_list()
        self.assertEqual(len(list), len(result))
        self.assertEqual(1, result[0])
        self.assertEqual(1, result[14])
        self.assertEqual(0, result[15])
        self.assertEqual(0, result[23])
        self.assertEqual(2 * (2 + 1 + 2 * 12 + 1), input._offset)
