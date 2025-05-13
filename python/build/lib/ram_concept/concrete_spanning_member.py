#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .add_property import _float_property
from .add_property import _int_property
from .add_property import _stiffness_property
from .concrete_member import ConcreteMember

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class ConcreteSpanningMember(ConcreteMember):
    """`ConcreteSpanningMember` is an abstract superclass for :any:`Beam` and :any:`SlabArea`.
    
    `ConcreteSpanningMembers` are always located on the `StructureLayer` ("Mesh Input" layer)
    """
     # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
   
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    thickness = _float_property("SlabThickness","Thickness of the slab or beam")

    # FUTURE: add slab thickness optimization properties?

    toc = _float_property("TOC", "Top of concrete elevation")

    priority = _int_property("Priority", "Relative priority of this vs other items (`SlabAreas`, `Beams`, `SlabOpenings`) (used in meshing)")

    kMr  = _stiffness_property("SlabKMr",  "Stiffness multiplier for bending moments about the r-axis")
    kMs  = _stiffness_property("SlabKMs",  "Stiffness multiplier for bending moments about the s-axis")
    kMrs = _stiffness_property("SlabKMrs", "Stiffness multiplier for twisting moments about the r-s axes")
    kFr  = _stiffness_property("SlabKFr",  "Stiffness multiplier for axial forces in the r-axis direction")
    kFs  = _stiffness_property("SlabKFs",  "Stiffness multiplier for axial forces in the s-axis direction")
    kVrs = _stiffness_property("SlabKVrs", "Stiffness multiplier for in-plane shear forces along the r-s axes")

    # INTERNAL OPERATIONS

    def _has_custom_stiffness_behavior(self):
        """This ConcreteSpanningMember has been set to use custom stiffness values.
        (this method must be overridden)"""
        raise Exception("Must override _has_custom_stiffness_behavior")