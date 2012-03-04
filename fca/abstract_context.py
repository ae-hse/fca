#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc

class AbstractContext:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_objects(self):
        return

    objects = abc.abstractproperty(get_objects)

    @abc.abstractmethod
    def get_attributes(self):
        return

    attributes = abc.abstractproperty(get_attributes)

    @abc.abstractmethod
    def get_intent(self, object):
        return

    @abc.abstractmethod
    def get_extent(self, attribute):
        return

    @abc.abstractmethod
    def set_intent(self, object, intent):
        pass

    @abc.abstractmethod
    def set_extent(self, attribute, extent):
        pass

    @abc.abstractmethod
    def add_object(self, object, intent):
        pass

    @abc.abstractmethod
    def add_attribute(self, attribute, extent):
        pass

    @abc.abstractmethod
    def remove_object(self, object):
        pass

    @abc.abstractmethod
    def remove_attribute(self, attribute):
        pass

    @abc.abstractmethod
    def oprime(self, objects):
        return

    @abc.abstractmethod
    def aprime(self, attributes):
        return

    @abc.abstractmethod
    def oclosure(self, objects):
        return

    @abc.abstractmethod
    def aclosure(self, attributes):
        return
