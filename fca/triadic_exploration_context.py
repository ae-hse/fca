#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy

import fca.abstract_context
import fca.algorithms.dg_basis
import fca

class TriadicExplorationContext(fca.TriadicContext):
    _background_implications = dict()
    __fca_basis_function = fca.algorithms.dg_basis.compute_dg_basis
    _relative_basis = dict()
    _relative_basis_recompute_flag = dict()

    class DyadicExplorationContextProxy(fca.TriadicContext.DyadicContextProxy):
        def _check_intent(self, intent):
            for imp in self._triadic_context._background_implications[self._condition]:
                if not imp.is_respected(intent):
                    raise Exception("Attempted context modification conflicts with existing background knowledge")

        def get_background_implications(self):
            return copy(self._triadic_context._background_implications[self._condition])

        def get_relative_basis(self):
            if self._triadic_context._relative_basis_recompute_flag[self._condition]:
                self._triadic_context._relative_basis = self._triadic_context.__fca_basis_function(
                    imp_basis=self._triadic_context._background_implications)
                self._triadic_context._relative_basis_recompute_flag[self._condition] = False
            return copy(self._triadic_context._relative_basis[self._condition])

        def add_background_implication(self, imp):
            self._triadic_context._background_implications.append(imp)
            self._triadic_context._relative_basis_recompute_flag[self._condition] = True

        def set_intent(self, object, intent):
            self._check_intent(intent)
            self._triadic_context._relative_basis_recompute_flag[self._condition] = True
            super(DyadicExplorationContextProxy, self).set_intent(object, intent)

        def set_extent(self, attribute, extent):
            self._triadic_context._relative_basis_recompute_flag[self._condition] = True
            super(DyadicExplorationContextProxy, self).set_extent(attribute, extent)

        def add_object(self, object, intent):
            self._check_intent(intent)
            self._triadic_context._relative_basis_recompute_flag[self._condition] = True
            super(DyadicExplorationContextProxy, self).add_object(object, intent)

        def add_attribute(self, attribute, extent):
            self._triadic_context._relative_basis_recompute_flag[self._condition] = True
            super(DyadicExplorationContextProxy, self).add_attribute(attribute, extent)

        def remove_object(self, object):
            self._triadic_context._relative_basis_recompute_flag[self._condition] = True
            super(DyadicExplorationContextProxy, self).remove_object(object)

        def remove_attribute(self, attribute):
            self._triadic_context._relative_basis_recompute_flag[self._condition] = True
            super(DyadicExplorationContextProxy, self).remove_attribute(attribute)