#!/usr/bin/env python
# encoding: utf-8
from copy import deepcopy
from fca import Context

class ExplorationException(Exception):
    pass
    
class NotCounterexample(ExplorationException):
    pass
    
class IllegalContextModification(ExplorationException):
    pass
    
def context_modifier(F):
    """
    Decorator for methods where context is somehow modified.
    Checks whether this new context respects all confirmed implications.
    If it does not, exception is raised and context remains unmodified. Also
    recompute implications in context.
    """
    def wrapper(db, *args):
        unmodified_cxt = deepcopy(db._cxt)
        F(db, *args)
        for intent in db._cxt.intents():
            for imp in db._implications:
                if not imp.is_respected(intent):
                    db._cxt = unmodified_cxt
                    raise IllegalContextModification()
    return wrapper
    
class ExplorationDB(object):
    """docstring for ExplorationDB"""
    def __init__(self, context, implications):
        super(ExplorationDB, self).__init__()
        self._cxt = context
        self._implications = implications
    
    def confirm_implication(self, imp):
        """docstring for confirm_implication"""
        self._implications.append(imp)
    
    @context_modifier
    def add_example(self, name, intent):
        self._cxt.add_object_with_intent(intent, name)
            
    def get_open_implications(self):
        cxt_implications = \
            self._cxt.get_attribute_implications(confirmed=self._implications)
        open_implications = []
        for imp in cxt_implications:
            if imp not in self._implications:
                open_implications.append(imp)
        return open_implications
        
    def get_base(self):
        return self._implications
                
    open_implications = property(get_open_implications)
    base = property(get_base)
        

class AttributeExploration(object):
    """Exploration"""
    def __init__(self, db, expert):
        super(AttributeExploration, self).__init__()
        self.db = db
        self.expert = expert
        
    def confirm_implication(self, imp):
        """docstring for confirm_implication"""
        self.db.confirm_implication(imp)
        
    def reject_implication(self, imp):
        """docstring for reject_implication"""
        name, intent = self.expert.provide_counterexample(imp)
        if imp.is_respected(intent):
            raise NotCounterexample()
        else:
            self.db.add_example(name, intent)