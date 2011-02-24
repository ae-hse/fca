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
        
    def __repr__(self):
        premise = ", ".join([str(element) for element in self._premise])
        conclusion = ", ".join([str(element) for element in self._conclusion])
        return " => ".join((premise, conclusion,))
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()