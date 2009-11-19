# -*- coding: utf-8 -*-
"""Holds ConceptSystem class"""

from concept import Concept

class ConceptSystem(object):
    """A ConceptSystem class contains a set of concepts

    Emulates container
    
    Examples
    ========

    >>> cs = ConceptSystem()
    >>> c = Concept([1, 2], ['a', 'b'])
    >>> cs.append(c)
    >>> c in cs
    True
    >>> Concept([1], ['c']) in cs
    False
    >>> cs.append(3.1415926535897931)
    Traceback (most recent call last):
        ...
    TypeError: concept must be an instance of the Concept class
    >>> print cs
    ([1, 2], ['a', 'b'])

    """

    def __init__(self, concepts=[]):
        self._concepts = concepts[:]

    def __len__(self):
        return len(self._concepts)

    def __getitem__(self, key):
        return self._concepts[key]

    def __contains__(self, value):
        return value in self._concepts

    def __str__(self):
        s = ""
        for c in self._concepts:
            s = s + "%s\n" % str(c)
        return s[:-1]

    def append(self, concept):
        if isinstance(concept, Concept):
            self._concepts.append(concept)
        else:
            raise TypeError("concept must be an instance of the Concept class")

    def index(self, concept):
        return self._concepts.index(concept)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
