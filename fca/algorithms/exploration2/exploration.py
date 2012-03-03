#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy

import fca

class ExplorationException(Exception):
    pass

class FalseCounterexample(ExplorationException):
    pass

class IllegalContextModification(ExplorationException):

    def __str__(self):
        return "Attempted context modification conflicts with existing background knowledge"

class ExplorationContext(object):
    """Implements lightweight interface to formal context"""
    _cxt = None
    _basis = None

    def get_objects(self):
        return copy(self._cxt.get_objects())

    objects = property(get_objects)

    def get_attributes(self):
        return copy(self._cxt.get_attributes())

    attributes = property(get_attributes)

    def __init__(self, cxt):
        self._cxt = cxt

    def set_basis(self, basis):
        self._basis = basis

    def get_intent(self, object):
        return copy(self._cxt.get_object_intent(object))

    def get_extent(self, attribute):
        return copy(self._cxt.get_attribute_extent(attribute))

    def add_object(self, object, intent):
        if self._basis.respect_background_knowledge(intent):
            self._cxt.add_object_with_intent(intent, object)
        else:
            raise IllegalContextModification()

class Basis(object):
    _cxt = None
    _background_implications = None
    _basis = None

    def __init__(self, cxt):
        self._cxt = cxt
        self._background_implications = []

    def get_dg_basis(self):
        return fca.compute_dg_basis(self._cxt._cxt, imp_basis=self._background_implications)

    def get_background_implications(self):
        return copy(self._background_implications)

    def add_background_implication(self, imp):
        self._background_implications.append(imp)

    def respect_background_knowledge(self, intent):
        for imp in self._background_implications:
            if not imp.is_respected(intent):
                return False
        return True

class ExplorationSession(object):
    _cxt = None
    _basis = None

    def __init__(self, cxt):
        self._cxt = cxt
        self._basis = Basis(cxt)
        self._cxt.set_basis(self._basis)

    def get_context(self):
        return self._cxt

    context = property(get_context)

    def get_accepted_implications(self):
        return self._basis.get_background_implications()

    def get_candidates(self):
        return self._basis.get_dg_basis()

    def accept_implication(self, imp):
        self._basis.add_background_implication(imp)

    def reject_implication(self, imp, object, intent):
        if not imp.is_respected(intent):
            self._cxt.add_object(object, intent)
        else:
            raise FalseCounterexample()

class Exploration(object):
    _cxt = None

    def __init__(self, cxt):
        self._cxt = copy(cxt)

    def set_context(self, cxt):
        self._cxt = copy(cxt)

    def create_session(self):
        return ExplorationSession(self._cxt)

