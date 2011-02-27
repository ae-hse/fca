# -*- coding: utf-8 -*-
"""
Holds a function that computes Duquenne-Guigues basis for a given context 
"""

import closure_operators
import fca.implication
import copy

def compute_dg_basis(cxt, close=closure_operators.closure, imp_basis=None):
    """
    Compute Duquenne-Guigues basis for a given *cxt* using 
    optimized Ganter algorithm
    """
    aclose = lambda attributes: closure_operators.aclosure(attributes, cxt)
    return generalized_compute_dg_basis(cxt.attributes, 
                                        aclose, 
                                        close=closure_operators.closure,
                                        imp_basis=imp_basis)

def generalized_compute_dg_basis(attributes,
                                 aclose,
                                 close=closure_operators.closure,
                                 imp_basis = None
                                 ):
    """
    Compute Duquenne-Guigues basis using optimized Ganter algorithm.
    *aclose* is a function that compute a closure of attributes in context
    defined inside it. We need this to implement exploration algorithm with
    partially given examples
    """
    if not imp_basis:
        imp_basis = []
        
    a = set()
    p = set()
    ind = 0
    success = True
    while success:
        pClosed = set(aclose(p))
        if p != pClosed:
            imp_basis.append(fca.implication.Implication(copy.deepcopy(p), copy.deepcopy(pClosed)))
        
        for x in attributes[:ind]:
            if (((x in pClosed) and not (x in p)) 
                or (not (x in pClosed) and (x in p))):
                break
        else:
            a = pClosed
            ind = len(attributes)
        
        success = False
        while True:
            ind = ind - 1
            i = attributes[ind]
            
            if not (i in a):
                flag, tmp = close(a | set([i,]), attributes, imp_basis, ind)
                if flag:
                    success = True
                    p = tmp                                            
            else:
                a.remove(i)
                
            if success or ind == 0:
                break
        
    return imp_basis

if __name__ == "__main__":    
    objects = ['Air Canada', 'Air New Zeland', 'All Nippon Airways',
               'Ansett Australia', 'The Australian Airlines Group',
               'British Midland', 'Lufthansa', 'Mexicana',
               'Scandinavian Airlines', 'Singapore Airlines',
               'Thai Airways International', 'United Airlines',
               'VARIG']
    attributes = ['Latin America', 'Europe', 'Canada', 'Asia Pasific',
                  'Middle East', 'Africa', 'Mexico', 'Carribean',
                  'United States']
    table = [[True, True, True, True, True, False, True, True, True],
             [False, True, False, True, False, False, False, False, True],
             [False, True, False, True, False, False, False, False, True],
             [False, False, False, True, False, False, False, False, False],
             [False, True, True, True, True, True, False, False, True],
             [False, True, False, False, False, False, False, False, False],
             [True, True, True, True ,True, True, True, False, True],
             [True, False, True, False, False, False, True, True, True],
             [True, True, False, True, False, True, False, False, True],
             [False, True, True, True, True, True, False, False, True],
             [True, True, False, True, False, False, False, True, True],
             [True, True, True, True, False, False, True, True, True],
             [True, True, False, True, False, True, True, False, True]]
    cxt = fca.Context(table, objects, attributes)
    
    imp_basis = compute_dg_basis(cxt, closure_operators.closure)
    print(len(imp_basis))
    for imp in imp_basis:
        print imp