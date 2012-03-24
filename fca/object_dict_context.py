#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy

import fca

class ObjectDictContext(fca.AbstractContext):
    _object_dict = dict()
    _attributes = set()

    def __init__(self, attributes):
        self._attributes = copy(attributes)

    def get_objects(self):
        return self._object_dict.keys()

    objects = property(get_objects)

    def get_attributes(self):
        return copy(self._attributes)

    attributes = property(get_attributes)

    def get_intent(self, object):
        return copy(self._object_dict[object])

    def get_extent(self, attribute):
        return {obj for obj in self._object_dict if attribute in self._object_dict[obj]}

    def set_intent(self, object, intent):
        if object not in self._object_dict:
            raise Exception("Unknown object")
        self._object_dict[object] = copy(intent)

    def set_extent(self, attribute, extent):
        if attribute not in self._attributes:
            raise Exception("Unknown attribute")
        for obj in self._object_dict:
            self._object_dict[obj].add(attribute)

    def add_object(self, object, intent):
        if object not in self._object_dict:
            self._object_dict[object] = copy(intent)
        else:
            raise Exception("Object is already exist in this context")

    def add_attribute(self, attribute, extent):
        if attribute not in self._attributes:
            self._attributes.add(attribute)
            for obj in extent:
                self._object_dict[obj].add(attribute)
        else:
            raise Exception("Attribute is already exist in this context")

    def remove_object(self, object):
        del self._object_dict[object]

    def remove_attribute(self, attribute):
        self._attributes.remove(attribute)
        for obj in self._object_dict:
            self._object_dict[obj].remove(attribute)

    def oprime(self, objects):
        if not len(objects):
            return copy(self._attributes)
        return set.intersection(*[self._object_dict[obj] for obj in objects])

    def aprime(self, attributes):
        return {obj for obj in self._object_dict if self._object_dict[obj] >= attributes}

    def oclosure(self, objects):
        return self.aprime(self.oprime(objects))

    def aclosure(self, attributes):
        return self.oprime(self.aprime(attributes))