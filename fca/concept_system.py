# -*- coding: utf-8 -*-
"""Holds ConceptSystem class"""

from concept import Concept
#from algorithms import compute_covering_relation

class ConceptSystem(object):
    """A ConceptSystem class contains a set of concepts

    Emulates container

    Examples
    ========
    
    >>> c = Concept([1, 2], ['a', 'b'])
    >>> cs = ConceptSystem([c])
    >>> c in cs
    True
    >>> Concept([1], ['c']) in cs
    False
    >>> print cs
    ([1, 2], ['a', 'b'])

    """
    def get_top_concept(self):
        # TODO: change
        return [c for c in self._concepts if not self.filter(c)][0]

    top_concept = property(get_top_concept)

    def get_bottom_concept(self):
        # TODO: change
        return [c for c in self._concepts if not self.ideal(c)][0]

    bottom_concept = property(get_bottom_concept)

    def filter(self, concept):
        # TODO: optimize
        return [c for c in self._concepts if concept.intent > c.intent]

    def ideal(self, concept):
        # TODO: optimize
        return [c for c in self._concepts if c.intent > concept.intent]

    def __init__(self, concepts=[]):
        self._concepts = concepts[:]
        self._parents = None
        self._bottom_concept = None
        self._top_concept = None

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

    def index(self, concept):
        return self._concepts.index(concept)

    def append(self, concept):
        if isinstance(concept, Concept):
            self._concepts.append(concept)
        else:
            raise TypeError("concept must be an instance of the Concept class")
        self._parents = None
        # TODO: optimize

    def remove(self, concept):
        if isinstance(concept, Concept):
            self._concepts.remove(concept)
        self._parents = None

    def compute_covering_relation(self):
        """Computes covering relation for a given concept system.

        Returns a dictionary containing sets of parents for each concept.

        Examples
        ========

        """
        cs = self
        parents = dict([(c, set()) for c in cs])

        for i in xrange(len(cs)):
            for j in xrange(len(cs)):
                if cs[i].intent < cs[j].intent:
                    parents[cs[j]].add(cs[i])
                    for k in xrange(len(cs)):
                        if cs[i].intent < cs[k].intent and\
                           cs[k].intent < cs[j].intent:
                                parents[cs[j]].remove(cs[i])
                                break
        return parents

    def parents(self, concept):
        if not self._parents:
            self._parents = self.compute_covering_relation()
        return self._parents[concept]

    def children(self, concept):
        return set([c for c in self._concepts if concept in self.parents(c)])


if __name__ == "__main__":
    import doctest
    doctest.testmod()
