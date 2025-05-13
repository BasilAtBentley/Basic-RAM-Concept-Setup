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
from .add_property import _point_location_property
from .concrete_support import ConcreteSupport
from .point_2D import Point2D

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class Column(ConcreteSupport):
    """`Column` represents an column at a point in the CAD system.
    
    `Columns` are always located on the :any:`StructureLayer` ("Mesh Input" layer).
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    b = _float_property("B", "The width of the column (if zero, column is round)")

    d = _float_property("D", "The depth of the column (diameter if b=0)")

    i_factor = _float_property("IFactor", "The bending stiffness multiplier (or 'crack factor')")

    angle = _float_property("Angle", "The plan view angle of the column (at 0, the 'b' dimension is along x-axis)")

    roller = _bool_property("Roller", "Is the far end of the column free to move laterally?")

    location: Point2D = _point_location_property("Read-only :any:`Point2D` location of the Column")
    
    # FUTURE: maybe add ISM property in future

# -------------------------------------------------------------------------------------------------

class DefaultColumn(Column):
    """`DefaultColumn` represents a `Column` that stores the default values for future `Columns` that are created.

    An `Exception` will be raised if the `location` property of `DefaultColumn` is accessed.
    
    There is only 1 and always 1 `DefaultColumn` in the `Model`. It is accessed through :any:`CadManager.default_column`
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
