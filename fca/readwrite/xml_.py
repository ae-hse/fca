# -*- coding: utf-8 -*-
"""Holds functions that read a concept system from .xml file"""

from xml.dom.minidom import getDOMImplementation
import xml.parsers.expat

import fca

def write_xml(path, cs):
    """Write concept system to xml document
    
    Examples
    ========
    
    >>> from fca import ConceptLattice
    >>> c = fca.read_cxt('tests/context.cxt')
    >>> cs = ConceptLattice(c)
    >>> write_xml("tests/test.xml", cs)
    """
    objects = list(cs.get_top_concept().extent)
    attributes = list(cs.get_bottom_concept().intent)
    
    objects_ids = dict([(objects[i], "o{0}".format(i+1))  for i in xrange(len(objects))])
    attributes_ids = dict([(attributes[i], "a{0}".format(i+1))  for i in xrange(len(attributes))])
    
    out = file(path, "wb")

    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, "conceptsystem", None)
    top_element = newdoc.documentElement
    
    element = newdoc.createElement("objects")
    for obj in objects:
        obj_element = newdoc.createElement("object")
        obj_element.setAttribute("id", objects_ids[obj])
        textnode = newdoc.createTextNode(obj)
        obj_element.appendChild(textnode)
        element.appendChild(obj_element)
    top_element.appendChild(element)
    
    element = newdoc.createElement("attributes")
    for attr in attributes:
        attr_element = newdoc.createElement("attribute")
        attr_element.setAttribute("id", attributes_ids[attr])
        textnode = newdoc.createTextNode(attr)
        attr_element.appendChild(textnode)
        element.appendChild(attr_element)
    top_element.appendChild(element)
    
    element = newdoc.createElement("concepts")
    for concept in cs:
        c_element = newdoc.createElement("concept")
        
        e_element = newdoc.createElement("extent")
        for obj in concept.extent:
            obj_element = newdoc.createElement("object")
            obj_element.setAttribute("ref", objects_ids[obj])
            e_element.appendChild(obj_element)
            
        c_element.appendChild(e_element)
        
        i_element = newdoc.createElement("intent")
        for attr in concept.intent:
            attr_element = newdoc.createElement("attribute")
            attr_element.setAttribute("ref", attributes_ids[attr])
            i_element.appendChild(attr_element)
            
        c_element.appendChild(i_element)
            
        m_element = newdoc.createElement("meta")
        for key in concept.meta.keys():
            m_element.setAttribute(key.replace(" ", "_"), str(concept.meta[key]))
            
        c_element.appendChild(m_element)
        
        element.appendChild(c_element)
        
    top_element.appendChild(element)
    
    newdoc.writexml(out, indent="\n", addindent="\t", encoding="UTF-8")
    out.close()


def read_xml(path):
    """Read concept system from valid xml file.
    
    Examples
    ========
    
    >>> cs = read_xml('tests/concepts.xml')
    >>> print cs
    (['obj1', 'obj2', 'obj3'], ['attr1'])
    (['obj2', 'obj3'], ['attr1', 'attr2'])
    (['obj1'], ['attr1', 'attr3'])
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
    new_meta = {}
    
    def start_element(name, attrs):
        global new_obj, new_attr
        global new_extent, new_intent, new_meta
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
        elif name == "meta":
            for key in attrs.keys():
                new_meta[key.replace("_", " ")] = float(attrs[key])
        elif name == "concept":
            new_intent = []
            new_extent = []
            new_meta = {}
        
    def end_element(name):
        global cs, new_intent, new_extent, new_meta
        if name == "concept":
            new_concept = fca.Concept(new_extent, new_intent)
            new_concept.meta = new_meta
            cs.append(new_concept)
            
            new_extent = []
            new_intent = []
            new_meta = {}
    
    def char_data(data):
        if data[0] == "\n":
            return
        data = data.strip()
        global new_obj, new_attr
        if new_obj:
            d_objects[new_obj] = str(data)
            objects.append(str(data))
            new_obj = None
        elif new_attr:
            d_attributes[new_attr] = str(data)
            attributes.append(str(data))
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
