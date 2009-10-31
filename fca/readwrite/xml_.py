# -*- coding: utf-8 -*-
"""Holds functions that read a concept system from .xml file"""

import xml.parsers.expat

import fca

def read_xml(path):
    """Read concept system from valid xml file.
    
    Examples
    ========
    
    >>> cs = read_xml('tests/concepts.xml')
    >>> print cs
    (["u'obj1'", "u'obj2'", "u'obj3'"], ["u'attr1'"])
    (["u'obj2'", "u'obj3'"], ["u'attr1'", "u'attr2'"])
    (["u'obj1'"], ["u'attr1'", "u'attr3'"])
    ([], M)
    """
    global new_obj, new_attr, cs
    
    cs = fca.ConceptSystem()
    
    new_obj = None
    new_attr = None
    
    objects = []
    d_objects = {}
    
    attributes = []
    d_attributes = {}
    
    new_intent = []
    new_extent = []
    
    def start_element(name, attrs):
        global new_obj, new_attr
        global new_extent, new_intent
        if name == "object":
            if "id" in attrs.keys():
                new_obj = attrs["id"]
            elif "ref" in attrs.keys():
                new_extent.append(d_objects[attrs["ref"]])
        elif name == "attribute":
            if "id" in attrs.keys():
                new_attr = attrs["id"]
            elif "ref" in attrs.keys():
                new_intent.append(d_attributes[attrs["ref"]])
        elif name == "concept":
            new_intent = []
            new_extent = []
        
    def end_element(name):
        global cs, new_intent, new_extent
        if name == "concept":
            cs.append(fca.Concept(new_extent, new_intent))
            new_extent = []
            new_intent = []
    
    def char_data(data):
        global new_obj, new_attr
        if new_obj:
            d_objects[new_obj] = repr(data)
            objects.append(repr(data))
            new_obj = None
        elif new_attr:
            d_attributes[new_attr] = repr(data)
            attributes.append(repr(data))
            new_attr = None
    
    p = xml.parsers.expat.ParserCreate()
    
    p.StartElementHandler = start_element
    p.EndElementHandler = end_element
    p.CharacterDataHandler = char_data
    
    f = open(path)
    p.ParseFile(f)
    
    return cs


if __name__ == "__main__":
    import doctest
    doctest.testmod()
