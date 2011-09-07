#
#  conceptual_exploration.py
#  
#
#  Created by object on 3/13/11.
#  Copyright (c) 2011 __MyCompanyName__. All rights reserved.
#

class WrongCounterExample(ExplorationException):
    pass


class Exploration(object):

    def __init__(self, db, expert):
        self.db = db
        self.expert = expert
            
    def confirm_implication(self, impl):
        self.db.add_implication(impl)
        
    def reject_implication(self, impl):
        counterexample = self.expert.provide_counterexample(impl)
        if self.db.respects(counterexample, impl):
            raise WrongCounterExample()
        self.db.add_example(counterexample)
        
    def on_context_update(self):
        