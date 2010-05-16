"""
Created on 12.02.2010

@author: jupp
"""
from math import exp, log

def compute_probability(lattice):
    
    def get_intent_probability(B, p_m, n):
        ans = 0
        log_p_B = log_subset_probability(B, p_m)
        p_B = exp(log_p_B)
        if len(B) == 0:
            p_B = 1
            log_p_B = 0
        
        not_B = set()
        for attr in p_m.keys():
            if not attr in B:
                not_B.add(attr)
        for k in range(n + 1):
            mult = 0
            mult_is_zero = False
            for attr in not_B:
                try:
                    mult += log(1 - ((p_m[attr]) ** k))
                except:
                    mult_is_zero = True
                    break
            if mult_is_zero:
                continue
            try:
                if p_B == 1 and n == k:
                    return exp(mult)
                else:
                    t = k * log_p_B + (n - k) * log((1 - p_B)) + mult
                    t = exp(t)
                    # print k, t
            except:
                t = 0
            nom = range(n - k + 1, n + 1)
            den = range(1, k + 1)
            if len(den) != len(nom):
                print "False"
            for i in range(len(nom)):
                t *= nom[i] / float(den[i])
            ans += t
        return ans

    def log_subset_probability(subset, p_m):
        ans = 0
        for attr in subset:
            try:
                ans += log(p_m[attr])
            except:
                pass
        return ans

    context = lattice.context
    n = len(context)
    p_m = {}
    for attr in context.attributes:
        m_ = 0
        for i in range(n):
            o = context.get_object_intent_by_index(i)
            if attr in o:
                m_ += 1
        p_m[attr] = m_ / float(n)
        
    probability = {}
    for concept in lattice:
        probability[concept] = get_intent_probability(concept.intent, p_m, n)
        
    return probability



if __name__ == '__main__':
    # Test code
    from fca import ConceptLattice, Context
    
    ct = [[True, False, False, True],\
          [True, False, True, False],\
          [False, True, True, False],\
          [False, True, True, True]]
    objs = [1, 2, 3, 4]
    attrs = ['a', 'b', 'c', 'd']
    c = Context(ct, objs, attrs)
    cs = ConceptLattice(c)
    ci = compute_probability(cs)
    print ci