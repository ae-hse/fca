#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy

import fca
import abstract_triadic_context

class TriadicContext(abstract_triadic_context.AbstractTriadicContext):
    """

    Examples
    ========

    >>> t_context = TriadicContext({"B", "M", "R", "K", "S"}, {"VEG", "NO PORK", "ALCO", "NONE"})
    >>> t_context.add_object("MON")
    >>> t_context.add_object("TUE")
    >>> t_context.add_object("WED")
    >>> t_context.add_object("THU")
    >>> t_context.add_object("FRI")
    >>> d_context = t_context.get_dyadic("VEG")
    >>> d_context.set_intent("MON", {"B", "M", "R", "K", "S"})
    >>> d_context.set_intent("TUE", {"B", "R", "K"})
    >>> d_context.set_intent("WED", {"B", "R", "K", "S"})
    >>> d_context.set_intent("THU", {"B", "R", "K"})
    >>> d_context.set_intent("FRI", {"B", "M", "R", "K", "S"})
    >>> d_context = t_context.get_dyadic("NO PORK")
    >>> d_context.set_intent("MON", {"B", "M", "K"})
    >>> d_context.set_intent("TUE", {"M", "R"})
    >>> d_context.set_intent("WED", {"B", "R", "K"})
    >>> d_context.set_intent("THU", {"B", "M", "R", "K"})
    >>> d_context.set_intent("FRI", {"R", "K"})
    >>> d_context = t_context.get_dyadic("ALCO")
    >>> d_context.set_intent("MON", {"R"})
    >>> d_context.set_intent("TUE", {"M"})
    >>> d_context.set_intent("WED", {})
    >>> d_context.set_intent("THU", {})
    >>> d_context.set_intent("FRI", {"K"})
    >>> d_context = t_context.get_dyadic("NONE")
    >>> d_context.set_intent("MON", {"B", "M"})
    >>> d_context.set_intent("TUE", {"B", "M", "R", "K", "S"})
    >>> d_context.set_intent("WED", {"B", "M"})
    >>> d_context.set_intent("THU", {"B", "M", "S"})
    >>> d_context.set_intent("FRI", {"B", "M", "R"})
    >>> print t_context
    S, R, M, K, B
    THU, WED, FRI, MON, TUE
    THU: { NONE } { VEG, NO PORK } { NO PORK, NONE } { VEG, NO PORK } { VEG, NO PORK, NONE }
    WED: { VEG } { VEG, NO PORK } { NONE } { VEG, NO PORK } { VEG, NO PORK, NONE }
    FRI: { VEG } { VEG, NO PORK, NONE } { VEG, NONE } { VEG, NO PORK, ALCO } { VEG, NONE }
    MON: { VEG } { VEG, ALCO } { VEG, NO PORK, NONE } { VEG, NO PORK } { VEG, NO PORK, NONE }
    TUE: { NONE } { VEG, NO PORK, NONE } { ALCO, NO PORK, NONE } { VEG, NONE } { VEG, NONE }
    """
    class DyadicContextProxy(fca.AbstractContext):
        _triadic_context = None
        _condition = None

        def __init__(self, triadic_context, condition):
            self._triadic_context = triadic_context
            self._condition = condition

        def get_objects(self):
            return self._triadic_context.objects

        objects = property(get_objects)

        def get_attributes(self):
            return self._triadic_context.attributes

        attributes = property(get_attributes)

        def get_intent(self, object):
            return {attr for attr in self._triadic_context._object_dict[object]
                    if self._condition in self._triadic_context._object_dict[object][attr]}

        def get_extent(self, attribute):
            return {obj for obj in self._triadic_context._object_dict
                    if self._condition in self._triadic_context._object_dict[obj][attribute]}

        def set_intent(self, object, intent):
            if object not in self._triadic_context._object_dict:
                raise Exception("Unknown object")
            for attr in intent:
                if attr in self._triadic_context._object_dict[object]:
                    self._triadic_context._object_dict[object][attr].add(self._condition)
                else:
                    self._triadic_context._object_dict[object][attr] = {self._condition}

        def set_extent(self, attribute, extent):
            if attribute not in self._triadic_context._attributes:
                raise Exception("Unknown attribute")
            for obj in extent:
                if attribute in self._triadic_context._object_dict[obj]:
                    self._triadic_context._object_dict[obj][attribute].add(self._condition)
                else:
                    self._triadic_context._object_dict[obj][attribute] = {self._condition}

        def add_object(self, object, intent):
            if object not in self._triadic_context._object_dict:
                self._triadic_context.add_object(object)
                self.set_intent(object, intent)
            else:
                raise Exception("Object is already exist in this context")

        def add_attribute(self, attribute, extent):
            if attribute not in self._triadic_context._attributes:
                self._triadic_context.add_attribute(attribute)
                self.set_extent(attribute, extent)
            else:
                raise Exception("Attribute is already exist in this context")

        def remove_object(self, object):
            self._triadic_context.remove_object(object)

        def remove_attribute(self, attribute):
            self._triadic_context.remove_object(attribute)

        def oprime(self, objects):
            if not len(objects):
                return copy(self._triadic_context._attributes)
            return set.intersection(*[self.get_intent(obj) for obj in objects])

        def aprime(self, attributes):
            if not len(attributes):
                return copy(self.objects)
            return set.intersection(*[self.get_extent(attr) for attr in attributes])

        def oclosure(self, objects):
            return self.aprime(self.oprime(objects))

        def aclosure(self, attributes):
            return self.oprime(self.aprime(attributes))

    _dyadic_proxy_class = DyadicContextProxy
    _conditions = set()
    _attributes = set()
    _object_dict = dict()

    def __init__(self, attributes, conditions):
        self._conditions = copy(conditions)
        self._attributes = copy(attributes)

    def get_objects(self):
        return copy(self._object_dict.keys())

    objects = property(get_objects)

    def get_attributes(self):
        return copy(self._attributes)

    attributes = property(get_attributes)

    def get_conditions(self):
        return copy(self._conditions)

    conditions = property(get_conditions)

    def add_condition(self, condition):
        self._conditions.add(condition)

    def remove_condition(self, condition):
        self._conditions.remove(condition)
        for obj in self._object_dict:
            for attr in self._attributes:
                if attr in self._object_dict[obj]:
                    self._object_dict[obj][attr].remove(condition)

    def get_dyadic(self, condition):
        if condition not in self._conditions:
            raise Exception("No such condition")
        return self._dyadic_proxy_class(self, condition)

    def remove_object(self, object):
        del self._object_dict[object]

    def remove_attribute(self, attribute):
        self._attributes.remove(attribute)
        for obj in self_object_dict:
            if attribute in self._object_dict[obj]:
                del self._object_dict[obj][attribute]

    def add_object(self, object):
        self._object_dict[object] = dict()

    def add_attribute(self, attribute):
        self._attributes.add(attribute)

    def __str__(self):
        s = ", ".join(self._attributes) + "\n"
        s += ", ".join(self._object_dict.keys()) + "\n"
        for obj in self._object_dict:
            s += obj + ": "
            for attr in self._attributes:
                if attr in self._object_dict[obj]:
                    s += "{ " + ", ".join(self._object_dict[obj][attr]) + " } "
                else:
                    s += "{} "
            s += "\n"

        return s[:-1]

if __name__ == "__main__":
    import doctest
    doctest.testmod()