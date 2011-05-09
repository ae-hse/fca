# -*- coding: utf-8 -*-
"""FCA library"""

from fca.concept import Concept
from fca.concept_system import ConceptSystem
from fca.concept_lattice import ConceptLattice
from fca.context import Context
from fca.mvcontext import ManyValuedContext
from fca.scale import Scale
from fca.implication import Implication

from fca.algorithms import (norris, compute_covering_relation,
                            scale_mvcontext, compute_dg_basis)
from fca.readwrite import (read_txt, read_cxt, write_cxt, write_dot,
                           read_mv_txt, read_xml, write_xml, write_mv_txt,
                           uread_cxt, uwrite_cxt)
from fca.algorithms.filtering import (filter_concepts, compute_estability,
compute_istability, compute_separation_index, 
compute_probability, compute_index)
