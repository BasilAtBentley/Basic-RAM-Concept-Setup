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

class ForceLoad(CadEntity):
    """`ForceLoad` is an abstract superclass for :any:`PointLoad`, :any:`LineLoad` and :any:`AreaLoad`.
    
    `ForceLoads` are always located on a :any:`ForceLoadingLayer`.
    """
    # internally this maps to the Load class
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    elevation = _float_property("LoadElevation", "The elevation of the load relative to the surface of the slab or beam it is applied to.")

    # skip IsmId