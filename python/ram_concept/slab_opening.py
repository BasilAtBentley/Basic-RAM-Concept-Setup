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
from .add_property import _int_property
from .add_property import _polygon_location_property
from .cad_entity import CadEntity
from .polygon_2D import Polygon2D

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class SlabOpening(CadEntity):
    """SlabOpening represents a polygon-shaped opening in the slab in the CAD system.
    
    `SlabOpenings` are always located on the :any:`StructureLayer` ("Mesh Input" layer).
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []

    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    priority = _int_property("Priority", "Relative priority of this vs other items (`SlabAreas`, `Beams`, `SlabOpenings`) (used in meshing)")

    location: Polygon2D = _polygon_location_property("Read-only :any:`Polygon2D` location of the `SlabOpening`")    

    # FUTURE: maybe add IsmId property later
# -------------------------------------------------------------------------------------------------

class DefaultSlabOpening(SlabOpening):
    """`DefaultSlabOpening` represents a `SlabOpening` that stores the default values for future `SlabOpenings` that are created.

    An `Exception` will be raised if the `location` property of `DefaultSlabOpening` is accessed.
    
    There is only 1 and always 1 `DefaultSlabOpening` in the `Model`. It is accessed through :any:`CadManager.default_slab_opening`
    """
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # CadEntity OVERRIDES

    def delete(self) -> None:
        """This method will raise an exception, as `delete` is not available for default objects."""
        raise Exception("delete() is not supported for default CadEntities")