#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import fca
import fca.algorithms.exploration2.exploration as expl
from fca import Implication


class ExplorationTest(unittest.TestCase):
    def setUp(self):
        table = [[True, False, False, True],\
            [True, False, True, False],\
            [False, True, True, False],\
            [False, True, True, True]]
        objs = ['1', '2', '3', '4']
        attrs = ['a', 'b', 'c', 'd']
        cxt = expl.ExplorationContext(fca.Context(table, objs, attrs))
        self.cxt = cxt

    def test_exploration_object(self):
        e = expl.Exploration(self.cxt)
        session = e.create_session()

equilateral = 'equilateral'
isosceles = 'isosceles'
acute = 'acute-angled'
right = 'right-angled'

class TrianglesTest(unittest.TestCase):

    def setUp(self):
        table = [[False, True, False, False],
                [False, False, True, False],
                [False, False, False, True]]
        objs = [isosceles, acute, right]
        attrs = [equilateral, isosceles, acute, right]
        cxt = expl.ExplorationContext(fca.Context(table, objs, attrs))
        self.e = expl.Exploration(cxt)

    def test_all(self):
        basis = [
            Implication(set([acute, right]), set([equilateral, isosceles])),
            Implication(set([equilateral]), set([isosceles, acute]))
        ]
        session = self.e.create_session()
        self.assertEqual(len(session.context.objects), 3)



if __name__ == '__main__':
    unittest.main()