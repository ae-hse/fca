#!/usr/bin/env python
# encoding: utf-8
"""
stabilitytest.py

Created by Nikita Romashkin on 2010-01-21.
"""

import sys
import os

import fca


def main():
    print "****************************"
    print "* stabilitytest 2010-01-21 *"
    print "****************************"
    if len(sys.argv) == 1:
        return
    path = sys.argv[1]
    if not os.path.exists(path):
        print "File does not exist: \"%s\"" % path
    else:
        print "Processing context: \"%s\"" % path
        root, ext = os.path.splitext(path)
        print "File extension = \"%s\"" % ext
        if ext == ".cxt":
            readfunction = fca.read_cxt
        elif ext == ".txt":
            readfunction = fca.read_txt
        else:
            print "Unknown file extension"
            return

        try:
            context = readfunction(path)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        print "Context loaded. Objects: {0}. Attributes: {1}".format(len(context.objects),
                                                                     len(context.attributes))
        cs = fca.norris(context)[0]
        print "{0} concepts".format(len(cs))
        print "Compute extensional stability"
        es = fca.compute_estability(cs)
        out = file(".".join([path, "e-s.txt"]), "w")

        l = es.items()
        l.sort(cmp=lambda x,y: cmp(x[1], y[1]), reverse=True)

        for concept in [c[0] for c in l]:
            s ="({0} , {1}) {2}\n".format(" ".join(concept.extent), " ".join(concept.intent),
                                        es[concept])
            out.write(s)
        out.close()

        print "Compute intensional stability"
        is_ = fca.compute_istability(cs)
        out = file(".".join([path, "i-s.txt"]), "w")

        l = is_.items()
        l.sort(cmp=lambda x,y: cmp(x[1], y[1]), reverse=True)

        for concept in [c[0] for c in l]:
            s ="({0} , {1}) {2}\n".format(" ".join(concept.extent), " ".join(concept.intent),
                                        is_[concept])
            out.write(s)
        out.close()
        print "End"


if __name__ == '__main__':
    main()