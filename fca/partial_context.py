""" Holds class for context with partially given exmaples (partial context) """

import fca.algorithms
from fca import Context
from fca.algorithms.closure_operators import aprime, oprime
from fca.algorithms.closure_operators import simple_closure as closure
from compare_context import subseteq_table
from fca.algorithms.dg_basis import compute_partial_dg_basis
from copy import copy, deepcopy

class PartialContext(object):
    """
    A Partial Context consists of two sets: *objects* and *attributes*
    and of a ternary (x, q) relation between them.
    """
    def __init__(self, x_table, q_table, objects, attributes):
        """
        Create a partial context from cross and question tables
        and list of objects, list of attributes.

        cross_table_x - the list of bool lists representing first context
            (only x in context)
        cross_table_q - the list of bool lists representing second context
            (only questions(q) in context)
                cross_table_x \subseteq cross_table_q
        objects - the list of objects
        attributes - the list of attributes
        """
        if not subseteq_table(x_table, q_table):
            raise ValueError('x table should be \subseteq q table')
        else:
            self.objects = copy(objects)
            self.attributes = copy(attributes)
            self.x_context = Context(x_table, objects[:], self.attributes[:])
            self.q_context = Context(q_table, objects[:], self.attributes[:])

    def __deepcopy__(self, memo):
        return PartialContext(deepcopy(self.x_context._table, memo),
                              deepcopy(self.q_context._table, memo),
                              self.objects[:],
                              self.attributes[:])

    def transpose(self):
        """ Return new partial context with transposed x and q contexts """
        new_objects = self.attributes[:]
        new_attributes = self.objects[:]
        new_x_table = []
        new_q_table = []
        for j in xrange(len(self.attributes)):
            x_line = []
            q_line = []
            for i in xrange(len(self.objects)):
                x_line.append(self.x_context._table[i][j])
                q_line.append(self.q_context._table[i][j])
            new_x_table.append(x_line)
            new_q_table.append(q_line)
        return PartialContext(new_x_table, new_q_table, new_objects, new_attributes)

    def __repr__(self):
        output = ", ".join([str(a) for a in self.attributes]) + "\n"
        output += ", ".join([str(o) for o in self.objects]) + "\n"
        for o in self.objects:
            output += "\n"
            output += self._intent_to_str(self.x_context.get_object_intent(o),
                                          self.q_context.get_object_intent(o))
        return output
        
    def _intent_to_str(self, xintent, qintent):
        line = ""
        for a in self.attributes:
            if a in xintent:
                line += "X"
            elif a in qintent:
                line += "?"
            else:
                line += "."
        return line
        

    def xq_aclosure(self, aset):
        """ +? closure for Partial context """
        oset = aprime(aset, self.x_context)
        return oprime(oset, self.q_context)

    def get_attribute_implications(self,
                                   basis=compute_partial_dg_basis,
                                   confirmed=[],
                                   cond=lambda x: True):
        return basis(self, imp_basis=confirmed, cond=cond)

    def add_object_with_intent(self, intent, name):
        if not intent[0] <= intent[1]:
            raise ValueError('inconsistent partial example')
        self.x_context.add_object_with_intent(intent[0], name)
        self.q_context.add_object_with_intent(intent[1], name)
        self.objects.append(name)
        
    def complete(self, implications):
        for o in self.objects:
            xintent = self.x_context.get_object_intent(o)
            new_xintent = closure(xintent, implications)
            qintent = self.q_context.get_object_intent(o)
            if not new_xintent <= qintent:
                # TODO: undo the modifications
                raise ValueError(
                    'implications are inconsistent with the partial context')
            self.x_context.set_object_intent(new_xintent, o)
            new_qintent = set([a for a in qintent
                                 if a in new_xintent or
                                 closure(new_xintent | set([a]), implications)
                                                                    <= qintent
                             ])
            self.q_context.set_object_intent(new_qintent, o)
            # TODO: Remove printing
            if xintent != new_xintent or qintent != new_qintent:
                print 'Object', o
                print self._intent_to_str(xintent, qintent)
                print 'completed to '
                print self._intent_to_str(new_xintent, new_qintent)
            
    def intents(self):
        for obj in self.objects:
            yield (self.x_context.get_object_intent(obj),
                   self.q_context.get_object_intent(obj))
        