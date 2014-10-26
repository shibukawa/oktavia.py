'''
This is a JSX version of shellinford library:
https://code.google.com/p/shellinford/

License: http://shibu.mit-license.org/
'''

import sys
import copy
import math
import struct

from . import binaryio
from . import bitvector

try:
    from . import _bitvector as native_bitvector
except ImportError:
    native_bitvector = None

_range = range if sys.version_info[0] == 3 else xrange

class WaveletMatrix(object):

    def __init__(self):
        self._range = {}
        self._bv = []
        self._seps = []
        self._maxcharcode = 65535
        self._bitsize = 16
        self._usedChars = set()
        self.clear()

    def bitsize(self):
        return self._bitsize

    def set_max_char_code(self, char_code):
        self._maxcharcode = char_code
        self._bitsize = int(math.ceil(math.log(self._maxcharcode) / math.log(2)))

    def max_char_code(self):
        return self._maxcharcode

    def clear(self):
        del self._bv[:]
        del self._seps[:]
        self._size = 0

    def usedChars(self):
        return self._usedChars

    def build(self, v):
        self.clear()
        size = len(v)
        if isinstance(v, str):
            # convert to JavaScript compatible string
            rawstring = v.encode('utf_16_le')
            v = struct.unpack("<%dH" % size, rawstring)
        self._usedChars = set(v)
        bitsize = self.bitsize()
        for i in _range(bitsize):
            if native_bitvector:
                self._bv.append(native_bitvector.BitVector())
            else:
                self._bv.append(bitvector.BitVector())
            self._seps.append(0)
        self._size = size
        for i, c in enumerate(v):
            self._bv[0].set(i, self._uint2bit(c, 0, bitsize))
        self._bv[0].build()
        self._seps[0] = self._bv[0].size0()
        self._range[0] = 0
        self._range[1] = self._seps[0]

        depth = 1
        while depth < bitsize:
            range_tmp = copy.copy(self._range)
            for i, code in enumerate(v):
                bit = self._uint2bit(code, depth, bitsize)
                key = code >> (bitsize - depth)
                self._bv[depth].set(range_tmp[key], bit)
                range_tmp[key] += 1
            self._bv[depth].build()
            self._seps[depth] = self._bv[depth].size0()

            range_rev = {}
            for range_key, value in self._range.items():
                if value != range_tmp[range_key]:
                    range_rev[value] = range_key
            self._range = {}
            pos0 = 0
            pos1 = self._seps[depth]
            for begin, value in sorted(range_rev.items()):
                end = range_tmp[value]
                num0  = self._bv[depth].rank(end, False) - self._bv[depth].rank(begin, False)
                num1  = end - begin - num0
                if num0 > 0:
                    self._range[value << 1] = pos0
                    pos0 += num0
                if num1 > 0:
                    self._range[(value << 1) + 1] = pos1
                    pos1 += num1
            depth += 1

    def size(self):
        return self._size
    
    def count(self, c):
        return self.rank(self.size(), c)
    
    def get(self, i):
        if i >= self.size():
            raise RangeError("WaveletMatrix.get() : range error")
        value = 0
        depth = 0
        bitsize = self.bitsize()
        while depth < bitsize:
            bit = self._bv[depth].get(i)
            i = self._bv[depth].rank(i, bit)
            value <<= 1
            if bit:
                i += self._seps[depth]
                value += 1
            depth += 1
        return value

    def rank(self, i, c):
        if i > self.size():
            raise RangeError("WaveletMatrix.rank(): range error")
        if i == 0:
            return 0
        begin = self._range.get(c)
        if begin == None:
            return 0
        end   = i
        depth = 0
        bitsize = self.bitsize()
        while depth < bitsize:
            bit = self._uint2bit(c, depth, bitsize)
            end = self._bv[depth].rank(end, bit)
            if bit:
                end += self._seps[depth]
            depth += 1
        return end - begin
    
    def rank_less_than(self, i, c):
        if i > self.size():
            raise RangeError("WaveletMatrix.rank_less_than(): range error")
        if i == 0:
            return 0
        begin = 0
        end   = i
        depth = 0
        rlt   = 0
        bitsize = self.bitsize()
        while depth < bitsize:
            rank0_begin = self._bv[depth].rank(begin, False)
            rank0_end   = self._bv[depth].rank(end,   False)
            if self._uint2bit(c, depth, bitsize):
                rlt += (rank0_end - rank0_begin)
                begin += (self._seps[depth] - rank0_begin)
                end   += (self._seps[depth] - rank0_end)
            else:
                begin = rank0_begin
                end   = rank0_end
            depth += 1
        return rlt
    
    def dump(self, output):
        output.dump_16bit_number(self._maxcharcode)
        output.dump_16bit_number(self.bitsize())
        output.dump_32bit_number(self._size)
        for i in _range(self.bitsize()):
            if native_bitvector:
                output.dump_32bit_number(self._bv[i].size())
                output.dump_32bit_number_list(self._bv[i].int32vector())
            else:
                self._bv[i].dump(output)
        for i in _range(self.bitsize()):
            output.dump_32bit_number(self._seps[i])
        output.dump_32bit_number(len(self._range))
        for key, value in self._range.items():
            output.dump_32bit_number(key)
            output.dump_32bit_number(value)

    def load(self, input):
        self.clear()
        self._maxcharcode = input.load_16bit_number()
        self._bitsize = input.load_16bit_number()
        self._size = input.load_32bit_number()
        for i in _range(self.bitsize()):
            bit_vector = bitvector.BitVector()
            bit_vector.load(input)
            self._bv.append(bit_vector)
        for i in _range(self.bitsize()):
            self._seps.append(input.load_32bit_number())
        range_size = input.load_32bit_number()
        for i in _range(range_size):
            key = input.load_32bit_number()
            value = input.load_32bit_number()
            self._range[key] = value

    def _uint2bit(self, c, i, bitsize):
        return ((c >> (bitsize - 1 - i)) & 0x1) == 0x1

