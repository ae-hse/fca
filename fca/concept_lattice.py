from algorithms import norris

class ConceptLattice(object):
    """ConceptLattice class

    Examples
    ========
    
    >>> from fca import (Context, Concept)
    >>> ct = [[True, False, False, True],\
              [True, False, True, False],\
              [False, True, True, False],\
              [False, True, True, True]]
    >>> objs = ['1', '2', '3', '4']
    >>> attrs = ['a', 'b', 'c', 'd']
    >>> c = Context(ct, objs, attrs)
    >>> cl = ConceptLattice(c)
    >>> print cl
    ([], M)
    (['1'], ['a', 'd'])
    (['2'], ['a', 'c'])
    (['1', '2'], ['a'])
    (['3', '4'], ['b', 'c'])
    (['2', '3', '4'], ['c'])
    (G, [])
    (['4'], ['b', 'c', 'd'])
    (['1', '4'], ['d'])
    >>> print cl.parents(cl[5]) == set((cl[6],))
    True
    >>> print cl.children(cl[6]) == set((cl[5], cl[3], cl[8]))
    True

    """
    def __init__(self, context, builder=norris):
        (self._concepts, self._parents) = norris(context)
        self._bottom_concept = [c for c in self._concepts if not self.ideal(c)][0]
        self._top_concept = [c for c in self._concepts if not self.filter(c)][0]
        self._context = context
    
    def get_context(self):
        return self._context
    
    context = property(get_context)
    
    def get_top_concept(self):
        # TODO: change
        return self._top_concept
    top_concept = property(get_top_concept)

    def get_bottom_concept(self):
        # TODO: change
        return self._bottom_concept

    bottom_concept = property(get_bottom_concept)

    def filter(self, concept):
        # TODO: optimize
        return [c for c in self._concepts if concept.intent > c.intent]

    def ideal(self, concept):
        # TODO: optimize
        return [c for c in self._concepts if c.intent > concept.intent]

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
    
    def parents(self, concept):
        return self._parents[concept]

    def children(self, concept):
        return set([c for c in self._concepts if concept in self.parents(c)])
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()