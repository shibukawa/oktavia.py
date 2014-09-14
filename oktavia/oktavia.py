import re
import math
import struct
import snowballstemmer
from . import fmindex
from . import binaryio
from . import query
from . import searchresult
from . import metadata

if hasattr(__builtins__, 'unichr'):
    tostr = unichr
else:
    tostr = chr

wordsplitter = re.compile(r'\s')
wordsplitter2 = re.compile(r'\W')

def to_utf16(string):
    binary = string.encode('utf-16le')
    return struct.unpack("%dH" % len(string), binary)

def from_utf16(codes):
    return struct.pack("%dH" % len(codes), *codes).decode('utf-16le')

class Oktavia(object):
    # sentinels
    eof = 0
    eob = 1
    unknown = 2

    # Enum
    USE_STEMMING = True

    def __init__(self):
        self._fmindex = fmindex.FMIndex(rawmode=True)
        self._metadatas = {}
        self._metadataLabels = []
        self._stemmer = None
        self._stemmingResult = {}
        self._build = False
        self._isLastEob = False
        self._utf162compressCode = {Oktavia.eof: 0, Oktavia.eob: 1, Oktavia.unknown: 2}
        self._compressCode2utf16 = [Oktavia.eof, Oktavia.eob, Oktavia.unknown]

    def set_stemmer(self, stemmer):
        self._stemmer = stemmer

    def get_primary_metadata(self):
        return self._metadatas[self._metadataLabels[0]]

    def add_section(self, key):
        if key in self._metadataLabels:
            raise ValueError('Metadata name ' + key + ' is already exists')
        self._metadataLabels.append(key)
        section = metadata.Section(self, key)
        self._metadatas[key] = section
        return section

    def get_section(self, key):
        if key not in self._metadataLabels:
            raise ValueError('Metadata name ' + key + " does't exists")
        return self._metadatas[key]

    def add_splitter(self, key):
        if key in self._metadataLabels:
            raise ValueError('Metadata name ' + key + ' is already exists')
        self._metadataLabels.append(key)
        splitter = metadata.Splitter(self, key)
        self._metadatas[key] = splitter
        return splitter

    def get_splitter(self, key):
        if key not in self._metadataLabels:
            raise ValueError('Metadata name ' + key + " does't exists")
        return self._metadatas[key]

    def add_table(self, key, headers):
        if key in self._metadataLabels:
            raise ValueError('Metadata name ' + key + ' is already exists')
        self._metadataLabels.append(key)
        table = metadata.Table(self, key, headers)
        self._metadatas[key] = table
        return table

    def get_table(self, key):
        if key not in self._metadataLabels:
            raise ValueError('Metadata name ' + key + " does't exists")
        return self._metadatas[key]

    def add_block(self, key):
        if key in self._metadataLabels:
            raise ValueError('Metadata name ' + key + ' is already exists')
        self._metadataLabels.append(key)
        block = metadata.Block(self, key)
        self._metadatas[key] = block
        return block

    def get_block(self, key):
        if key not in self._metadataLabels:
            raise ValueError('Metadata name ' + key + " does't exists")
        return self._metadatas[key]

    def add_end_of_block(self):
        self._fmindex.append([Oktavia.eob])
        self._isLastEob = True

    def add_word(self, word, stemming=None):
        word.encode
        string = []
        utf16word = to_utf16(word)
        for charCode in utf16word:
            if charCode not in self._utf162compressCode:
                convertedChar = len(self._compressCode2utf16)
                self._utf162compressCode[charCode] = convertedChar
                self._compressCode2utf16.append(charCode)
            else:
                convertedChar = self._utf162compressCode[charCode]
            string.append(convertedChar)
        self._fmindex.append(string)
        self._isLastEob = utf16word[-1] < 2

        if stemming is None:
            return

        wordList = wordsplitter.split(word)
        for originalWord in wordList:
            smallWord = originalWord[0:1].lower() + originalWord[1:]
            registerWord = None
            if stemming and self._stemmer:
                baseWord = self._stemmer.stemWord(originalWord.lower())
                if baseWord not in originalWord:
                    registerWord = baseWord
            elif originalWord != smallWord:
                registerWord = smallWord
            if registerWord:
                compressedCodeWord = self._convertToCompressionCode(originalWord)
                if registerWord not in self._stemmingResult:
                    stemmedList = [compressedCodeWord]
                    self._stemmingResult[registerWord] = stemmedList
                else:
                    stemmedList = self._stemmingResult[registerWord]
                    if compressedCodeWord not in stemmedList:
                        stemmedList.append(compressedCodeWord)

    def _convertToCompressionCode(self, keyword):
        resultChars = []
        if type(keyword) is not list:
            keyword = to_utf16(keyword)
        for originalChar in keyword:
            if originalChar not in self._utf162compressCode:
                resultChars.append("\x02")
            else:
                char = self._utf162compressCode[originalChar]
                resultChars.append(char)
        return resultChars

    def raw_search(self, keyword, stemming=False):
        if not self._build:
            raise RuntimeError("Oktavia.build() is not called yet")
        if stemming:
            result = []
            if self._stemmer:
                baseWord = self._stemmer.stemWord(keyword.lower())
                if baseWord in self._stemmingResult:
                    stemmedList = self._stemmingResult[baseWord]
                    for word in stemmedList:
                        result += self._fmindex.search(word)
        else:
            result = self._fmindex.search(self._convertToCompressionCode(keyword))
        return result

    def search(self, queries):
        if not self._build:
            raise RuntimeError("Oktavia.build() is not called yet")
        summary = searchresult.SearchSummary(self)
        for query in queries:
            summary.add_query(self._searchQuery(query))
        summary.merge_result()
        return summary

    def _searchQuery(self, query):
        result = searchresult.SingleResult(query.word, query.OR, query.NOT)
        if query.RAW:
            positions = self.raw_search(query.word, False)
        else:
            positions = self.raw_search(query.word, False) + (self.raw_search(query.word, True))
        self.get_primary_metadata().grouping(result, positions, query.word, not query.RAW)
        return result

    def build(self, cacheDensity=5):
        if self._build:
            raise RuntimeError("Oktavia.build() is already called")
        for key in self._metadatas:
            self._metadatas[key]._build()
        maxCharCode = len(self._compressCode2utf16)
        cacheRange = round(max(1, (100 / min(100, max(0.01, cacheDensity)))))
        self._fmindex.build(cacheRange, maxCharCode)
        self._build = True

    def dump(self, verbose=False):
        if not self._build:
            raise RuntimeError("Oktavia.build() is not called yet")
        output = binaryio.BinaryOutput()
        headerSource = u"oktavia-02"
        output.dump_raw_string(binaryio.BinaryOutput.convert_string(headerSource)[2:])
        if verbose:
            print('Source text size: %d bytes' % (self._fmindex.size() * 2))
        self._fmindex.dump(output)
        output.dump_string(self._compressCode2utf16[3:])
        if verbose:
            print('Char Code Map: %d bytes' % (len(self._compressCode2utf16) * 2 - 2))
        size = output.outputBytes
        output.dump_string_list_map(self._stemmingResult)
        if verbose:
            print('Stemmed Word Table: %d bytes' % (output.outputBytes - size) * 2)

        output.dump_16bit_number(len(self._metadataLabels))
        for name in self._metadataLabels:
            size = output.outputBytes
            self._metadatas[name]._dump(output)
            if verbose:
                print('Meta Data %s: %d bytes' % (name, output.outputBytes - size) * 2)
        return output.result()

    def load(self, data):
        headerSource = u"oktavia-02"
        header = binaryio.BinaryOutput.convert_string(headerSource)[2:]
        if data[0:10] != header:
            raise ValueError('Invalid data file')
        input = binaryio.BinaryInput(data, 10)
        self._metadatas = {}
        self._metadataLabels = []

        self._fmindex.load(input)
        charCodes = input.load_string()
        self._utf162compressCode = {Oktavia.eof: 0, Oktavia.eob: 1, Oktavia.unknown: 2}
        self._compressCode2utf16 = [Oktavia.eof, Oktavia.eob, Oktavia.unknown]

        for i, charCode in enumerate(to_utf16(charCodes)):
            self._compressCode2utf16.append(charCode)
            self._utf162compressCode[charCode] = i + 3

        self._stemmingResult = input.load_string_list_map()

        metadataCount = input.load_16bit_number()
        for i in range(metadataCount):
            typecode = input.load_16bit_number()
            if typecode == metadata.Section.TypeID:
                metadata.Section._load(self, input)
            elif typecode == metadata.Splitter.TypeID:
                metadata.Splitter._load(self, input)
            elif typecode == metadata.Table.TypeID:
                metadata.Table._load(self, input)
            elif typecode == metadata.Block.TypeID:
                metadata.Block._load(self, input)
            else:
                raise TypeError("Metadata TypeError: %d" % type)
        self._build = True

    def content_size(self):
        return self._fmindex.content_size()

    def word_position_type(self, position):
        result = 0
        if position == 0:
            result = 4
        else:
            ahead = self._fmindex.get_substring(position - 1, 1)
            if wordsplitter.match(ahead):
                result = 2
            elif wordsplitter2.match(ahead):
                result = 1
            elif Oktavia.eob == ahead:
                result = 3
        return result

    def _get_substring(self, position, length):
        codes = self._fmindex.get_substring(position, length)
        result = [] 
        for code in codes:
            if code > 2:
                result.append(self._compressCode2utf16[code])
        return from_utf16(result)

    def _get_substring_with_EOB(self, position, length):
        result = self._fmindex.get_substring(position, length)
        str = []
        for code in result:
            if code > 2:
                str.append(self._compressCode2utf16[code])
            elif code == 1:
                str.append(1)
        return from_utf16(str)
