import fca

import cross
import probability
import stability

def filter_concepts(lattice, context, mode, part=1):
    """Return new lattice containing at least len(lattice)*part concepts
     plus some concepts with almost equal to "worthiest" concepts index value
     according to the filtering mode.
    
    Modes:
    --- "intensional stability"
    --- "extensional stability"
    --- "cross"
    --- "probability"
    
    Additionaly add attribute, containing inforamtion about indexes, to the new lattice
    """
    def _filter(lattice, indexes, part):
        n = int(len(lattice) * part)
        cmp_ = lambda x,y: cmp(x[1], y[1])
        sorted_indexes = dict(sorted(indexes.items(), cmp_, reverse=True))
        filtered_concepts = sorted_indexes.items()[:n]
        
        values = sorted_indexes.values()
        eps = values[n-2]-values[n-1]
        
        other_concepts = sorted_indexes.items()[n:]
        for concept in other_concepts:
            if abs(concept[1] - values[n]) < eps:
                filtered_concepts.append(concept)
                
        for concept in filtered_concepts:
            if concept[0].meta:
                concept[0].meta[mode] = concept[1]
            else:
                concept[0].meta = {mode : concept[1]}
            
        return fca.ConceptSystem([c[0] for c in filtered_concepts])
    
    if mode == "intensional stability":
        indexes = stability.compute_istability(lattice)
    elif mode == "extensional stability":
        indexes = stability.compute_estability(lattice)
    elif mode == "cross":
        indexes = cross.compute_cross_index(lattice, context)
    elif mode == "probability":
        indexes = probability.compute_probability(lattice, context)
    else:
        print "No such mode"
        return
    if indexes:
        return _filter(lattice, indexes, part)
    
if __name__ == '__main__':
    # Test code
    from fca import norris, Context
    
    ct = [[True, False, False, True],\
          [True, False, True, False],\
          [False, True, True, False],\
          [False, True, True, True]]
    objs = [1, 2, 3, 4]
    attrs = ['a', 'b', 'c', 'd']
    c = Context(ct, objs, attrs)
    cs = norris(c)
    l = filter_concepts(cs, c, "intensional stability")
    l = filter_concepts(l, c, "extensional stability")
    l = filter_concepts(l, c, "cross")
    l = filter_concepts(l, c, "probability")
    print l