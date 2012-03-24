#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc

class AbstractTriadicContext:
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
    def get_conditions(self):
        return

    conditions = abc.abstractproperty(get_conditions)

    @abc.abstractmethod
    def add_condition(self, condition):
        pass

    @abc.abstractmethod
    def remove_condition(self, condition):
        pass

    @abc.abstractmethod
    def get_dyadic(self, condition):
        return

    @abc.abstractmethod
    def remove_object(self, object):
        pass

    @abc.abstractmethod
    def remove_attribute(self, attribute):
        pass

    @abc.abstractmethod
    def add_object(self, object):
        pass

    @abc.abstractmethod
    def add_attribute(self, attribute):
        pass