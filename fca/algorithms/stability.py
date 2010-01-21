#!/usr/bin/env python
# encoding: utf-8
"""
stability.py

Created by Nikita Romashkin on 2010-01-19.

"""

from copy import copy

def compute_stability(lattice):
    """
    Examples
    ========

    >>> from fca import *
    >>> ct = [[True, False, False, True],\
              [True, False, True, False],\
              [False, True, True, False],\
              [False, True, True, True]]
    >>> objs = [1, 2, 3, 4]
    >>> attrs = ['a', 'b', 'c', 'd']
    >>> c = Context(ct, objs, attrs)
    >>> cs = norris(c)
    >>> st = compute_stability(cs)
    >>> print st

    """
    concepts = copy(lattice)
    count = {}
    subsets = {}
    stability = {}

    for concept in concepts:
        count[concept] = len([c for c in concepts if c.extent < concept.extent])
        subsets[concept] = 2 ** len(concept.extent)
    while not len(concepts) == 0:
        bottom_concept = [c for c in concepts if count[c] == 0][0]
        stability[bottom_concept] = subsets[bottom_concept] / \
            float(2 ** len(bottom_concept.extent))
        concepts.remove(bottom_concept)
        for c in concepts:
            if bottom_concept.intent > c.intent:
                subsets[c] -= subsets[bottom_concept]
                count[c] -= 1
    return stability

if __name__ == '__main__':
    import doctest
    doctest.testmod()

