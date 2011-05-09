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
    
class NotUniqueAttributeName(ExplorationException):
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
        db._cxt_implications = db._cxt.get_attribute_implications(
                                            confirmed=db._implications)
    return wrapper
    
def base_modifier(F):
    """
    Decorator for methods where background knowledge is somehow modified.
    Recomputes context relative basis
    """
    def wrapper(db, *args):
        F(db, *args)
        db._cxt_implications = db._cxt.get_attribute_implications(
                                                confirmed=db._implications)
    return wrapper
    
class ExplorationDB(object):
    """docstring for ExplorationDB"""
    def __init__(self, context, implications):
        super(ExplorationDB, self).__init__()
        self._cxt = deepcopy(context)
        # background knowledge
        self._implications = deepcopy(implications)
        # relative basis
        self._cxt_implications = context.get_attribute_implications(
                                                confirmed=self._implications)
    
    @base_modifier
    def confirm_implication(self, imp):
        """docstring for confirm_implication"""
        self._implications.append(imp)
        
    @base_modifier
    def unconfirm_implication(self, imp):
        self._implications.remove(imp)
    
    @context_modifier
    def add_example(self, name, intent):
        if name in self._cxt.objects:
            raise NotUniqueAttributeName()
        self._cxt.add_object_with_intent(intent, name)
            
    def get_open_implications(self):
        return deepcopy(self._cxt_implications)
        
    def get_base(self):
        return deepcopy(self._implications)
        
    def get_object_names(self):
        return self._cxt.objects
        
    def get_attribute_names(self):
        return self._cxt.attributes
    
    objects = property(get_object_names)
    attributes = property(get_attribute_names)
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
            
    def unconfirm_implication(self, imp):
        self.db.unconfirm_implication(imp)
            
    def get_open_implications(self):
        return self.db.open_implications