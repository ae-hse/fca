# -*- coding: utf-8 -*-
"""Derivation and closure operators"""

import copy

def oprime(objects, context):
    """
    Compute the set of all attributes shared by objects in context.
    NB: objects must be of type set
    
    """
    attributes = set(context.attributes[:])
    for o in objects:
        attributes &= context.get_object_intent(o)
    return attributes
    

def aprime(attributes, context):
    """
    Compute the set of all objects sharing attributes in context.
    NB: attributes must be of type set
    
    """
    objects = set(context.objects[:])
    for a in attributes:
        objects &= context.get_attribute_extent(a)
    return objects
    
    
def oclosure(objects, context):
    """Return the closure of objects in context as a sorted list"""
    return sorted(aprime(oprime(objects, context), context))
    

def aclosure(attributes, context):
    """Return the closure of attributes in context as a sorted list"""
    return sorted(oprime(aprime(attributes, context), context))

def closure(current, base_set, implications, prefLen):
    """
    return the closure of attributes
    NB: current and base_set must be of type set
    """
    unused_imps = copy.copy(implications)
    old_closure = copy.copy(base_set)
    new_closure = copy.copy(current)
    
    while (old_closure != new_closure):
        old_closure = copy.copy(new_closure)
        delete_list = [];
        
        for imp in unused_imps:
            if imp.get_premise() <= new_closure:
                new_closure |= imp.get_conclusion()
                
                for x in base_set[:prefLen]:
                    if (((x in new_closure) and not (x in current)) 
                        or (not (x in new_closure) and (x in current))):
                        return False, set()
                
                delete_list.append(imp)
                
        for imp in delete_list:
            unused_imps.remove(imp)
    
    return True, new_closure    
                
        
