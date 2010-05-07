# -*- coding: utf-8 -*-
"""FCA library"""

from fca.concept import Concept
from fca.concept_system import (ConceptSystem, ConceptLattice)
from fca.context import Context
from fca.mvcontext import ManyValuedContext
from fca.scale import Scale

from fca.algorithms import (norris, compute_covering_relation, scale_mvcontext)
from fca.readwrite import (read_txt, read_cxt, write_cxt, write_dot,
                           read_mv_txt, read_xml, write_xml)
from fca.algorithms.filtering import filter_concepts
