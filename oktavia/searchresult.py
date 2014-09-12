class Proposal(object):
    def __init__(self, omit, expect):
        self.omit = omit
        self.expect = expect


class Position(object):
    def __init__(self, word, position, stemmed):
        self.word = word
        self.position = position
        self.stemmed = stemmed


class SearchUnit(object):
    def __init__ (self, id):
        self.positions = {}
        self.id = id
        self._size = 0
        self.score = 0
        self.startPosition = -1

    def add_position(self, word, position, stemmed):
        if position not in self.positions: 
            self._size += 1
            self.positions[position] = Position(word, position, stemmed)
        else:
            positionObj = self.positions[position]
            if len(positionObj.word) < len(word):
                positionObj.word = word
            positionObj.stemmed = positionObj.stemmed and stemmed

    def get(self, position):
        return self.positions[position]

    def __len__(self):
        return self._size

    def merge(self, rhs):
        for pos in rhs.positions:
            self.addPosition(pos.word, pos.position, pos.stemmed)

    def get_positions(self):
        result = []
        for pos in self.positions:
            result.append(pos)
        result.sort(key=lambda a: -a.position)
        return result


class SingleResult(object):
    def __init__(self, searchWord='', OR=False, NOT=False):
        self.units = []
        self.unitIds = []
        self.OR = OR
        self.NOT = NOT
        self.searchWord = searchWord

    def get_search_unit(self, unitId):
        if unitId not in self.unitIds:
            result = SearchUnit(unitId)
            self.units.append(result)
            self.unitIds.append(unitId)
        else:
            result = self.units[self.unitIds.index(unitId)]
        return result

    def merge(self, rhs):
        result = SingleResult()
        if rhs.OR:
            self._orMerge(result, rhs)
        elif rhs.NOT:
            self._notMerge(result, rhs)
        else:
            self._andMerge(result, rhs)
        return result

    def __len__(self):
        return len(self.units)

    def _andMerge(self, result, rhs):
        for i, id in enumerate(self.unitIds):
            if id in rhs.unitIds:
                lhsSection = self.units[i]
                result.unitIds.append(id)
                result.units.append(lhsSection)

    def _orMerge(self, result, rhs):
        result.unitIds = self.unitIds[:]
        result.units = self.units[:]

        for i, id in enumerate(rhs.unitIds):
            rhsSection = rhs.units[i]
            if id in result.unitIds:
                lhsSection = result.units[result.unitIds.index(id)]
                lhsSection.merge(rhsSection)
            else:
                result.unitIds.append(id)
                result.units.append(rhsSection)

    def _notMerge(self, result, rhs):
        for i, id in enumerate(self.unitIds):
            if id not in rhs.unitIds:
                lhsSection = self.units[i]
                result.unitIds.append(id)
                result.units.append(lhsSection)


class SearchSummary(object):
    def __init__ (self, oktavia=None):
        self.sourceResults = []
        self.result = None
        self.oktavia = oktavia

    def add_query(self, result):
        self.sourceResults.append(result)

    def merge_result(self, results=None):
        if results is None:
            self.result = self.merge_result(self.sourceResults)
        else:
            rhs = results[0]
            for result in results:
                rhs = rhs.merge(result)
            return rhs

    def get_proposals(self):
        proposals = []
        for i in range(len(self.sourceResults)):
            tmpSource = []
            for j in range(len(self.sourceResults)):
                if i != j:
                    tmpSource.append(self.sourceResults[j])
            result = self.merge_result(tmpSource)
            proposals.append(Proposal(i, len(result)))
        
        proposals.sort(key=lambda a: -a.expect)
        return proposals

    def get_sorted_result(self):
        result = self.result.units[:]
        result.sort(key=lambda a: -a.score)
        return result

    def __len__(self):
        return len(self.result)

    def add(self, result):
        self.sourceResults.append(result)
