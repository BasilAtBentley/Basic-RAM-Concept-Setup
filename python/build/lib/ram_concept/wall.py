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
from .add_property import _bool_property
from .add_property import _float_property
from .add_property import _line_segment_location_property
from .concrete_support import ConcreteSupport
from .line_segment_2D import LineSegment2D

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class Wall(ConcreteSupport):
    """`Wall` represents a wall along a line segment in the CAD system.
    
    `Walls` are always located on the :any:`StructureLayer` ("Mesh Input" layer).
    """
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    shear_wall = _bool_property("ShearWall", "If True, the wall is fixed to the slab horizontally")

    thickness = _float_property("WallThickness", "The through-thickness of the Wall")

    location: LineSegment2D = _line_segment_location_property("Read-only :any:`LineSegment2D` location of the Wall")
    
    # FUTURE: perhaps add ISM property in future

# -------------------------------------------------------------------------------------------------

class DefaultWall(Wall):
    """`DefaultWall` represents a `Wall` that stores the default values for future `Walls` that are created.

    An `Exception` will be raised if the `location` property of `DefaultWall` is accessed.
    
    There is only 1 and always 1 `DefaultWall` in the `Model`. It is accessed through :any:`CadManager.default_wall`
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
