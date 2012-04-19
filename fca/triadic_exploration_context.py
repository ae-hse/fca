#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy

import fca.triadic_context
import fca.abstract_context
from fca.algorithms.dg_basis import compute_dg_basis
import triadic_context
from fca.utils.context_utils import union_contexts
from fca.object_dict_context import ObjectDictContext

class TriadicExplorationContext(triadic_context.TriadicContext):
    _background_implications = dict()
    _fca_basis_function = compute_dg_basis
    _relative_basis = dict()
    _relative_basis_recompute_flag = dict()

    def is_generally_true(self, implication):
        for condition in self.conditions:
            d_context = self.get_dyadic(condition)
            for object in self.objects:
                if not implication.is_respected(d_context.get_intent(object)):
                    return False
        return True

    def get_super_dyadic(self):
        return union_contexts(ObjectDictContext(self.attributes),
            {self.get_dyadic(condition) for condition in self.conditions})

    def get_universally_true_implications(self):
        super_cxt = self.get_super_dyadic()
        basis = TriadicExplorationContext._fca_basis_function
        return basis(super_cxt)

    def get_conditionally_equal_attributes(self, conditions = None):
        if not conditions:
            conditions = self.conditions
        result = set()

        for attr in self.attributes:
            first_extent= None
            accept = True
            for condition in conditions:
                d_cxt = self.get_dyadic(condition)
                if not first_extent:
                    first_extent = d_cxt.get_extent(attr)
                extent = d_cxt.get_extent(attr)
                if extent != first_extent:
                    accept = False
                    break

            if accept:
                result.add(attr)

        return result

    def get_extentionally_equal_dyadic(self, conditions=None):
        if not conditions:
            conditions = self.conditions

        sub_cxt = fca.ObjectDictContext(set())

        if len(conditions) > 0:
            d_cxt = self.get_dyadic(conditions[0])

        for attr in self.get_conditionally_equal_attributes(conditions):
            sub_cxt.add_attribute(attr, d_cxt.get_extent(obj))

        return sub_cxt

    def get_conditionally_equal_objects(self, conditions=None):
        if not conditions:
            conditions = self.conditions

        result = set()

        for obj in self.objects:
            first_intent = None
            accept = True
            for condition in conditions:
                d_cxt = self.get_dyadic(condition)
                if not first_intent:
                    first_intent = d_cxt.get_intent(obj)
                intent = d_cxt.get_intent(obj)
                if intent != first_intent:
                    accept = False
                    break

            if accept:
                result.add(obj)

        return result

    def get_intentionally_equal_dyadic(self, conditions=None):
        if not conditions:
            conditions = self.conditions

        sub_cxt = fca.ObjectDictContext(self.attributes)

        if len(conditions) > 0:
            d_cxt = self.get_dyadic(conditions[0])

        for obj in self.get_conditionally_equal_objects(conditions):
            sub_cxt.add_object(obj, d_cxt.get_intent(obj))

        return sub_cxt

    def get_dyadic(self, condition):
        if condition not in self._background_implications:
            self._background_implications[condition] = list()

        if condition not in self._relative_basis:
            self._relative_basis[condition] = list()

        if condition not in self._relative_basis_recompute_flag:
            self._relative_basis_recompute_flag[condition] = True

        return super(TriadicExplorationContext, self).get_dyadic(condition)


    class DyadicExplorationContextProxy(fca.triadic_context.TriadicContext.DyadicContextProxy):
        _fca_basis_function = compute_dg_basis
        def _check_intent(self, intent):
            for imp in self._triadic_context._background_implications[self._condition]:
                if not imp.is_respected(intent):
                    raise Exception("Attempted context modification conflicts with existing background knowledge")

        def get_background_implications(self):
            return copy(self._triadic_context._background_implications[self._condition])

        def get_relative_basis(self):
            if self._triadic_context._relative_basis_recompute_flag[self._condition]:
                self._triadic_context._relative_basis[self._condition] = self._fca_basis_function(
                    imp_basis=self._triadic_context._background_implications[self._condition])
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

    _dyadic_proxy_class = DyadicExplorationContextProxy