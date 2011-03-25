#!/usr/bin/env python
# encoding: utf-8
import unittest

from exploration import (AttributeExploration, ExplorationDB, 
                        NotCounterexample, IllegalContextModification)
import fca

class DummyPerfectExpert(object):
        
    def provide_counterexample(self, imp):
        return ('test', imp.premise)
        
class DummyFoolishExpert(object):

    def provide_counterexample(self, imp):
        return ('test', imp.premise | imp.conclusion)

class ExplorationTest(unittest.TestCase):
    def setUp(self):
        table = [[True, False, False, True],\
                 [True, False, True, False],\
                 [False, True, True, False],\
                 [False, True, True, True]]
        objs = ['1', '2', '3', '4']
        attrs = ['a', 'b', 'c', 'd']
        cxt = fca.Context(table, objs, attrs)
        self.db = ExplorationDB(cxt, list())
        
class InitializationTest(ExplorationTest):
    
    def test_with_perfect_expert(self):
        expert = DummyPerfectExpert()
        exploration = AttributeExploration(self.db, expert)
        self.assertEqual(len(self.db.open_implications), 3,
                         "Wrong number of attribute implications")
        
    def test_with_foolish_expert(self):
        expert = DummyFoolishExpert()
        exploration = AttributeExploration(self.db, expert)
        self.assertEqual(len(self.db.open_implications), 3,
                         "Wrong number of attribute implications")
        
class ConfirmingImplicationsTest(ExplorationTest):
    
    def test_implication_confirm(self):
        expert = DummyPerfectExpert()
        exploration = AttributeExploration(self.db, expert)
        exploration.confirm_implication(self.db.open_implications[0])
        self.assertEqual(len(self.db.base), 1)
        self.assertEqual(len(self.db.open_implications), 2)
        
class RejectingImplicationTest(ExplorationTest):
    
    def test_correct_implication_reject(self):
        expert = DummyPerfectExpert()
        exploration = AttributeExploration(self.db, expert)
        exploration.reject_implication(self.db.open_implications[0])
        self.assertEqual(len(self.db._cxt.objects), 5)
        
    def test_incorrect_implication_reject(self):
        expert = DummyFoolishExpert()
        exploration = AttributeExploration(self.db, expert)
        self.assertRaises(
            NotCounterexample,
            exploration.reject_implication,
            self.db.open_implications[0]    
        )
        self.assertEqual(len(self.db._cxt.objects), 4)
        
class AddExampleTest(ExplorationTest):
    
    def test_add_correct_example(self):
        expert = DummyPerfectExpert()
        exploration = AttributeExploration(self.db, expert)
        exploration.confirm_implication(self.db.open_implications[0])
        imp = self.db.open_implications[0]
        intent = imp.premise | imp.conclusion
        self.db.add_example('test', intent)
        self.assertEqual(len(self.db._cxt.objects), 5)
        
    def test_add_incorrect_example(self):
        expert = DummyPerfectExpert()
        exploration = AttributeExploration(self.db, expert)
        exploration.confirm_implication(self.db.open_implications[0])
        imp = self.db.base[0]
        intent = imp.premise
        self.assertRaises(
            IllegalContextModification,
            self.db.add_example,
            'test', intent
        )
        self.assertEqual(len(self.db._cxt.objects), 4)
        
if __name__ == '__main__':
    unittest.main()