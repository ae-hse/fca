#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy

import fca
from fca.triadic_exploration_context import TriadicExplorationContext
from exploration import ExplorationSession

class ConflictExploration(object):

    class NoSuchObject(object):
        pass

    class ConflictContextProxy(TriadicExplorationContext.DyadicExplorationContextProxy):
        def get_attributes(self):
            return super(ConflictContextProxy, self).get_attributes() - {self._triadic_context.NoSuchObject}

        def challenge_object(self, object):
            self.set_intent(object, self._triadic_context.attributes)

    _cxt = TriadicExplorationContext({NoSuchObject}, set())
    _cxt._dyadic_proxy_class = ConflictContextProxy

    def __init__(self, attributes):
        super(ConflictExploration, self).__init__()
        self._cxt = TriadicExplorationContext(attributes | {self.NoSuchObject}, set())

    def get_accepted_objects(self):
        return self._cxt.get_conditionally_equal_objects()

    def get_controversial_objects(self):
        return self._cxt.attributes - self.get_accepted_objects()

    def get_accepted_implications(self):
        return set.union(*[self._cxt._background_implications[condition]
                           for condition in self._cxt._background_implications])

    def filter_generally_true_implications(self, implications):
        return {imp for imp in implications if self._cxt.is_generally_true(imp)}

    def create_session(self, expert):
        return ExplorationSession(self._cxt.get_dyadic(expert))

    def get_experts(self):
        return copy(self._cxt.conditions)

    experts = property(get_experts)

    def add_expert(self, expert):
        self._cxt.add_condition(expert)

if __name__ == "__main__":
    e = fca.algorithms.exploration.ConflictExploration({"a", "b", "c", "d"})
    e.add_expert("E1")
    e.add_expert("E2")

    session = e.create_session("E1")
    print session.get_candidates()
