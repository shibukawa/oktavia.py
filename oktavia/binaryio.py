import struct
import sys

_range = range if sys.version_info[0] == 3 else xrange

class BinaryInput(object):
    def __init__(self, buffer, offset=0):
        self._buffer = buffer;
        self._offset = offset;

    def load_32bit_number(self):
        '''
        :return: number
        '''
        result = struct.unpack_from('<I', self._buffer, self._offset)[0]
        self._offset += 4
        return result

    def load_16bit_number(self):
        '''
        :return: number
        '''
        result = struct.unpack_from('<H', self._buffer, self._offset)[0]
        self._offset += 2
        return result

    def load_string(self):
        str_length = self.load_16bit_number()
        offset = self._offset
        data = self._buffer
        if (str_length > 32767):
            str_length = str_length - 32768
            result = data[offset : offset + str_length].decode('latin-1')
            self._offset += str_length + str_length % 2
        else:
            result = data[offset : offset + str_length * 2].decode('utf_16_le')
            self._offset += str_length * 2
        return result

    def load_string_list(self):
        length = self.load_32bit_number()
        return [self.load_string() for i in _range(length)]

    def load_string_list_map(self):
        result = {}
        length = self.load_32bit_number()
        for i in _range(length):
            key = self.load_string()
            values = self.load_string_list()
            result[key] = values
        return result

    def load_32bit_number_list(self):
        result_length = self.load_32bit_number()
        result = []
        while len(result) < result_length:
            tag = self.load_16bit_number()
            if (tag >> 15) == 1: # zebra
                length = min(result_length - len(result), 15)
                for i in _range(length):
                    if (tag >> i) & 0x1:
                        result.append(self.load_32bit_number())
                    else:
                        result.append(0);
            elif (tag >> 14) == 1: # non-zero
                length = tag - 0x4000 + 1
                for i in _range(length):
                    result.append(self.load_32bit_number())
            else: #zero
                length = tag + 1
                for i in _range(length):
                    result.append(0)
        return result

class BinaryOutput(object):
    def __init__(self):
        self._output = []
        self.outputBytes = 0;

    def dump_32bit_number(self, num):
        self._output.append(struct.pack('<I', num % (2 ** 32)))
        self.outputBytes += 4

    def dump_16bit_number(self, num):
        self._output.append(struct.pack('<H', num % (2 ** 16)))
        self.outputBytes += 2

    @staticmethod
    def convert_16bit_number(num):
        return struct.pack('<H', num % (2 ** 16))

    def dump_string(self, string):
        if type(string) is list:
            string = struct.pack('<%dH' % len(string), *string).decode("utf_16_le")
        converted_result = BinaryOutput.convert_string(string)
        self.outputBytes += len(converted_result)
        self._output.append(converted_result)

    @staticmethod
    def convert_string(string):
        result = []
        if len(string) > 32768:
            string = string[0:32768]
        length = len(string)
        byte_str = string.encode('utf_16_le')
        compress = True
        char_codes = []
        for i in _range(1, len(byte_str), 2):
            if byte_str[i] != b'\x00' and byte_str[i] != 0:
                compress = False
                break;
        if compress:
            result.append(BinaryOutput.convert_16bit_number(length + 32768))
            result.append(string.encode('latin-1'))
            if length % 2 == 1:
                result.append(b'\x00')
        else:
            result.append(BinaryOutput.convert_16bit_number(length))
            result.append(byte_str)
        return b"".join(result)

    def dump_raw_string(self, string):
        self._output.append(string)
        self.outputBytes += len(string)

    def dump_string_list(self, str_list):
        self.dump_32bit_number(len(str_list))
        for string in str_list:
            self.dump_string(string)

    def dump_string_list_map(self, str_map):
        self.dump_32bit_number(len(str_map))
        for key, value in str_map.items():
            self.dump_string(key)
            self.dump_string_list(value)

    def dump_32bit_number_list(self, array):
        self.dump_32bit_number(len(array))
        index = 0;
        input_length = len(array)
        while index < input_length:
            if array[index] == 0:
                length = self._count_zero(array, index)
                self._zero_block(length)
                index += length
            elif (self._should_zebra_code(array, index)):
                self._create_zebra_code(array, index)
                index = min(len(array), index + 15)
            else:
                length = self._search_double_zero(array, index)
                self._non_zero_block(array, index, length)
                if length == 0:
                    raise ValueError()
                index += length

    def _count_zero(self, array, offset):
        for i in _range(offset, len(array)):
            if array[i] != 0:
                return i - offset
        return len(array) - offset

    def _zero_block(self, length):
        while length > 0:
            if length > 16384:
                self.dump_16bit_number(16384 - 1)
                length -= 16384
            else:
                self.dump_16bit_number(length - 1)
                length = 0

    def _should_zebra_code(self, array, offset):
        if len(array) - offset < 16:
            return True
        change = 0
        is_last_zero = False
        for i in _range(offset, offset + 15):
            if array[i] == 0:
                if not is_last_zero:
                    is_last_zero = True
                    change += 1
            else:
                if is_last_zero:
                    is_last_zero = False
                    change += 1
        return change > 2

    def _search_double_zero(self, array, offset):
        is_last_zero = False;
        for i in _range(offset, len(array)):
            if array[i] == 0:
                if is_last_zero:
                    return i - offset - 1
                is_last_zero = True
            else:
                is_last_zero = False
        return len(array) - offset

    def _non_zero_block (self, array, offset, length):
        while length > 0:
            if length > 16384:
                block_length = 16384
                length -= 16384
            else:
                block_length = length
                length = 0
            self.dump_16bit_number((block_length - 1) + 0x4000)
            for i in _range(offset, offset + block_length):
                self.dump_32bit_number(array[i])
            offset += block_length

    def _create_zebra_code(self, array, offset):
        last = min(offset + 15, len(array))
        code = 0x8000
        temp_output = self._output
        index = len(self._output)
        for i in _range(offset, last):
            if array[i] != 0:
                self.dump_32bit_number(array[i]);
                code = code + (0x1 << (i - offset));
        self._output.insert(index, struct.pack('<H', code % (2 ** 16)))
        self.outputBytes += 2

    def result(self):
        return b''.join(self._output);
