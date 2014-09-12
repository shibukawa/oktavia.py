from . import bitvector
from . import binaryio


class Metadata(object):
    def __init__(self, parent, name):
        self._parent = parent
        self._bitVector = bitvector.BitVector()
        self._name = name

    def _size(self):
        return self._bitVector.rank(self._bitVector.size(), 1)

    def get_content(self, index):
        '''
        :param index: index
        :type  index: int
        '''
        if index < 0 or self._size() <= index:
            raise IndexError("Section.getContent() : range error %d" % index)
        startPosition = 0
        if index > 0:
            startPosition = self._bitVector.select(index - 1, 1) + 1
        length = self._bitVector.select(index, 1) - startPosition + 1
        return self._parent._get_substring(startPosition, length)

    def get_content_with_EOB(self, index):
        '''
        :param index: index
        :type  index: int
        '''
        if index < 0 or self._size() <= index:
            raise IndexError("Section.getContent() : range error %d" % index)
        
        startPosition = 0
        if index > 0:
            startPosition = self._bitVector.select(index - 1, 1) + 1
        
        length = self._bitVector.select(index, 1) - startPosition + 1
        return self._parent._get_substring_with_EOB(startPosition, length)

    def get_start_position(self, index):
        '''
        :param index: index
        :type  index: int
        '''
        if index < 0 or self._size() <= index:
            raise IndexError("Section.getContent() : range error %d" % index)
        
        startPosition = 0
        if index > 0:
            startPosition = self._bitVector.select(index - 1, 1) + 1
        
        return startPosition
    
    def grouping(self, result, positions, word, stemmed):
        '''
        :param result: result
        :type  result: SingleResult
        :param positions: positions
        :type  positions: int[]
        :param word: word
        :type  word: str
        :param stemmed: stemmed
        :type  stemmed: bool
        '''
        pass

    def get_information(self, index):
        '''
        :param index: index
        :type  index: int
        '''
        pass

    def _build(self):
        self._bitVector.build()

    def _load_parent(self, input):
        self._bitVector.load(input)
        self._parent._metadataLabels.append(self._name)
        self._parent._metadatas[self._name] = self

    def _dump(self, output):
        output.dump_string(self._name)
        self._bitVector.dump(output)
    

class Section(Metadata):
    TypeID = 0

    def __init__(self, parent, name):
        super(Section, self).__init__(parent, name)
        self._names = []
    
    def set_tail(self, name, index=None):
        '''
        :param name: name
        :type  name: str
        :param index: index
        :type  index: int
        '''
        if index is None:
            index = self._parent.content_size() - 1
        if self._parent._isLastEob:
            raise ValueError("Tail should not be 'eof' or 'eob'")
        self._names.append(name)
        self._bitVector.set(index, 1)

    def size(self):
        '''
        :return: section count
        :rtype: int
        '''
        return len(self._names)

    def get_section_index(self, position):
        '''
        :param position: position
        :type  position: int
        :return:
        :rtype: int
        '''
        if position < 0 or self._bitVector.size() <= position:
            raise IndexError("Section.getSectionIndex() : range error %d" % position)
        return self._bitVector.rank(position, 1)

    def get_name(self, index):
        '''
        :param index: index
        :type  index: int
        :return: name
        :rtype: str
        '''
        if index < 0 or self.size() <= index:
            raise IndexError("Section.getName() : range error")
        return self._names[index]

    def grouping(self, result, positions, word, stemmed):
        '''
        :param result: result
        :type  result: SingleResult
        :param positions: positions
        :type  positions: int[]
        :param word: word
        :type  word: str
        :param stemmed: stemmed
        :type  stemmed: bool
        '''
        for position in positions:
            index = self.getSectionIndex(position)
            unit = result.getSearchUnit(index)
            if unit.startPosition < 0:
                unit.startPosition = self.getStartPosition(index)
            unit.addPosition(word, position - unit.startPosition, stemmed)

    def get_information(self, index):
        '''
        :param index: index
        :type  index: int
        '''
        return self.getName(index)

    @staticmethod
    def _load(parent, input):
        name = input.load_string()
        section = Section(parent, name)
        section._load_parent(input)
        section._names = input.load_string_list()

    def _dump(self, output):
        output.dump_16bit_number(Section.TypeID)
        super(Section, self)._dump(output)
        output.dump_string_list(self._names)
    

class Splitter(Metadata):
    TypeID = 1

    def __init__(self, parent, name):
        super(Splitter, self).__init__(parent, name)

    def size(self):
        '''
        :return: section count
        :rtype: int
        '''
        return self._size()

    def split(self, index = None):
        '''
        :param index: index
        :type  index: int
        '''
        if index is None:
            index = self._parent.content_size() - 1
        if self._parent._isLastEob:
            raise ValueError("Tail should not be 'eof' or 'eob'")
        self._bitVector.set(index, 1)

    def get_index(self, position):
        '''
        :param position: position
        :type  position: int
        '''
        if position < 0 or self._bitVector.size() <= position:
            raise IndexError("Section.getSectionIndex() : range error")
        return self._bitVector.rank(position, 1)

    def grouping(self, result, positions, word, stemmed):
        '''
        :param result: result
        :type  result: SingleResult
        :param positions: positions
        :type  positions: int[]
        :param word: word
        :type  word: str
        :param stemmed: stemmed
        :type  stemmed: bool
        '''
        for position in positions:
            index = self.get_index(position)
            unit = result.get_search_unit(index)
            if unit.startPosition < 0:
                unit.startPosition = self.getStartPosition(index)
            unit.addPosition(word, position - unit.startPosition, stemmed)

    def get_information(self, index):
        '''
        :param index: index
        :type  index: int
        '''
        return "%s %d" % (self._name, index + 1)

    @staticmethod
    def _load(parent, input):
        name = input.load_string()
        section = Splitter(parent, name)
        section._load_parent(input)

    def _dump(self, output):
        output.dump_16bit_number(Splitter.TypeID)
        super(Splitter, self)._dump(output)


class Table(Metadata):
    TypeID = 2

    def __init__(self, parent, name, headers = None):
        super(Table, self).__init__(parent, name)
        if headers is not None:
            self._headers = headers
        self._columnTails = bitvector.BitVector()

    def row_size(self):
        return self._size()

    def column_size(self):
        return len(self._headers)

    def set_column_tail(self):
        index = self._parent.content_size()
        if self._parent._isLastEob:
            raise Error("Tail should not be 'eof' or 'eob'")
        self._columnTails.set(index, 1)

    def set_column_tail_and_EOB(self):
        self.set_column_tail()
        self._parent.add_end_of_block()

    def set_row_tail(self):
        index = self._parent.content_size() - 1
        self._bitVector.set(index, 1)
    
    def get_cell(self, position):
        if position < 0 or self._bitVector.size() <= position:
            raise IndexError("Section.getSectionIndex() : range error %d" % position)
        row = self._bitVector.rank(position, 1)
        currentColumn = self._columnTails.rank(position, 1)
        lastRowColumn = 0
        if row > 0:
            startPosition = self._bitVector.select(row - 1, 1) + 1
            lastRowColumn = self._columnTails.rank(startPosition, 1)
        result = [row, currentColumn - lastRowColumn]
        return result

    def get_row_content(self, rowIndex):
        content = self.get_content_with_EOB(rowIndex)
        values = content.split("\x01", len(self._headers))
        result = {}
        for i, header in enumerate(self._headers):
            if i < len(values):
                result[header] = values[i]
            else:
                result[header] = ''
        return result

    def grouping(self, result, positions, word, stemmed):
        '''
        :param result: result
        :type  result: SingleResult
        :param positions: positions
        :type  positions: int[]
        :param word: word
        :type  word: str
        :param stemmed: stemmed
        :type  stemmed: bool
        '''
        # TODO implement
        pass

    def get_information(self, index):
        '''
        :param index: index
        :type  index: int
        '''
        return ''

    def _build(self):
        self._bitVector.build()
        self._columnTails.build()

    @staticmethod
    def _load(parent, input):
        name = input.load_string()
        table = Table(parent, name)
        table._load_parent(input)
        table._headers = input.load_string_list()
        table._columnTails.load(input)

    def _dump(self, output):
        output.dump_16bit_number(Table.TypeID)
        super(Table, self)._dump(output)
        output.dump_string_list(self._headers)
        self._columnTails.dump(output)

class Block(Metadata):
    TypeID = 3

    def __init__(self, parent, name):
        super(Block, self).__init__(parent, name)
        self._names = []
        self._start = False

    def start_block(self, blockName, index = None):
        if index is None:
            index = self._parent.content_size() - 1
        if self._start:
            raise ValueError('Splitter `%s` is not closed' % self._names[-1])
        self._start = True
        self._names.append(blockName)
        self._bitVector.set(index, 1)

    def end_block(self, index=None):
        if index is None:
            index = self._parent.content_size() - 1
        if self._parent._isLastEob:
            raise ValueError("Block end should not be 'eof' or 'eob'")
        if not self._start:
            raise ValueError('Splitter is not started')
        self._start = False
        self._bitVector.set(index, 1)

    def size(self):
        '''
        :return: section count
        :rtype: int
        '''
        return len(self._names)

    def block_index(self, position):
        if position < 0 or (self._parent._fmindex.size() - 1) <= position:
            raise IndexError("Block.block_index() : range error %d" % position)
        if position >= self._bitVector.size():
            position = self._bitVector.size() - 1
            result = self._bitVector.rank(position, 1) + 1
        else:
            result = self._bitVector.rank(position, 1)
        return result

    def in_block(self, position):
        block_index = self.block_index(position)
        return (block_index % 2) != 0

    def get_block_content(self, position):
        block_index = self.block_index(position)
        if block_index % 2 != 0:
            result = self.get_content(block_index)
        else:
            result = ''
        return result

    def get_block_name(self, position):
        block_index = self.block_index(position)
        if block_index % 2 != 0:
            result = self._names[block_index >> 1]
        else:
            result = ''
        return result

    def get_information(self, index):
        '''
        :param index: index
        :type  index: int
        '''
        return ''

    @staticmethod
    def _load(parent, input):
        name = input.load_string()
        block = Block(parent, name)
        block._load_parent(input)
        block._names = input.load_string_list()

    def _dump(self, output):
        output.dump_16bit_number(Block.TypeID)
        super(Block, self)._dump(output)
        output.dump_string_list(self._names)
