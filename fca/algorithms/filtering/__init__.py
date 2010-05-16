"""Module provides filtering capabilities"""
from filter import (filter_concepts, compute_index)
from probability import compute_probability
from separation import compute_separation_index
from stability import (compute_estability, compute_istability)

def get_compute_functions():
    functions = {"Probability index" : compute_probability,
                 "Separation index" : compute_separation_index,
                 "Intensional stability" : compute_istability,
                 "Extensional stability" : compute_estability}
    return functions

def get_modes():
    return ["part", "abs", "value"]