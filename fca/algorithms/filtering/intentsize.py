from __future__ import division

def compute_intent_size(lattice):
    number_of_attributes = len(lattice.context.attributes)
    intent_size_index = {}
    
    for c in lattice:
        intent_size_index[c] = len(c.intent) / number_of_attributes
            
    return intent_size_index