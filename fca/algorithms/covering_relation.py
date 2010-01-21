# -*- coding: utf-8 -*-
"""Holds a function that computes covering relation for a given concept
system"""

def compute_covering_relation(cs):
    """Computes covering relation for a given concept system.
    
    Returns a dictionary containing sets of parents for each concept.

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
    >>> print cs
    ([], M)
    ([1], ['a', 'd'])
    ([2], ['a', 'c'])
    ([1, 2], ['a'])
    ([3, 4], ['b', 'c'])
    ([2, 3, 4], ['c'])
    (G, [])
    ([4], ['b', 'c', 'd'])
    ([1, 4], ['d'])
    >>> parents = compute_covering_relation(cs)
    >>> for c in cs:
    ...     print c
    ...     for p in parents[c]:
    ...         print ' '.join(['<<<', str(p)])
    ...
    ([], M)
    <<< ([1], ['a', 'd'])
    <<< ([2], ['a', 'c'])
    <<< ([4], ['b', 'c', 'd'])
    ([1], ['a', 'd'])
    <<< ([1, 2], ['a'])
    <<< ([1, 4], ['d'])
    ([2], ['a', 'c'])
    <<< ([1, 2], ['a'])
    <<< ([2, 3, 4], ['c'])
    ([1, 2], ['a'])
    <<< (G, [])
    ([3, 4], ['b', 'c'])
    <<< ([2, 3, 4], ['c'])
    ([2, 3, 4], ['c'])
    <<< (G, [])
    (G, [])
    ([4], ['b', 'c', 'd'])
    <<< ([3, 4], ['b', 'c'])
    <<< ([1, 4], ['d'])
    ([1, 4], ['d'])
    <<< (G, [])

    """
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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
