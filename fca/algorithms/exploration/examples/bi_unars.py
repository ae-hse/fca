#!/usr/bin/env python
# encoding: utf-8
import copy
import itertools

import fca

from fca.algorithms.exploration.exploration import (AttributeExploration,
                                                    ExplorationDB)
from fca import Implication
# from fca.algorithms.closure_operators import simple_closure as closure


class BiUnar(object):

    def  __init__(self, f, g):
        self.f = f
        self.g = g
        
    def __str__(self):
        return '%s%s' % (self.f, self.g)
        
    def automorphic_copy(self):
        return BiUnar(self.g, self.f)
        
        
class Term(object):
    
    def __init__(self, name, function):
        self._name = name
        self._function = function
        
    def __call__(self, bu):
        return self._function(bu)
        
    def __str__(self):
        return self._name
        
        
class Equality(object):
    
    def __init__(self, left_term, right_term):
        self.left = left_term
        self.right = right_term
        
    def __call__(self, bu):
        return self.left(bu) == self.right(bu)
        
    def __str__(self):
        return "%s = %s" % (self.left, self.right)
        
    def automorphic_copy(self):
        return Equality(get_symmetric_term(self.left),
                        get_symmetric_term(self.right))
#        
#    def __eq__(self, eq):
#        return ((self.left == eq.left and self.right == eq.right) or
#                (self.left == eq.right and self.right == eq.left))
#                
#    def __ne__(self, eq):
#        return not self == eq
#
#    def __hash__(self):
#        if self.left < self.right:
#            return hash((self.left, self.right))
#        else:
#            return hash((self.right, self.left))


class CommandLineExpert(object):

    def is_valid(self, imp):
        print "{0}".format(imp)
        return input('Is the following implication valid? Enter "True" or "False": {0}'.format(imp))
                                                                                    
    def explore(self, exploration):
        while exploration.get_open_implications():
            imp = exploration.get_open_implications()[0]
            if self.is_valid(imp):
                exploration.confirm_implications([imp,
                                                get_symmetric_implication(imp)])
            else:
                exploration.reject_implication(imp)

    def provide_counterexample(self, imp):
        print 'Provide a counterexample by typing in two tuples.'
        bu = BiUnar(input('f: '), input('g: '))
        if input('Add as a partial example? Enter "True" or "False": '):
            intent = generate_partial_counterexample(imp, bu)
        else:
            intent = [bu_intent(bu)] * 2    # since our context is partial
        return ((bu, bu.automorphic_copy()),
                (intent, [get_symmetric_attribute_set(s) for s in intent]))


def compose(f, g):
    return tuple([f[x - 1] for x in g])
    
            
def generate_examples(n):
    maps = itertools.product(range(1, n + 1), repeat=n)
    return (BiUnar(mm[0], mm[1]) for mm in itertools.product(maps, repeat=2))
    
    
def bu_intent(bu):
    return set([a for a in attributes if a(bu)])
    
    
def generate_partial_counterexample(imp, bu):
    relevant_attributes = imp.premise | imp.conclusion
    xintent = set([a for a in relevant_attributes if a(bu)])
    qintent = (set(attributes) - relevant_attributes) | xintent
    return xintent, qintent


def find_counter_example(n, imp):
    for e in generate_examples(n):
        if not imp.is_respected(bu_intent(e)):
            return e
    
    
def generate_context(n, attributes):
    objects = [e for e in generate_examples(n)]
    table = [[a(o) for a in attributes] for o in objects]
    cxt = fca.partial_context.PartialContext(table,
                                             copy.deepcopy(table),
                                             objects,
                                             attributes)
    # TODO: reduce cxt
    return cxt
    
    
def generate_background_implications(attributes):
    return [Implication(set([x, y]), set([z]))
                    for x in attributes
                    for y in attributes
                    for z in attributes
                    if (x.left == z.left and
                        x.right == y.left and
                        y.right == z.right) or
                       (x.left == z.left and
                        x.right == y.right and
                        y.left == z.right) or
                       (x.left == y.left and
                        x.right == z.left and
                        y.right == z.right)
            ]
            
            
def is_orbit_maximal(eqs):
    symmetric_eqs = get_symmetric_attribute_set(eqs)
    for a in attributes:
        if a in eqs:
            if a not in symmetric_eqs:
                return True
        elif a in symmetric_eqs:
            return False
    return True
    
    
def get_symmetric_attribute_set(eqs):
    symmetric_eqs = set([])
    for e in eqs:
        left = get_symmetric_term(e.left)
        right = get_symmetric_term(e.right)
        if terms.index(left) > terms.index(right):
            left, right = right, left
        for a in attributes:
            if a.left == left and a.right == right:
                symmetric_eqs.add(a)
                break
    return symmetric_eqs
                

def get_symmetric_term(term):
    s = str(term)
    s = s.replace('f', 'F')
    s = s.replace('g', 'f')
    s = s.replace('F', 'g')
    for t in terms:
        if str(t) == s:
            return t
            
            
def get_symmetric_equality(e):
    s = str(e.automorphic_copy())
    for a in attributes:
        if str(a) == s:
            return a


def get_symmetric_implication(imp):
    return Implication(get_symmetric_attribute_set(imp.premise),
                       get_symmetric_attribute_set(imp.conclusion))


terms = [
            Term('id', lambda bu: tuple(range(1, len(bu.f) + 1))),
            Term('f', lambda bu: bu.f),
            Term('g', lambda bu: bu.g),
            Term('ff', lambda bu: compose(bu.f, bu.f)),
            Term('fg', lambda bu: compose(bu.f, bu.g)),
            Term('gf', lambda bu: compose(bu.g, bu.f)),
            Term('gg', lambda bu: compose(bu.g, bu.g))
        ]
        
            
attributes = [Equality(terms[i], terms[j]) for i in range(len(terms))
                                           for j in range(i + 1, len(terms))]
                                              

db = ExplorationDB(generate_context(3, attributes),
                   generate_background_implications(attributes),
                   is_orbit_maximal)
expert = CommandLineExpert()
exploration = AttributeExploration(db, expert)

# expert.explore(exploration)


