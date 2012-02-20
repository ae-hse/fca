import fca

from fca.algorithms import closure_operators


def kclosure(s, k, cxt):
    """Return the closure of s in cxt restricted to the first k attributes."""
    closure = set(cxt.attributes[:k])
    for o in cxt.examples():
        if s == closure:
            break
        if s <= o:
            closure &= o
    return closure


# todo: optimize!
def compare_tuples(p, r):
    diff = p[1] ^ r[1]
    if diff:
        return 1 if sorted(diff)[0] in p[1] else -1
    else:
        return 0


def canonical_basis(cxt, close=closure_operators.simple_closure):
    preclosed = [(set(cxt.objects), set())]
    basis = []
    # each preclosed is (extent, intent) or (extent, premise, implication)
    # assuming that premise and implication.premise are the same object
    for i in range(len(cxt.attributes)):
        preclosed, basis = update_preclosed(i, cxt, preclosed, close)        
    return basis


def update_preclosed(i, cxt, preclosed,
                     close=closure_operators.simple_closure):

        m = cxt.attributes[i]
        extent = cxt.get_attribute_extent_by_index(i)
        context_closure = lambda s: kclosure(s, i + 1, cxt)
    
        old_stable_impl = []    # stores implications
        new_stable_impl = []    # stores implications
        min_mod_impl = []       # stores implications
        
        non_min_mod = []        # stores triples
        mod_extra = []          # stores pairs or triples

        new_preclosed = []

        for p in preclosed:
            if p[0] <= extent:  # p[1] -> m holds
                if is_concept(p):
                    process_modified_concept(p, m, min_mod_impl, mod_extra,
                                             new_preclosed)
                else:
                    process_modified_implication(p, m, min_mod_impl,
                                                 non_min_mod,
                                                 new_preclosed)
            else:               # p[1] -> m does not hold
                new_preclosed.append(p)
                if is_concept(p):       # p[1] remains closed
                    process_stable_concept(p, m, extent, new_stable_impl,
                                           new_preclosed,
                                           context_closure)
                else:                   # p[1] remains pseudo-closed
                    old_stable_impl.append(p[2])

        basis = old_stable_impl + new_stable_impl + min_mod_impl
        n = len(basis)
        basis += [p[2] for p in non_min_mod]
        for j in range(len(non_min_mod) - 1, -1, -1):
            impl = non_min_mod[j][2]
            del basis[n + j]
            premise = impl.premise
            premise |= close(premise, basis)    # sic! changing impl.premise
            if premise != impl.get_conclusion():
                basis.append(impl)
                mod_extra.append(non_min_mod[j])

        mod_extra.sort(cmp=compare_tuples)

        return new_preclosed + mod_extra, basis


def process_stable_concept(p, m, extent, new_stable_impl, new_preclosed,
                           closure):
    # p is of the form (extent, intent)
    new_extent = p[0] & extent
    new_premise = p[1].copy()
    new_premise.add(m)
    for i in new_stable_impl:
        if not i.is_respected(new_premise):
            break
    else:
        new_conclusion = closure(new_premise)
        if new_conclusion == new_premise:
            new_preclosed.append((new_extent, new_premise))
        else:
            impl = fca.Implication(new_premise, new_conclusion)
            new_stable_impl.append(impl)
            new_preclosed.append((new_extent, impl.premise, impl))


def process_modified_implication(p, m, min_mod_impl, non_min_mod,
                                 new_preclosed):
    # p is of the form (extent, premise, implication)
    p[2].get_conclusion().add(m)
    for i in min_mod_impl:
        if i.premise <= p[1]:   # p[1] is no longer preclosed
            p[1].add(m)         # assuming that p[1] is p[2].premise
            non_min_mod.append(p)
            break
    else:                       # p[1] remains psuedo-closed
        min_mod_impl.append(p[2])
        new_preclosed.append(p)


def process_modified_concept(p, m, min_mod_impl, mod_concepts, new_preclosed):
    # p is of the form (extent, intent)
    for i in min_mod_impl:
        if i.premise <= p[1]:   # p[1] is no longer preclosed
            break
    else:                       # p[1] becomes psuedo-closed
        impl = fca.Implication(p[1].copy(), p[1].copy())
        impl.get_conclusion().add(m)
        min_mod_impl.append(impl)
        new_preclosed.append((p[0], impl.premise, impl))
    p[1].add(m)
    mod_concepts.append(p)
    

def is_concept(p):
    return len(p) == 2


if __name__ == '__main__':
    import time
    import sys
    
    
    def timeit(algo, cxt):
        start = time.time()
        basis = algo(cxt)
        end = time.time()
        print len(basis), end - start
        return basis, end - start
        

    cxt = fca.read_cxt(sys.argv[1])
    print 'Ganter:'
    timeit(fca.compute_dg_basis, cxt)
    print 'Incremental:'
    timeit(canonical_basis, cxt)
