#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections

from copy import copy

class TriadicContext(collections.Mapping, collections.Sized):
    _attributes = set()
    _objects = set()

    def get_attributes(self):
        return copy(self._attributes)

    attributes = property(get_attributes)

    def get_objects(self):
        return copy(self._objects)

    objects = property(get_objects)

    def get_conditions(self):
        return copy(self.keys())

    conditions = property(get_conditions)

    _conditions_dict = dict()

    def __getitem__(self, item):
        return self._conditions_dict[item]

    def __delitem__(self, key):
        self._conditions_dict.__delitem__(key)

    def __len__(self):
        return len(self._conditions_dict)
