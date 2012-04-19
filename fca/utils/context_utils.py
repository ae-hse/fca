#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy

def union_contexts(super_cxt, cxt_set):
    super_cxt = copy(super_cxt)
    for cxt in cxt_set:
        for obj in cxt:
            super_cxt.add(obj, cxt.get_intent(obj))

    return super_cxt