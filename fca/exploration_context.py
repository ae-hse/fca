#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy

import fca
import fca.algorithms

class ExplorationContext(fca.AbstractContext):
    """Exploration mix-in"""
    _background_implications = list()
    __fca_basis_function = fca.algorithms.compute_dg_basis
    _relative_basis = list()
    _relative_basis_recompute_flag = True

    def _check_intent(self, intent):
        for imp in self._background_implications:
            if not imp.is_respected(intent):
                raise Exception("Attempted context modification conflicts with existing background knowledge")

    def get_background_implications(self):
        return copy(self._background_implications)

    def get_relative_basis(self):
        if self._relative_basis_recompute_flag:
            self._relative_basis = self.__fca_basis_function(imp_basis=self._background_implications)
            self._relative_basis_recompute_flag = False
        return copy(self._relative_basis)

    def add_background_implication(self, imp):
        self._background_implications.append(imp)
        self._relative_basis_recompute_flag = True

    def set_intent(self, object, intent):
        self._check_intent(intent)
        self._relative_basis_recompute_flag = True
        super(ExplorationContext, self).set_intent(object, intent)

    def set_extent(self, attribute, extent):
        self._relative_basis_recompute_flag = True
        super(ExplorationContext, self).set_extent(attribute, extent)

    def add_object(self, object, intent):
        self._check_intent(intent)
        self._relative_basis_recompute_flag = True
        super(ExplorationContext, self).add_object(object, intent)

    def add_attribute(self, attribute, extent):
        self._relative_basis_recompute_flag = True
        super(ExplorationContext, self).add_attribute(attribute, extent)

    def remove_object(self, object):
        self._relative_basis_recompute_flag = True
        super(ExplorationContext, self).remove_object(object)

    def remove_attribute(self, attribute):
        self._relative_basis_recompute_flag = True
        super(ExplorationContext, self).remove_attribute(attribute)