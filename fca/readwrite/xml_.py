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
    objects = set()
    attributes = set()
    for concept in cs:
        objects = objects.union(concept.extent)
        attributes = attributes.union(concept.intent)
    objects = list(objects)
    attributes = list(attributes)
    
    objects_ids = dict([(objects[i], u"o{0}".format(i+1))  for i in xrange(len(objects))])
    attributes_ids = dict([(attributes[i], u"a{0}".format(i+1))  for i in xrange(len(attributes))])
    
    out = file(path, "wb")

    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, u"conceptsystem", None)
    top_element = newdoc.documentElement
    
    element = newdoc.createElement(u"objects")
    for obj in objects:
        obj_element = newdoc.createElement(u"object")
        obj_element.setAttribute(u"id", objects_ids[obj])
        textnode = newdoc.createTextNode(obj.encode("utf-8"))
        obj_element.appendChild(textnode)
        element.appendChild(obj_element)
    top_element.appendChild(element)
    
    element = newdoc.createElement(u"attributes")
    for attr in attributes:
        attr_element = newdoc.createElement(u"attribute")
        attr_element.setAttribute(u"id", attributes_ids[attr])
        textnode = newdoc.createTextNode(attr.encode("utf-8"))
        attr_element.appendChild(textnode)
        element.appendChild(attr_element)
    top_element.appendChild(element)
    
    element = newdoc.createElement(u"concepts")
    for concept in cs:
        c_element = newdoc.createElement(u"concept")
        
        e_element = newdoc.createElement(u"extent")
        for obj in concept.extent:
            obj_element = newdoc.createElement(u"object")
            obj_element.setAttribute(u"ref", objects_ids[obj])
            e_element.appendChild(obj_element)
            
        c_element.appendChild(e_element)
        
        i_element = newdoc.createElement(u"intent")
        for attr in concept.intent:
            attr_element = newdoc.createElement(u"attribute")
            attr_element.setAttribute(u"ref", attributes_ids[attr])
            i_element.appendChild(attr_element)
            
        c_element.appendChild(i_element)
            
        m_element = newdoc.createElement(u"meta")
        for key in concept.meta.keys():
            m_element.setAttribute(unicode(key.replace(" ", "_")), unicode(concept.meta[key]))
            
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
    global new_obj, new_attr, cs, buffer
    
    buffer = ""
    
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
        global new_obj, new_attr, buffer
        global new_extent, new_intent, new_meta
        if name == "object":
            if "id" in attrs.keys():
                buffer = ""
                new_obj = attrs["id"]
            elif "ref" in attrs.keys():
                new_extent.append(d_objects[attrs["ref"]])
        elif name == "attribute":
            if "id" in attrs.keys():
                buffer = ""
                new_attr = attrs["id"]
            elif "ref" in attrs.keys():
                new_intent.append(d_attributes[attrs["ref"]])
        elif name == "meta":
            for key in attrs.keys():
                new_meta[str(key).replace("_", " ")] = float(attrs[key])
        elif name == "concept":
            new_intent = []
            new_extent = []
            new_meta = {}
        
    def end_element(name):
        global cs, new_intent, new_extent, new_meta
        global new_obj, new_attr, buffer
        if name == "object":
            if new_obj:
                d_objects[new_obj] = buffer
                objects.append(buffer)
                new_obj = None
                buffer = ""
        elif name == "attribute":
            if new_attr:
                d_attributes[new_attr] = buffer
                attributes.append(buffer)
                new_attr = None
                buffer = ""
        elif name == "concept":
            new_concept = fca.Concept(new_extent, new_intent)
            new_concept.meta = new_meta
            cs.append(new_concept)
            
            new_extent = []
            new_intent = []
            new_meta = {}
    
    def char_data(data):
        global buffer
        if data[0] == "\n":
            return
        data = data.strip()
        buffer += data
    
    p = xml.parsers.expat.ParserCreate()
    
    p.StartElementHandler = start_element
    p.EndElementHandler = end_element
    p.CharacterDataHandler = char_data
    
    f = open(path)
    p.ParseFile(f)
    
    return cs
    
def uread_xml(path):
    global new_obj, new_attr, cs, buffer

    buffer = ""

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
        global new_obj, new_attr, buffer
        global new_extent, new_intent, new_meta
        if name == "object":
            if "id" in attrs.keys():
                buffer = ""
                new_obj = attrs["id"]
            elif "ref" in attrs.keys():
                new_extent.append(d_objects[attrs["ref"]])
        elif name == "attribute":
            if "id" in attrs.keys():
                buffer = ""
                new_attr = attrs["id"]
            elif "ref" in attrs.keys():
                new_intent.append(d_attributes[attrs["ref"]])
        elif name == "meta":
            for key in attrs.keys():
                new_meta[str(key).replace("_", " ")] = float(attrs[key])
        elif name == "concept":
            new_intent = []
            new_extent = []
            new_meta = {}

    def end_element(name):
        global cs, new_intent, new_extent, new_meta
        global new_obj, new_attr, buffer
        if name == "object":
            if new_obj:
                d_objects[new_obj] = buffer
                objects.append(buffer)
                new_obj = None
                buffer = ""
        elif name == "attribute":
            if new_attr:
                d_attributes[new_attr] = buffer
                attributes.append(buffer)
                new_attr = None
                buffer = ""
        elif name == "concept":
            new_concept = fca.Concept(new_extent, new_intent)
            new_concept.meta = new_meta
            cs.append(new_concept)

            new_extent = []
            new_intent = []
            new_meta = {}

    def char_data(data):
        global buffer
        if data[0] == "\n":
            return
        data = data.strip()
        buffer += data

    p = xml.parsers.expat.ParserCreate(encoding="UTF-8")

    p.StartElementHandler = start_element
    p.EndElementHandler = end_element
    p.CharacterDataHandler = char_data
    
    f = open(path)
    p.ParseFile(f)

    return cs


if __name__ == "__main__":
    import doctest
    doctest.testmod()
