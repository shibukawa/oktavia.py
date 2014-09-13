'''
This is a Python version of shellinford library:
https:#code.google.com/p/shellinford/

License: http:#shibu.mit-license.org/
'''

import math
import struct

from . import waveletmatrix
from . import bwt
from . import binaryio

try:
    _range = xrange
except NameError:
    _range = range

try:
    _strtype = basestring
except NameError:
    _strtype = str

class FMIndex(object):
    def __init__(self, rawmode = False):
        self._ddic = 0
        self._head = 0
        self._substr = []
        self._sv = waveletmatrix.WaveletMatrix()
        self._posdic = []
        self._idic = []
        self._rlt = [0] * 65536
        self._build = False
        self._rawmode = rawmode

    def clear(self):
        self._sv.clear()
        del self._posdic[:]
        del self._idic[:]
        self._ddic = 0
        self._head = 0
        self._rlt = [0] * 65536
        del self._substr[:]

    def size(self):
        return self._sv.size()
    
    def content_size(self):
        return sum((len(s) for s in self._substr))

    def rank(self, pos, code):
        return self._sv.rank(pos, code)

    def get(self, pos):
        return self._sv.get(pos)

    def get_rows(self, key, pos=None):
        import sys
        if isinstance(key, _strtype):
            # convert to JavaScript compatible string
            rawstring = key.encode('utf_16_le')
            key = struct.unpack("<%dH" % len(key), rawstring)
        i = len(key) - 1
        c = key[i]
        first = self._rlt[c] + 1
        last  = self._rlt[c + 1]
        while first <= last:
            if i == 0:
                if pos is not None:
                    first -= 1
                    last -= 1
                    del pos[:]
                    pos.append(first)
                    pos.append(last)
                return (last - first  + 1)
            i -= 1
            c = key[i]
            first = self._rlt[c] + self._sv.rank(first - 1, c) + 1
            last  = self._rlt[c] + self._sv.rank(last,      c)
        return 0

    def get_position(self, i):
        if i >= self.size():
            raise RangeError("FMIndex.get_position() : range error")
        pos = 0
        while i != self._head:
            if (i % self._ddic) == 0:
                pos += (self._posdic[i // self._ddic] + 1)
                break
            c = self._sv.get(i)
            i = self._rlt[c] + self._sv.rank(i, c) #LF
            pos += 1
        return pos % self.size()

    def _join(self):
        if self._rawmode:
            doc = []
            for substr in self._substr:
                doc = doc + substr
        else:
            doc = "".join(self._substr)
        return doc

    def get_substring(self, pos, length):
        if not self._build:
            doc = self._join()
            return doc[pos : pos + length]

        if pos >= self.size():
            raise RangeError("FMIndex.get_substring() : range error")
        pos_end = min(pos + length, self.size())
        pos_tmp = self.size() - 1
        i = self._head
        pos_idic = (pos_end + self._ddic - 2) // self._ddic
        if pos_idic < len(self._idic):
            pos_tmp = pos_idic * self._ddic
            i = self._idic[pos_idic]
        codes = []
        while pos_tmp >= pos:
            c = self.get(i)
            i = self._rlt[c] + self.rank(i, c) #LF
            if pos_tmp < pos_end and c != 0:
                codes.insert(0, c)
            if pos_tmp == 0:
                break
            pos_tmp -= 1

        if self._rawmode:
            return codes
        return struct.pack('<%dH' % len(codes), *codes).decode('utf_16_le')

    def build(self, ddic, maxChar=65535):
        doc = self._join()
        sa = bwt.BWT(doc, rawmode=self._rawmode)
        s = sa.get()
        self._ssize = len(s)
        self._head = sa.head()
        del self._substr[:]
        self._sv.set_max_char_code(maxChar)
        self._sv.build(s)
        size = self.size()
        for c in _range(maxChar):
            self._rlt[c] = self._sv.rank_less_than(size, c)
        self._rlt[maxChar] = 0;
        self._ddic = int(ddic)
        self._buildDictionaries()
        self._build = True

    def _buildDictionaries(self):
        del self._posdic[:]
        del self._idic[:]
        for i in _range(self._ssize // self._ddic + 1):
            self._posdic.append(0)
            self._idic.append(0)
        i = self._head
        pos = self.size() - 1

        if (i % self._ddic) == 0:
            self._posdic[i // self._ddic] = pos
        if (pos % self._ddic) == 0:
            self._idic[pos // self._ddic] = i
        c = self._sv.get(i)
        i = self._rlt[c] + self._sv.rank(i, c) #LF
        pos -= 1
        while i != self._head:
            if (i % self._ddic) == 0:
                self._posdic[i // self._ddic] = pos
            if (pos % self._ddic) == 0:
                self._idic[pos // self._ddic] = i
            c = self._sv.get(i)
            i = self._rlt[c] + self._sv.rank(i, c) #LF
            pos -= 1

    def append(self, doc):
        if len(doc) == 0:
            raise ValueError("FMIndex::append(): empty string")
        self._substr.append(doc)

    def search(self, keyword):
        result = []
        position = []
        rows = self.get_rows(keyword, position)
        if rows > 0:
            first = position[0]
            last = position[1]
            for i in _range(first, last + 1):
                result.append(self.get_position(i))
        return result

    def dump(self, output):
        output.dump_32bit_number(self._ddic)
        output.dump_32bit_number(self._ssize)
        output.dump_32bit_number(self._head)
        self._sv.dump(output)
        output.dump_32bit_number(len(self._posdic))
        for v in self._posdic:
            output.dump_32bit_number(v)
        for v in self._idic:
            output.dump_32bit_number(v)

    def load(self, input):
        self.clear()
        self._ddic = int(input.load_32bit_number())
        self._ssize = input.load_32bit_number()
        self._head = input.load_32bit_number()
        self._sv.load(input)
        maxChar = self._sv.max_char_code()
        size = self._sv.size()
        self._rlt = []
        for c in _range(maxChar):
            self._rlt.append(self._sv.rank_less_than(size, c))
        self._rlt.append(0)
        size = input.load_32bit_number()
        del self._posdic[:]
        del self._idic[:]
        for i in _range(size):
            self._posdic.append(input.load_32bit_number())
        for i in _range(size):
            self._idic.append(input.load_32bit_number())
        self._build = True

