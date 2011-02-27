import copy

import fca

class ExplorationException(Exception):
    pass
    
class WrongCounterExample(ExplorationException):
    pass
    
class BasisConflict(ExplorationException):
    
    def __init__(self, set_):
        self.set = set_
        
    def __str__(self):
        return "{0} conflict with confirmed implications".format(self.set)
    
class NotCounterExamplePremise(WrongCounterExample):
    
    def __init__(self, set_, implication):
        self.set = set_
        self.implication = implication
        
    def __str__(self):
        output = "{0} is not counter example to {1}. ".format(self.set, 
                                                            self.implication)
        output += "Counter example doesn't contain all elements from premise"
        return output
        
class NotCounterExampleConclusion(WrongCounterExample):

    def __init__(self, set_, implication):
        self.set = set_
        self.implication = implication

    def __str__(self):
        output = "{0} is not counter example to {1}. ".format(self.set, 
                                                            self.implication)
        output += "Counter example intent contains all elements from "\
                  "conclusion"
        return output

class BasicExploration(object):
    """
    Exploration class for basic exploration algorithm
    """
    
    context = None
    attribute_implications = None
    object_implications = None
    confirmed_attribute_implications = None
    confirmed_object_implications = None
    
    def __init__(self, initial_cxt):
        """Exploration starts with some initial context - *initial_cxt*"""
        self.context = copy.deepcopy(initial_cxt)
        # After initializng of context we need to compute initial implications
        self._init_implications()
        
    def __repr__(self):
        output = ""
        output += "Context:\n"
        output += "========\n"
        output += str(self.context) + "\n"
        output += "Attribute implications:\n"
        output += "=======================\n"
        for imp in self.attribute_implications:
            output += str(imp) + "\n"
        output += "Confirmed attribute implications:\n"
        output += "=================================\n"
        for imp in self.confirmed_attribute_implications:
            output += str(imp) + "\n"
        output += "Object implications:\n"
        output += "====================\n"
        for imp in self.object_implications:
            output += str(imp) + "\n"
        output += "Confirmed object implications:\n"
        output += "==============================\n"
        for imp in self.confirmed_object_implications:
            output += str(imp) + "\n"
        return output
        
    def _init_implications(self):
        """Compute stem base for initial context"""
        self.attribute_implications = fca.compute_dg_basis(self.context)
        transposed_cxt = self.context.transpose()
        self.object_implications = fca.compute_dg_basis(transposed_cxt)
        self.confirmed_attribute_implications = []
        self.confirmed_object_implications = []
        
    def recompute_basis(self):
        basis = self.confirmed_attribute_implications
        new_implications = fca.compute_dg_basis(self.context, basis)
        self.attribute_implications = []
        for imp in new_implications:
            if imp not in basis:
                self.attribute_implications.append(imp)
                
        basis = self.confirmed_object_implications
        transposed_cxt = self.context.transpose()
        new_implications = fca.compute_dg_basis(transposed_cxt, basis)
        self.object_implications = []
        for imp in new_implications:
            if imp not in basis:
                self.object_implications.append(imp)
        
    def confirm_attribute_implication(self, imp_index):
        imp = self.attribute_implications[imp_index]
        self.confirmed_attribute_implications.append(imp)
        del self.attribute_implications[imp_index]
        
    def confirm_object_implication(self, imp_index):
        imp = self.object_implications[imp_index]
        self.confirmed_object_implications.append(imp)
        del self.object_implications[imp_index]
        
    def counter_example_for_attr_implication(self, name, intent, imp_index):
        implication = self.attribute_implications[imp_index]
        premise = implication.premise
        conclusion = implication.conclusion
        
        # first we need to check that it is actually the counter example
        # counter example intent should contain all attributes from premise
        if (premise & intent) != premise:
            raise NotCounterExamplePremise(intent, implication)

        # Counterexample intent should contain NOT all attributes from 
        # conclusion
        if (conclusion & intent) == conclusion:
            raise NotCounterExampleConclusion(intent, implication)
        
        if not self.check_intent_for_conflicts(intent):
            raise BasisConflict(intent)    
            
        # if counter example is correct, we add new object to context
        # and recompute stem base with confirmed implications as basis
        self.context.add_object_with_intent(intent, name)
        self.recompute_basis()
            
    def counter_example_for_obj_implication(self, name, extent, imp_index):
        implication = self.object_implications[imp_index]
        premise = implication.premise
        conclusion = implication.conclusion

        # first we need to check that it is actually the counter example
        # counter example intent should contain all attributes from premise
        if (premise & extent) != premise:
            raise NotCounterExamplePremise(extent, implication)

        # Counterexample intent should contain NOT all attributes from 
        # conclusion
        if (conclusion & extent) == conclusion:
            raise NotCounterExampleConclusion(extent, implication)
            
        if not self.check_extent_for_conflicts(extent):
            raise BasisConflict(extent)
            
        # if counter example is correct, we add new attribute to context
        # and recompute stem base with confirmed implications as basis
        self.context.add_attribute_with_extent(extent, name)
        self.recompute_basis()    
        
    def check_extent_for_conflicts(self, extent):
        """
        Checks new attribute with *extent* for conflicts with confirmed
        object implications. Return True if all is ok.
        """
        for imp in self.confirmed_object_implications:
            if (imp.premise & extent) != imp.premise:
                continue
            if (imp.conclusion & extent) == imp.conclusion:
                continue
            return False

        return True
        
    def check_intent_for_conflicts(self, intent):
        """
        Checks new object with *intent* for conflicts with confirmed
        attribute implications. Return True if all is ok.
        """
        for imp in self.confirmed_attribute_implications:
            if (imp.premise & intent) != imp.premise:
                continue
            if (imp.conclusion & intent) == imp.conclusion:
                continue
            return False

        return True
        
    def add_object(self, intent, name):
        if not check_intent_for_conflicts(intent):
            raise BasisConflict(intent)
        else:
            self.context.add_object_with_intent(intent, name)
            self.recompute_basis()
            
    def add_attribute(self, extent, name):
        if not check_extent_for_conflicts(extent):
            raise BasisConflict(extent)
        else:
            self.context.add_attribute_with_extent(extent, name)
            self.recompute_basis()
            
    def edit_attribute(self, new_extent, name):
        if not check_extent_for_conflicts(extent):
            raise BasisConflict(extent)
        else:
            self.context.set_attribute_extent(extent, name)
            self.recompute_basis()
            
    def edit_object(self, new_intent, name):
        if not check_intent_for_conflicts(intent):
            raise BasisConflict(intent)
        else:
            self.context.set_object_intent(intent, name)
            self.recompute_basis()

if __name__ == "__main__":    
    table = [[True, False, False, True],\
             [True, False, True, False],\
             [False, True, True, False],\
             [False, True, True, True]]
    objs = ['1', '2', '3', '4']
    attrs = ['a', 'b', 'c', 'd']
    cxt = fca.Context(table, objs, attrs)
    exp = BasicExploration(cxt)
    print exp
    exp.confirm_object_implication(1)
    exp.counter_example_for_obj_implication('test', set(['3']), 0)
    print exp