class Query(object):
    def __init__(self):
        self.word = ''
        self.OR = False
        self.NOT = False
        self.RAW = False

    def __str__(self):
        result = []
        if self.OR:
            result.push("OR ")
        if self.NOT:
            result.push("-")
        if self.RAW:
            result.push('"', self.word, '"')
        else:
            result.push(self.word)
        return ''.join(result)
