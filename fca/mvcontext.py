# -*- coding: utf-8 -*-
"""
Holds class for many valued context
"""

from fca import Context

class ManyValuedContext(Context):
    """
    Many valued context.

    Examples
    ========

    Create a context.

    >>> t = [[2, 1, 2, 3],\
              [1, 2, 3, 1],\
              [2, 1, 3, 1],\
              [2, 3, 3, 2]]
    >>> objs = [1, 2, 3, 4]
    >>> attrs = ['a', 'b', 'c', 'd']
    >>> c = ManyValuedContext(t, objs, attrs)
    >>> c[0][0]
    2
    >>> c[0][2]
    2
    >>> 1 in c.objects
    True
    >>> 'f' in c.attributes
    False
    >>> for o in c:
    ...     print o
    ...     break
    ...
    [2, 1, 2, 3]

    Class emulates container type.

    >>> len(c)
    4
    >>> c[1]
    [1, 2, 3, 1]
    """

    def __init__(self, table=[], objects=[], attributes=[]):
        """Create a many valued context from table and list of objects, list
        of attributes
        
        table - list of attribute values lists
        objects - the list of objects
        attributes - the list of attributes 
        """
        if len(table) != len(objects):
            raise ValueError("Number of objects (=%i) and number of cross table"
                   " rows(=%i) must agree" % (len(objects), len(table)))
        elif (len(table) != 0) and len(table[0]) != len(attributes):
            raise ValueError("Number of attributes (=%i) and number of cross table"
                    " columns (=%i) must agree" % (len(attributes),
                        len(table[0])))

        self._table = table
        self._objects = objects
        self._attributes = attributes

    def get_objects(self):
        return self._objects

    objects = property(get_objects)

    def get_attributes(self):
        return self._attributes
        
    attributes = property(get_attributes)

    def extract_subcontext(self, attribute_names):
        """Create a subcontext with only indicated attributes"""
        return ManyValuedContext(self._extract_subtable(attribute_names),
                                self.objects,
                                attribute_names)
                                
    def extract_subcontext_by_condition(self, condition):
        """Extract a subcontext containing only objects that satisfy the
        condition.
        
        Keyword arguments:
        condition(object_index) -- a function that takes an an object index and
            returns a Boolean value
        
        """
        object_names, table = self._extract_subtable_by_condition(condition)
        return ManyValuedContext(table, object_names, self.attributes)
                                
    def extract_subcontext_by_attribute_values(self, values):
        """Extract a subcontext containing only objects with certain attribute
        values.
        
        Keyword arguments:
        values -- an attribute-value dictionary
        
        """
        object_names, table = self._extract_subtable_by_attribute_values(values)
        return ManyValuedContext(table, object_names, self.attributes)
                            

    ############################
    # Emulating container type #
    ############################

    def __len__(self):
        return len(self._table)

    def __getitem__(self, key):
        return self._table[key]

    ############################

if __name__ == "__main__":
    import doctest
    doctest.testmod()
