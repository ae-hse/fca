#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy

class ExplorationException(Exception):
    pass

class FalseCounterexample(ExplorationException):
    pass

class ExplorationSession(object):
    _cxt = None
    _basis = None

    def __init__(self, cxt):
        self._cxt = cxt

    def get_context(self):
        return self._cxt

    context = property(get_context)

    def get_accepted_implications(self):
        return self._cxt.get_background_implications()

    def get_candidates(self):
        return self._cxt.get_relative_basis()

    def accept_implication(self, imp):
        self._cxt.add_background_implication(imp)

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