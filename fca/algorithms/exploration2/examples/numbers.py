#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fca.algorithms.exploration2.exploration import *

def is_prime(n):
    for m in xrange(n - 1, 1, -1):
        if n % m == 0:
            return False

    return True

def is_factorial(n):
    f = 1
    for m in xrange(1, n + 1):
        f *= m
        if f == n:
            return True
        if f > n:
            return False



class CommandLineExploration(Exploration):
    def __init__(self):
        self.d = {
            "even" : lambda n: n % 2 == 0,
            "odd" : lambda n: n % 2 == 1,
            "divided_by_three" : lambda n: n % 3 == 0,
            "prime" : is_prime,
            "factorial" : is_factorial
        }

        cxt = fca.Context(attributes=list(self.d.keys()))

        super(CommandLineExploration, self).__init__(ExplorationContext(cxt))
        self._session = self.create_session()

    def is_valid(self, imp):
        print "{0}".format(imp)
        return input('Is the following implication valid? Enter "True" or "False":\n'.format(imp))

    def ask_for_counterexample(self):
        return input('Provide counterexample:')

    def get_intent(self, number):
        return {attr for attr in self._cxt.attributes if self.d[attr](number) }

    def explore(self):
        while self._session.get_candidates():
            imp = self._session.get_candidates()[0]
            if self.is_valid(imp):
                self._session.accept_implication(imp)
            else:
                counterexample = self.ask_for_counterexample()
                intent = self.get_intent(counterexample)
                print intent
                self._session.reject_implication(imp, counterexample, intent)

if __name__ == "__main__":
    CommandLineExploration().explore()




