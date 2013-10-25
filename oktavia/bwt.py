from . sais import SAIS

class BWT(object):

    END_MARKER = chr(0)

    def __init__(self, string):
        str2 = string + BWT.END_MARKER;
        self._str = str2;
        self._size = len(self._str)
        self._suffixarray = SAIS.make(str2);
        self._head = self._suffixarray.index(0);

    def size(self):
        return self._size;

    def head(self):
        return self._head;

    def clear(self):
        self._str = "";
        self._size = 0;
        self._head = 0;
        del self._suffixarray[:]

    def get(self, i = None, replace = None):
        if i is None:
            chars = []
            size = self.size();
            for i in range(size):
                chars.append(self.get(i));
            result = ''.join(chars)
            if replace is not None:    
                result = result.replace(BWT.END_MARKER, replace);
        else:
            size = self.size();
            if i >= size:
                raise RangeError("BWT.get() : range error");
            index = (self._suffixarray[i] + size - 1) % size;
            result = self._str[index];
        return result

def bwt(string, endMarker=None):
    bwt = BWT(string);
    return bwt.get(replace=endMarker)
