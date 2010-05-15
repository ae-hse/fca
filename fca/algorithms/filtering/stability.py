#!/usr/bin/env python
# encoding: utf-8
"""
stability.py

Created by Nikita Romashkin on 2010-01-19.

"""
from __future__ import division

from copy import deepcopy

from fca import ConceptSystem


def compute_istability(lattice):
    """
    Examples
    ========

    >>> from fca import Context, ConceptLattice
    >>> ct = [[True, False, False, True],\
              [True, False, True, False],\
              [False, True, True, False],\
              [False, True, True, True]]
    >>> objs = [1, 2, 3, 4]
    >>> attrs = ['a', 'b', 'c', 'd']
    >>> c = Context(ct, objs, attrs)
    >>> cl = ConceptLattice(c)
    >>> st = compute_estability(cl)
    >>> print st

    """
    concepts = ConceptSystem(lattice)
    count = {}
    subsets = {}
    stability = {}

    for concept in concepts:
        count[concept] = len([c for c in concepts if c.extent < concept.extent])
        subsets[concept] = 2 ** len(concept.extent)

    bottom_concepts = set([concepts.bottom_concept])
    while not len(concepts) == 0:
        bottom_concept = bottom_concepts.pop()
        stability[bottom_concept] = subsets[bottom_concept] / \
            (2 ** len(bottom_concept.extent))
        concepts.remove(bottom_concept)
        for c in concepts:
            if bottom_concept.intent > c.intent:
                subsets[c] -= subsets[bottom_concept]
                count[c] -= 1
                if count[c] == 0:
                    bottom_concepts.add(c)
    return stability

def compute_estability(lattice):
    """
    Examples
    ========

    >>> from fca import ConceptLattice, Context
    >>> ct = [[True, False, False, True],\
              [True, False, True, False],\
              [False, True, True, False],\
              [False, True, True, True]]
    >>> objs = [1, 2, 3, 4]
    >>> attrs = ['a', 'b', 'c', 'd']
    >>> c = Context(ct, objs, attrs)
    >>> cl = ConceptLattice(c)
    >>> st = compute_estability(cl)
    >>> print st

    """

    concepts = ConceptSystem(lattice)
    count = {}
    subsets = {}
    stability = {}

    for concept in concepts:
        count[concept] = len([c for c in concepts if c.intent < concept.intent])
        subsets[concept] = 2 ** len(concept.intent)

    bottom_concepts = set([concepts.top_concept])
    while not len(concepts) == 0:
        bottom_concept = bottom_concepts.pop()
        stability[bottom_concept] = subsets[bottom_concept] / \
            (2 ** len(bottom_concept.intent))
        concepts.remove(bottom_concept)
        for c in concepts:
            if bottom_concept.intent < c.intent:
                subsets[c] -= subsets[bottom_concept]
                count[c] -= 1
                if count[c] == 0:
                    bottom_concepts.add(c)
    return stability

if __name__ == '__main__':
    import doctest
    doctest.testmod()

