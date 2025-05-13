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
from .cad_entity import CadEntity

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class Spring(CadEntity):
    """Spring is an abstract superclass for :any:`PointSpring`, :any:`LineSpring` and :any:`AreaSpring`.
    
    Springs are always located on the :any:`StructureLayer` ("Mesh Input" layer).
    """
    # Spring maps to a merging of SpringOrSupport and Spring in the back end

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []

    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    elevation = _float_property("SpringElevation", "The elevation of the spring relative to the soffit of the slab or beam it is applied to.")

    angle = _float_property("SpringAngle", "The counter-clockwise angle of the spring r-axis (about the z-axis), with angle 0 being parallel to the x-axis.") 
