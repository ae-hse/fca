#!/usr/bin/env python
# encoding: utf-8
"""
explorationtest.py
"""

import unittest
from exploration import (BasicExploration, NotCounterExamplePremise, 
                        NotCounterExampleConclusion)

import fca


class ExplorationTest(unittest.TestCase):
    def setUp(self):
        table = [[True, False, False, True],\
                 [True, False, True, False],\
                 [False, True, True, False],\
                 [False, True, True, True]]
        objs = ['1', '2', '3', '4']
        attrs = ['a', 'b', 'c', 'd']
        self.exp = BasicExploration(fca.Context(table, objs, attrs))
        
class TestNotEmptyConfirmedList(ExplorationTest):
        
    def test_counter_examples_for_object_implication(self):
        self.exp.confirm_object_implication(1)
        confirmed_implication = self.exp.confirmed_object_implications[0]

        number_of_attrs_before = len(self.exp.context.attributes)
        self.exp.counter_example_for_obj_implication(
                                    'test', set(['3']), 0)
        number_of_attrs_after = len(self.exp.context.attributes)
        self.assertEqual(number_of_attrs_after - number_of_attrs_before, 
                            1, "Number of attributes isn't increased")
                            
        self.failIf(confirmed_implication in self.exp.object_implications)
                            
    def test_counter_examples_for_attribute_implication(self):
        self.exp.confirm_attribute_implication(1)
        confirmed_implication = self.exp.confirmed_attribute_implications[0]
        
        number_of_objects_before = len(self.exp.context.objects)
        self.exp.counter_example_for_attr_implication(
                                    'test', set(['c', 'd']), 0)
        number_of_objects_after = len(self.exp.context.objects)
        self.assertEqual(number_of_objects_after - number_of_objects_before, 
                            1, "Number of objects isn't increased")
                            
        self.failIf(confirmed_implication in self.exp.attribute_implications)
           
class TestExplorationInitialization(ExplorationTest):
    """docstring for TestExplorationInitialization"""
    def runTest(self):
        self.assertEqual(len(self.exp.attribute_implications), 3,
                         "Wrong number of attribute implications")
        self.assertEqual(len(self.exp.object_implications), 3,
                         "Wrong number of object implications")
                         
class TestImplicationsConfirming(ExplorationTest):
    
    def test_object_implication_confirm(self):
        self.exp.confirm_attribute_implication(0)
        self.assertEqual(len(self.exp.attribute_implications), 2,
                         "Wrong number of attribute implications")
        self.assertEqual(len(self.exp.confirmed_attribute_implications), 1,
                         "Wrong number of confirmed attribute implications")
                         
        self.exp.confirm_object_implication(0)
        self.assertEqual(len(self.exp.object_implications), 2,
                         "Wrong number of object implications")
        self.assertEqual(len(self.exp.confirmed_object_implications), 1,
                         "Wrong number of object attribute implications")
        
class TestCounterExample(ExplorationTest):
    
    def test_providing_wrong_counter_examples(self):
        self.assertRaises(
            NotCounterExamplePremise,
            self.exp.counter_example_for_attr_implication,
            'test', set(['c']), 0
        )
        self.assertRaises(
            NotCounterExamplePremise,
            self.exp.counter_example_for_attr_implication,
            'test', set(['c', 'b']), 0
        )
        self.assertRaises(
            NotCounterExampleConclusion,
            self.exp.counter_example_for_attr_implication,
            'test', set(['c', 'd', 'b']), 0
        )
        self.assertRaises(
            NotCounterExamplePremise,
            self.exp.counter_example_for_obj_implication,
            'test', set(['1']), 0
        )
        self.assertRaises(
            NotCounterExamplePremise,
            self.exp.counter_example_for_obj_implication,
            'test', set(['1', '2']), 0
        )
        self.assertRaises(
            NotCounterExampleConclusion,
            self.exp.counter_example_for_obj_implication,
            'test', set(['3', '4']), 0
        )
        
    def test_correct_counter_example_for_attribute_implication(self):
        number_of_objects_before = len(self.exp.context.objects)
        self.exp.counter_example_for_attr_implication(
                                    'test', set(['c', 'd']), 0)
        number_of_objects_after = len(self.exp.context.objects)
        self.assertEqual(number_of_objects_after - number_of_objects_before, 
                            1, "Number of objects isn't increased")
                            
    def test_correct_counter_example_for_object_implication(self):
        number_of_attrs_before = len(self.exp.context.attributes)
        self.exp.counter_example_for_obj_implication(
                                    'test', set(['3']), 0)
        number_of_attrs_after = len(self.exp.context.attributes)
        self.assertEqual(number_of_attrs_after - number_of_attrs_before, 
                            1, "Number of attributes isn't increased")

    
if __name__ == '__main__':
    unittest.main()