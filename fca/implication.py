# -*- coding: utf-8 -*-
"""
Contains class for implications
"""

class Implication(object):
    """
    An Implication consists of two sets: *premise* and *conclusion*
    
    Examples
    ========
    
    >>> imp = Implication(set(('a', 'b',)), set(('c',)))
    >>> imp
    a, b => c
    >>> print imp
    a, b => c
    >>> imp.is_respected(set(('a', 'b',)))
    False
    >>> imp.is_respected(set(('a', 'b', 'd')))
    False
    >>> imp.is_respected(set(('a', 'b', 'c',)))
    True
    >>> imp.is_respected(set(('a', 'c',)))
    True
    >>> imp.is_respected(set(('b')))
    True
    >>> imp.is_respected(set(('c')))
    True
    """

    def __init__(self, premise = set(), conclusion = set()):
        """
        Create implication from two sets of attributes
        """
        self._premise = premise
        self._conclusion = conclusion
        
    def get_premise(self):
        """
        Return premise of implication
        """
        return self._premise
        
    def get_conclusion(self):
        """
        Return conclusion of implication
        """
        return self._conclusion
    
    premise = property(get_premise)
    conclusion = property(get_conclusion)
        
    def __repr__(self):
        premise = ", ".join([str(element) for element in self._premise])
        short_conclusion = self._conclusion - self._premise
        conclusion = ", ".join([str(element) for element in short_conclusion])
        return " => ".join((premise, conclusion,))
        
    def __cmp__(self, other):
        if ((self._premise == other.premise) and 
            (self._conclusion == other.conclusion)):
            return 0
        else:
            return -1
            
    def is_respected(self, some_set):
        """Checks whether *some_set* respects an implication or not"""
        # if some_set contains every element from premise and not every
        # element from conclusion then it doesn't respect an implication
        if (self.premise & some_set) == self.premise and \
           (self.conclusion & some_set) != self.conclusion:
            return False
        else:
            return True
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()