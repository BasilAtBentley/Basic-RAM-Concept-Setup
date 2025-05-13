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
from .add_property import _point_location_property
from .force_load import ForceLoad
from .point_2D import Point2D

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class PointLoad(ForceLoad):
    """`PointLoad` is a load at a point that is applied to slabs.
    
    `PointLoads` are always located on a `ForceLoadingLayer`.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    Fx = _float_property("PLFx", "Force value in the x-axis direction")

    Fy = _float_property("PLFy", "Force value in the y-axis direction")

    Fz = _float_property("PLFz", "Force value in the z-axis direction")

    Mx = _float_property("PLMx", "Moment value about the x-axis")

    My = _float_property("PLMy", "Moment value about the y-axis")

    location : Point2D = _point_location_property("Read-only :any:`Point2D` location of this `PointLoad`.")

    # CONVENIENCE PROPERTY SETTING OPERATIONS
    
    def zero_load_values(self) -> None:
        """Sets all load values to zero"""
        self.Fx = 0
        self.Fy = 0
        self.Fz = 0
        self.Mx = 0
        self.My = 0

# -------------------------------------------------------------------------------------------------

class DefaultPointLoad(PointLoad):
    """`DefaultPointLoad` represents a `PointLoad` that stores the default values for future `PointLoads` that are created.

    An `Exception` will be raised if the `location` property of `DefaultPointLoad` is accessed.
    
    There is only 1 and always 1 `DefaultPointLoad` in the `Model`. It is accessed through :any:`CadManager.default_point_load`
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




