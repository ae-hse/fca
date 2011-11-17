# -*- coding: utf-8 -*-
"""Holds function that write lattice diagram to .dot file""" 

import fca

def write_dot(cs, path):
    """For given concept_system writes a .dot file, which contains graph
    representation of lattice diagram in format understandable 
    by graphviz' dot. "path" contains name of the output file.  
 
    Examples
    ========

    Load example file from tests directory

    >>> c = fca.read_cxt('tests/context.cxt')
    >>> cs = fca.norris(c)
    >>> write_dot(cs, "")
    Traceback (most recent call last):
        ...
    AssertionError: Filename can't be empty

    """
    assert len(path)!=0, "Filename can't be empty"
    output_file = open(path, "w")
    output_file.write("digraph L{")
    output_file.write("\n")
    output_file.write("nodesep=.25;\n")
    output_file.write("node[shape=circle,label=\"\"];")
    output_file.write("\n")
    output_file.write("edge[dir=\"none\",minlen=2,fontsize=11,labelfloat=true,fontname=Arial];")
    output_file.write("\n")

    own_objects = find_own_objects(cs)
    own_attributes = find_own_attributes(cs)
    for i in xrange(len(cs)):
        output_file.write("c%i [width=0.25]\n" % i)
        if len(own_objects[cs[i]])!=0:
            output_file.write("c%i -> c%i" % (i, i))
            # TODO:
            if len(own_objects[cs[i]]) >= 5:
                own_objects[cs[i]] = [str(len(own_objects[cs[i]]))]
            output_file.write("[headlabel=\"%s\", " %\
                     "\\n ".join(own_objects[cs[i]]))
            output_file.write(
                "labeldistance=1,labelangle=270,color=transparent]\n")
        if len(own_attributes[cs[i]])!=0:
            output_file.write("c%i -> c%i" % (i, i))
            # TODO:
            if len(own_attributes[cs[i]]) >= 5:
                own_attributes[cs[i]] = [str(len(own_attributes[cs[i]]))]
            output_file.write("[taillabel=\"%s\", " %\
                     "\\n ".join(own_attributes[cs[i]]))
            output_file.write(
                "labeldistance=2,labelangle=90,color=transparent]\n")

    parents = fca.compute_covering_relation(cs)
    for i in xrange(len(cs)):
        for p in parents[cs[i]]:
            output_file.write("c%i -> c%i\n" % (cs.index(p), i))
    output_file.write("}")

    output_file.close()

def uwrite_dot(cs, path, full=False):
    assert len(path)!=0, "Filename can't be empty"
    
    import codecs
    
    output_file = codecs.open(path, "w", "utf-8")
    output_file.write("digraph L{")
    output_file.write("\n")
    output_file.write("nodesep=.25;\n")
    output_file.write("node[shape=circle,label=\"\"];")
    output_file.write("\n")
    output_file.write("edge[dir=\"none\",minlen=2,fontsize=9,labelfloat=true,fontname=Arial,color=grey,style=\"setlinewidth(.7)\"];")
    output_file.write("\n")

    own_objects = find_own_objects(cs)
    own_attributes = find_own_attributes(cs)

    for i in xrange(len(cs)):
        output_file.write("c%i [width=0.25]\n" % i)

    parents = fca.compute_covering_relation(cs)
    for i in xrange(len(cs)):
        for p in parents[cs[i]]:
            output_file.write("c%i -> c%i\n" % (cs.index(p), i))

    for i in xrange(len(cs)):
        if len(own_objects[cs[i]])!=0:
            output_file.write("c%i -> c%i" % (i, i))
            # TODO:
            if not full:
                if len(own_objects[cs[i]]) >= 1:
                    own_objects[cs[i]] = [str(len(own_objects[cs[i]]))]
            if len(own_objects[cs[i]]) > 6:
                own_objects[cs[i]] = own_objects[cs[i]][:6] + ["..."]
            n = len(own_objects[cs[i]])
            output_file.write("[headlabel=\"%s\", " %\
                     "\\n ".join(own_objects[cs[i]]))
            output_file.write(
                "labeldistance={0},labelangle=270,color=transparent]\n".format(n/1.8 + 0.5))
        if len(own_attributes[cs[i]])!=0:
            output_file.write("c%i -> c%i" % (i, i))
            # TODO:
            if not full:
                if len(own_attributes[cs[i]]) >= 1:
                    own_attributes[cs[i]] = [str(len(own_attributes[cs[i]]))]
            if len(own_attributes[cs[i]]) > 6:
                own_attributes[cs[i]] = own_attributes[cs[i]][:6] + ["..."]
            n = len(own_attributes[cs[i]])
            output_file.write("[taillabel=\"%s\", " %\
                     "\\n ".join(own_attributes[cs[i]]))
            output_file.write(
                "labeldistance={0},labelangle=90,color=transparent]\n".format(n/1.8 + 0.5))

    output_file.write("}")

    output_file.close()

def find_own_objects(cs):
    """Return set of own objects for current concept"""
    own_objects = {}
    for con in cs:
        own_objects[con] = []
        for obj in con.extent:
            own_objects[con].append(obj)
            for sub_con in cs:
                if sub_con.extent < con.extent and\
                        obj in sub_con.extent:
                    own_objects[con].pop()
                    break
    return own_objects

def find_own_attributes(cs):
    """Return set of own attributes for current concept"""
    own_attributes = {}
    for con in cs:
        own_attributes[con] = []
        for attr in con.intent:
            own_attributes[con].append(attr)
            for sub_con in cs:
                if sub_con.intent < con.intent and\
                        attr in sub_con.intent:
                    own_attributes[con].pop()
                    break
    return own_attributes


if __name__ == "__main__":
    import doctest
    doctest.testmod()
