from . sais import SAIS

_range = getattr(__builtins__, 'xrange', range)

class BWT(object):

    END_MARKER = chr(0)
    END_MARKER_CODE = 0

    def __init__(self, string, rawmode=False):
        self._rawmode = rawmode
        if rawmode:
            str2 = string + [0];
            self._str = str2;
            self._size = len(self._str)
            self._suffixarray = SAIS.make(str2, rawmode=True);
            self._head = self._suffixarray.index(0);
        else:
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
            size = self.size();
            chars = [self.get(i) for i in _range(size)]
            if self._rawmode:
                result = chars
                if replace is not None:
                    while BWT.END_MARKER_CODE in replace:
                        index = result.index(BWT.END_MARKER_CODE)
                        result[index] = replace
            else:
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
