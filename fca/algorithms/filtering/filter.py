import fca

import separation
import probability
import stability

def compute_index(lattice, function, name):
    indexes = function(lattice)
    
    for concept in indexes.items():
        if concept[0].meta:
            concept[0].meta[name] = concept[1]
        else:
            concept[0].meta = {name : concept[1]}

def filter_concepts(lattice, function, mode, opt=1):
    """Return new concept system, filtered by function according to the mode.
    
    Modes:
    --- "part" - part of initial concept lattice
    --- "abs" - absolute value of the concepts in resulting concept system
    --- "value" - value of the index
    
    Additionaly add attribute, containing inforamtion about indexes, to the new lattice
    """
    def _filter_value(lattice, indexes, value):
        filtered_concepts = [item for item in indexes.items() if item[1]>=value]
        return fca.ConceptSystem([c[0] for c in filtered_concepts])
    
    def _filter_abs(lattice, indexes, n):
        cmp_ = lambda x,y: cmp(x[1], y[1])
        sorted_indexes = sorted(indexes.items(), cmp_, reverse=True)
        filtered_concepts = sorted_indexes[:int(n)]
            
        return fca.ConceptSystem([c[0] for c in filtered_concepts])
    
    def _filter_part(lattice, indexes, part):
        n = int(len(lattice) * part)
        cmp_ = lambda x,y: cmp(x[1], y[1])
        sorted_indexes = sorted(indexes.items(), cmp_, reverse=True)
        filtered_concepts = sorted_indexes[:n]
        
        values = sorted_indexes
        eps = values[n-2][1]-values[n-1][1]
        
        other_concepts = sorted_indexes[n:]
        for concept in other_concepts:
            if abs(concept[1] - values[n][1]) < eps:
                filtered_concepts.append(concept)
            
        return fca.ConceptSystem([c[0] for c in filtered_concepts])
    
    indexes = function(lattice)
    if indexes:
        if mode == "part":
            ret = _filter_part(lattice, indexes, opt)
        elif mode == "abs":
            ret = _filter_abs(lattice, indexes, opt)
        elif mode == "value":
            ret = _filter_value(lattice, indexes, opt)
    return ret
    
if __name__ == '__main__':
    # Test code
    from fca import ConceptLattice, Context
    from probability import compute_probability
    from stability import (compute_estability, compute_istability)
    from separation import compute_separation_index
    
    ct = [[True, False, False, True],\
          [True, False, True, False],\
          [False, True, True, False],\
          [False, True, True, True]]
    objs = ['1', '2', '3', '4']
    attrs = ['a', 'b', 'c', 'd']
    c = Context(ct, objs, attrs)
    cl = ConceptLattice(c)
#    compute_index(cl, compute_probability, "Probability")
#    cs = filter_concepts(cl, compute_probability, "abs", 4)
#    compute_index(cl, compute_separation_index, "Separation")
#    cs = filter_concepts(cl, compute_probability, "value", 0.5)
    # compute_index(cl, compute_istability, "Intensional Stability")
    # print cl
    cs = filter_concepts(cl, compute_istability, "abs", 2)
    print cs