# -*- coding: utf-8 -*-
"""
Holds functions that compute implication covers for a given context 
"""
import copy

import closure_operators
from fca.implication import Implication
import fca


def compute_implication_cover(cxt, close=closure_operators.closure):
    """
    Compute an implication cover for a given *cxt* using 
    an object-incremental algorithm
    """
    attributes = set(cxt.attributes)
    basis = [Implication(set(), attributes.copy())]
    i = 0
    for intent in cxt.examples():
        i += 1
        print 'object ', i
#        print_basis(basis)
#        print 'Adding ', intent
#        raw_input()
        basis = updated_basis(intent, basis, attributes)
        print len(basis), 'implications'
    return basis


def print_basis(basis):
    print '***'
    for imp in basis:
        print imp
    print '+++'
    

def is_redundant(imp, basis, close=closure_operators.simple_closure):
    return imp.conclusion <= close(imp.premise, basis)
    
    
def is_new(imp, implications):
    if imp.conclusion <= imp.premise:
        return False
    for i in implications:
        if is_subsumed_simply(imp, i):
            return False
        elif is_subsumed(imp, i):
            raise 'ALERT: %s is sumbsumed by %s' %(imp, i)
        elif is_subsumed(i, imp):
            raise 'ALERT: %s sumbsumes %s' % (imp, i)
    return True
    

def is_subsumed_simply(imp, by_imp):
    return by_imp.premise <= imp.premise and imp.conclusion <= by_imp.conclusion


def is_subsumed(imp, by_imp):
    return (by_imp.premise <= imp.premise and
            imp.conclusion <= (by_imp.conclusion | imp.premise))
    

def remove_subsumed_plus(imp, implications):
    if imp.conclusion <= imp.premise:
        return False
    for i in implications[:]:
        if i.premise == imp.premise:
            i.conclusion.update(imp.conclusion)
            return False
        elif i.premise <= imp.premise:
            if imp.conclusion <= i.conclusion:
                return False
            else:
                imp.conclusion.update(i.conclusion)
        elif imp.premise <= i.premise:
            if i.conclusion <= imp.conclusion:
                implications.remove(i)
            else:
                i.conclusion.update(imp.conclusion)
    return True


def remove_subsumed(imp, implications):
    if imp.conclusion <= imp.premise:
        return False
    can_be_subsumed = True
    for i in implications[:]:
        if can_be_subsumed and i.premise <= imp.premise:
            if imp.conclusion <= i.conclusion:
                return False
            else:
                imp.conclusion.update(i.conclusion)
        elif is_subsumed_simply(i, imp):
            implications.remove(i)
            can_be_subsumed = False
    return True
    

def remove_subsumed_simply(imp, implications):
    if imp.conclusion <= imp.premise:
        return False
    can_be_subsumed = True
    for i in implications[:]:
        if can_be_subsumed and is_subsumed_simply(imp, i):
            return False
        elif is_subsumed_simply(i, imp):
            implications.remove(i)
            can_be_subsumed = False
    return True


def add_smartly(imp, new_valid, valid):
    if is_new(imp, valid) and remove_subsumed_simply(imp, new_valid):
        new_valid.append(imp)


def updated_basis(intent, basis, attributes):
    valid = []
    invalid = []
    for imp in basis:
        if not imp.premise <= intent or imp.conclusion <= intent:
            valid.append(imp)
        else:
            invalid.append(imp)
            
    new_valid = []
    for imp in invalid:
        new_imp = Implication(imp.premise, imp.conclusion & intent)
        add_smartly(new_imp, new_valid, valid)
        
    valid += new_valid
    new_valid = []
    for imp in invalid:
        for a in attributes - intent:
            aset = set([a])
            new_imp = Implication(imp.premise | aset, imp.conclusion | aset)
            if (remove_subsumed(new_imp, valid) and
                remove_subsumed_plus(new_imp, new_valid)):
               new_valid.append(new_imp)
    return valid + new_valid
                    

def minimize(cover, close=closure_operators.simple_closure):
#    i = 0
#    for imp in cover:
#        i += 1
#        print 'maximizing conclusion ', i
#        imp._conclusion = close(imp.premise | imp.conclusion, cover)
    i = 0
    for imp in cover[:]:
        i += 1
        print 'maximizing premise ', i
        cover.remove(imp)
        imp._premise = close(imp.premise, cover)
        if not imp.conclusion <= imp.premise:
            cover.append(imp)
        print len(cover), 'implications'


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
    
    imp_basis = compute_implication_cover(cxt, closure_operators.closure)
    print_basis(imp_basis)
    minimize(imp_basis)
    print(len(imp_basis))
    for imp in imp_basis:
        print imp
        
    print '***'
    
    objects = [1, 2, 3, 4]
    attributes = ['a', 'b', 'c', 'd']
    table = [[True, False, True, True],
             [True, False, True, False],
             [False, True, True, False],
             [False, True, False, True]]
    cxt = fca.Context(table, objects, attributes)
    
    imp_basis = compute_implication_cover(cxt, closure_operators.closure)
    print_basis(imp_basis)
    minimize(imp_basis)
    print(len(imp_basis))
    for imp in imp_basis:
        print imp