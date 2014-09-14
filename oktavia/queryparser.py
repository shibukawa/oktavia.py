import re
from .query import Query

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

class QueryParser(object):
    def highlight(self):
        '''
        :rtype: string
        '''
        result = []
        for query in self.queries:
            if not query.NOT:
                result.append(("highlight", query.word))
        return '?' + urlencode(result)


class QueryListParser(QueryParser):
    def __init__(self):
        self.queries = []

    def parse(self, queryStrings):
        '''
        :param queryStrings: query
        :type  queryStrings: str[]
        :return: parsed query
        :rtype: Query[]
        '''
        nextOr = False
        for word in queryStrings:
            if word == 'OR':
                nextOr = True
            else:
                query = Query()
                if nextOr:
                    query.OR = True
                    nextOr = False
                if word.startswith('-'):
                    query.NOT = True
                    word = word[1:]
                if word.startswith('"') and word.endswith('"'): 
                    query.RAW = True
                    word = word[1:-1]
                query.word = word
                self.queries.append(query)
        return self.queries;


class QueryStringParser(QueryParser):
    def __init__(self):
        self.queries = []

    def parse(self, queryString):
        '''
        :param queryString: query
        :type  queryString: str
        return: parsed query
        :rtype: Query[]
        '''
        nextOr = False
        nextNot = False
        currentWordStart = 0
        status = 0
        # 0: free
        # 1: in unquoted word
        # 2: in quote
        isSpace = re.compile(r"[\s\u3000]")
        for i, ch in enumerate(queryString):
            if status ==  0: # free
                if not isSpace.match(ch):
                    if ch == '-':
                        nextNot = True
                    elif ch == '"':
                        currentWordStart = i + 1
                        status = 2
                    else:
                        currentWordStart = i
                        status = 1
                else:
                    nextNot = False
            elif status == 1: # unquoted word
                if isSpace.match(ch):
                    word = queryString[currentWordStart:i]
                    if word == 'OR':
                        nextOr = True
                    else:
                        query = Query()
                        query.word = word
                        query.OR = nextOr
                        query.NOT = nextNot
                        self.queries.append(query)
                        nextOr = False
                        nextNot = False
                    status = 0
            elif status == 2: # in quote
                if ch == '"':
                    word = queryString[currentWordStart:i]
                    query = Query()
                    query.word = word
                    query.OR = nextOr
                    query.NOT = nextNot
                    query.RAW = True
                    self.queries.append(query)
                    nextOr = False
                    nextNot = False
                    status = 0
        if status == 1: 
            query = Query()
            word = queryString[currentWordStart:len(queryString)]
            if word != 'OR':
                query.word = word
                query.OR = nextOr
                query.NOT = nextNot
                self.queries.append(query)
        elif status == 2:
            query = Query()
            query.word = queryString[currentWordStart:currentWordStart + len(queryString)]
            query.OR = nextOr
            query.NOT = nextNot
            query.RAW = True
            self.queries.append(query)
        
        return self.queries
