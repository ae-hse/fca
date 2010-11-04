# -*- coding: utf-8 -*-
"""Reading many-valued contexts from comma-separated text files"""

import csv
import fca

def read_mv_csv(path):
    """Read many-valued context from path, which is comma-separated text file

    Format
    ======

    First line consists of comma-separated attribute names.
    Then comma-separated values, each line corresponds to one object.
    The first value in each line is an object name.

    Examples
    ========

    Load example file from tests directory

    >>> c = read_mv_csv('tests/table.csv')
    >>> len(c)
    3
    >>> len(c[0])
    3
    >>> for o in c:
    ...     print o
    ...
    ['7', '6', '7']
    ['7', '2', '9']
    ['1', '3', '4']
    >>> print c.objects
    ['obj1', 'obj2', 'obj3']
    >>> print c.attributes
    ['attr1', 'attr2', 'attr3']

    """
    input_file = open(path, "rb")
    rdr = csv.reader(input_file, delimiter=",")
    
    objects = []
    
    rec = rdr.next() # read attributes names

    attributes = []
    for attr in rec:
        attributes.append(str(attr).strip())
        
    table = []
    for rec in rdr:
        objects.append(str(rec[0]).strip())
        line = []
        for val in rec[1:]:
            line.append(val)
        table.append(line)
    input_file.close()

    return fca.ManyValuedContext(table, objects, attributes)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
    

