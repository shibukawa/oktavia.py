'''
Original source code:
*  G. Nong, S. Zhang and W. H. Chan, Two Efficient Algorithms for Linear Time Suffix Array Construction, IEEE Transactions on Computers, To Appear
* http:#www.cs.sysu.edu.cn/nong/index.files/Two%20Efficient%20Algorithms%20for%20Linear%20Suffix%20Array%20Construction.pdf
'''

from . bitvector import BitVector
import sys
_range = range if sys.version_info.major == 3 else xrange

class OArray(object):
    def __init__(self, array, offset = 0):
        self.array = array
        self.offset = offset

    def get(self, index):
        return self.array[index + self.offset]

    def set(self, index, value):
        self.array[index + self.offset] = value

    def isS(self, index):
        return self.array[index + self.offset] < self.array[index + self.offset + 1]

    def compare(self, index1, index2):
        return self.array[index1 + self.offset] == self.array[index2 + self.offset]

class SAIS(object):
    @staticmethod
    def _isLMS(t, i):
        return i > 0 and t.get(i) and not t.get(i - 1)

    @staticmethod
    def _getBuckets(s, bkt, n, K, end):
        '''find the start or end of each bucket'''
        sum = 0
        for i in _range(K + 1):
            bkt[i] = 0 # clear all buckets
        for i in _range(n):
            bkt[s.get(i)] += 1 # compute the size of each bucket
        for i in _range(K + 1):
            sum += bkt[i]
            bkt[i] = sum if end else sum - bkt[i]

    @staticmethod
    def _induceSAl(t, SA, s, bkt, n, K, end):
        # compute SAl
        SAIS._getBuckets(s, bkt, n, K, end) # find starts of buckets
        for i in _range(n):
            j = SA[i] - 1
            if j >= 0 and not t.get(j):
                index = s.get(j)
                SA[bkt[index]] = j
                bkt[index] += 1

    @staticmethod
    def _induceSAs(t, SA, s, bkt, n, K, end):
        # compute SAs
        SAIS._getBuckets(s, bkt, n, K, end) # find ends of buckets
        for i in _range(n - 1, -1, -1):
            j = SA[i] - 1
            if j >= 0 and t.get(j):
                index = s.get(j)
                bkt[index] -= 1
                SA[bkt[index]] = j

    @staticmethod
    def make(source, rawmode=False):
        '''
        find the suffix array SA of s[0..n-1] in 1..K^n
        require s[n-1]=0 (the sentinel!), n>=2
        use a working space (excluding s and SA) of at most 2.25n+O(1) for a constant alphabet
        '''
        if rawmode:
            charCodes = source
        else:
            charCodes = [ord(c) for c in source]
        
        SA = [0] * len(source)
        s = OArray(charCodes)
        SAIS._make(s, SA, len(source), max(charCodes))
        return SA

    @staticmethod
    def _make(s, SA, n, K):
        # Classify the type of each character
        t = BitVector()
        t.set(n - 2, False)
        t.set(n - 1, True) # the sentinel must be in s1, important!!!
        for i in _range(n - 3, -1, -1):
            t.set(i, s.isS(i) or (s.compare(i, i + 1) and t.get(i + 1)))
        # stage 1: reduce the problem by at least 1/2
        # sort all the S-substrings
        bkt = [0] * (K + 1)
        SAIS._getBuckets(s, bkt, n, K, True) # find ends of buckets
        for i in _range(n):
            SA[i] = -1
        for i in _range(1, n):
            if SAIS._isLMS(t, i):
                index = s.get(i)
                bkt[index] -= 1
                SA[bkt[index]] = i
        SAIS._induceSAl(t, SA, s, bkt, n, K, False)
        SAIS._induceSAs(t, SA, s, bkt, n, K, True)
        # compact all the sorted substrings into the first n1 items of SA
        # 2*n1 must be not larger than n (proveable)
        n1 = 0
        for i in _range(n):
            if SAIS._isLMS(t, SA[i]):
                SA[n1] = SA[i]
                n1 += 1

        # find the lexicographic names of all substrings
        for i in _range(n1, n):
            SA[i]=-1 # init the name array buffer
        
        name = 0
        prev = -1
        for i in _range(n1):
            pos = SA[i]
            diff = False
            for d in _range(n):
                if prev == -1 or not s.compare(pos + d, prev + d) or t.get(pos + d) != t.get(prev + d):
                    diff = True
                    break
                elif d > 0 and (SAIS._isLMS(t, pos+d) or SAIS._isLMS(t, prev + d)):
                    break
            if diff:
                name += 1
                prev = pos
            pos = pos // 2 if (pos % 2 == 0) else (pos - 1) // 2
            SA[n1 + pos] = name - 1
       
        j = n - 1
        for i in _range(n - 1, n1 - 1, -1):
            if SA[i] >= 0:
                SA[j] = SA[i]
                j -= 1
        # stage 2: solve the reduced problem
        # recurse if names are not yet unique
        SA1 = SA
        s1 = OArray(SA, n - n1)
        if name < n1:
            SAIS._make(s1, SA1, n1, name - 1)
        else:
            # generate the suffix array of s1 directly
            for i in _range(n1):
                SA1[s1.get(i)] = i
        # stage 3: induce the result for the original problem
        bkt = [0] * (K + 1)
        # put all left-most S characters into their buckets
        SAIS._getBuckets(s, bkt, n, K, True) # find ends of buckets
        j = 0
        for i in _range(n):
            if SAIS._isLMS(t, i):
                s1.set(j, i) # get p1
                j += 1
        for i in _range(n1):
            SA1[i] = s1.get(SA1[i]) # get index in s
        for i in _range(n1, n):
            SA[i] = -1 # init SA[n1..n-1]
        for i in _range(n1 - 1, -1, -1):
            j = SA[i]
            SA[i] = -1
            index = s.get(j)
            bkt[index] -= 1
            SA[bkt[index]] = j
        SAIS._induceSAl(t, SA, s, bkt, n, K, False)
        SAIS._induceSAs(t, SA, s, bkt, n, K, True)

