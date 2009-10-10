# -*- coding: utf-8 -*-
"""
Holds scale class for conceptual scaling
"""

from context import Context

class Scale(Context):
    """
    Scale inherited from the Context used for conceptual scaling.
    
    Examples
    ========
    
    >>> ct = [[True, False],\
              [False, True]]
    >>> objs = ['value>7', 'value<2']
    >>> attrs = ['>7', '<2']
    >>> c = Context(ct, objs, attrs)
    >>> s = Scale(c)
    
    """

    def __init__(self, context):
        """
        Constructor
        """
        super(Scale, self).__init__(context._table,
                                    context._objects,
                                    context._attributes)
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()
        