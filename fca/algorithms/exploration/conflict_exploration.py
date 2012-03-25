#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fca

class ConflictExploration(object):

    class NoSuchObject(object):
        pass

    class ConflictContextProxy(fca.TriadicExplorationContext.DyadicExplorationContextProxy):
        def get_attributes(self):
            return super(ConflictContextProxy, self).get_attributes() - {self._triadic_context.NoSuchObject}

        def challenge_object(self, object):
            self.set_intent(object, self._triadic_context.attributes)

    _cxt = fca.TriadicExplorationContext({NoSuchObject}, set())
    _cxt._dyadic_proxy_class = ConflictContextProxy

    def get_accepted_objects(self):
        return self._cxt.get_conditionally_equal_objects()

    def get_controversial_objects(self):
        return self._cxt.attributes - self.get_accepted_objects()

    def get_accepted_implications(self):
        return set.union(*[self._cxt._background_implications[condition]
                           for condition in self._cxt._background_implications])

    def filter_generally_true_implications(self, implications):
        return {imp for imp in implications if self._cxt.is_generally_true(imp)}

    def get_context(self, expert):
        return self._cxt.get_dyadic(expert)

