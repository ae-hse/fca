# -*- coding: utf-8 -*-
"""
Holds a function that computes Duquenne-Guigues basis for a given context 
"""

import closure_operators
from fca.implication import Implication
import fca

def compute_dg_basis(cxt,
                     close=closure_operators.lin_closure,
                     imp_basis=[],
                     cond=lambda x: True):
    """
    Compute Duquenne-Guigues basis for a given *cxt* using 
    optimized Ganter algorithm
    """
    return generalized_compute_dg_basis(list(cxt.attributes),
                                        cxt.aclosure,
                                        close=close,
                                        imp_basis=imp_basis,
                                        cond=cond)


def compute_partial_dg_basis(pcxt,
                             close=closure_operators.simple_closure,
                             imp_basis=[],
                             cond=lambda x: True):
    """
    Compute Duquenne-Guigues basis for a given partial context *pcxt* using
    optimized Ganter algorithm
    """
    return generalized_compute_dg_basis(pcxt.attributes,
                                        pcxt.xq_aclosure,
                                        close=close,
                                        imp_basis=imp_basis,
                                        cond=cond)


def generalized_compute_dg_basis(attributes,
                                 aclose,
                                 close=closure_operators.simple_closure,
                                 imp_basis=[],
                                 cond=lambda x: True):
    """Compute the Duquenne-Guigues basis using optimized Ganter's algorithm.
    
    *aclose* is a closure operator on the set of attributes.
    We need this to implement the exploration
    algorithm with partially given examples.
    
    """
    relative_basis = []
    
    a = close(set(), imp_basis)
    i = len(attributes)
    
    while len(a) < len(attributes):
        a_closed = aclose(a)
        if a != a_closed and cond(a):
            relative_basis.append(Implication(a.copy(), a_closed.copy()))
        if (a_closed - a) & set(attributes[: i]):
            a -= set(attributes[i :])
        else:
            if len(a_closed) == len(attributes):
                return relative_basis
            a = a_closed
            i = len(attributes)
        for j in range(i - 1, -1, -1):
            m = attributes[j]
            if m in a:
                a.remove(m)
            else:
                b = close(a | set([m]), relative_basis + imp_basis)
                if not (b - a) & set(attributes[: j]):
                    a = b
                    i = j
                    break

    return relative_basis

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

    cxt = fca.ObjectDictContext(set(attributes))

    gen_intent = lambda row: {attributes[i] for i in xrange(len(attributes)) if row[i]}
    for object_index in xrange(len(objects)):
        cxt.add_object(objects[object_index], gen_intent(table[object_index]))

    for imp in compute_dg_basis(cxt):
        print imp
