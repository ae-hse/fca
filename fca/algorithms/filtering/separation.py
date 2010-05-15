"""
Created on 12.02.2010

@author: jupp
"""
from __future__ import division

def compute_separation_index(lattice):
    context = lattice.context
    cross_index = {}
    
    for c in lattice:
        attrs = c.intent
        objs = c.extent
        square = len(attrs)*len(objs)
        crossed = 0
        for attr in attrs:
            crossed += len(context.get_attribute_extent(attr))
                 
        for obj in objs:
            crossed += len(context.get_object_intent(obj))
        crossed -= square
        if square == 0:
            cross_index[c] = 1.0
        else:
            cross_index[c] = square/crossed
            
    return cross_index

if __name__ == '__main__':
    from fca import ConceptLattice, Context
    
    ct = [[True, False, False, True],\
          [True, False, True, False],\
          [False, True, True, False],\
          [False, True, True, True]]
    objs = [1, 2, 3, 4]
    attrs = ['a', 'b', 'c', 'd']
    c = Context(ct, objs, attrs)
    cl = ConceptLattice(c)
    ci = compute_separation_index(cl)
    print ci