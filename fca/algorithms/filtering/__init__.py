"""Module provides filtering capabilities"""
from filter import (filter_concepts, compute_index)
from probability import compute_probability
from separation import compute_separation_index
from stability import (compute_estability, compute_istability)
from extentsize import compute_extent_size
from intentsize import compute_intent_size

def get_compute_functions():
    functions = {"Probability index" : compute_probability,
                 "Separation index" : compute_separation_index,
                 "Intensional stability" : compute_istability,
                 "Extensional stability" : compute_estability,
                 "Extent size" : compute_extent_size,
                 "Intent size" : compute_intent_size}
    return functions

def get_modes():
    return ["part", "abs", "value"]