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
from .add_property import _polygon_location_property
from .force_load import ForceLoad
from .polygon_2D import Polygon2D

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class AreaLoad(ForceLoad):
    """`AreaLoad` is an polygon-shaped load that is applied to slabs.
    
    `AreaLoads` are always located on a `ForceLoadingLayer`.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    Fx0 = _float_property("ALFx0", "Force value in the x-axis direction at first point in shape")
    Fx1 = _float_property("ALFx1", "Force value in the x-axis direction at second point in shape")
    Fx2 = _float_property("ALFx2", "Force value in the x-axis direction at third point in shape")

    Fy0 = _float_property("ALFy0", "Force value in the y-axis direction at first point in shape")
    Fy1 = _float_property("ALFy1", "Force value in the y-axis direction at second point in shape")
    Fy2 = _float_property("ALFy2", "Force value in the y-axis direction at third point in shape")

    Fz0 = _float_property("ALFz0", "Force value in the z-axis direction at first point in shape")
    Fz1 = _float_property("ALFz1", "Force value in the z-axis direction at second point in shape")
    Fz2 = _float_property("ALFz2", "Force value in the z-axis direction at third point in shape")

    Mx0 = _float_property("ALMx0", "Moment value about the x-axis at first point in shape")
    Mx1 = _float_property("ALMx1", "Moment value about the x-axis at second point in shape")
    Mx2 = _float_property("ALMx2", "Moment value about the x-axis at third point in shape")

    My0 = _float_property("ALMy0", "Moment value about the y-axis at first point in shape")
    My1 = _float_property("ALMy1", "Moment value about the y-axis at second point in shape")
    My2 = _float_property("ALMy2", "Moment value about the y-axis at third point in shape")

    location : Polygon2D = _polygon_location_property("Read-only :any:`Polygon2D` location of this `AreaLoad`.")

    # CONVENIENCE PROPERTY SETTING OPERATIONS

    def set_load_values(self, Fx: float, Fy: float, Fz: float, Mx: float, My: float) -> None:
        """Sets the given (uniform) load values"""
        self.Fx0 = Fx
        self.Fx1 = Fx
        self.Fx2 = Fx

        self.Fy0 = Fy
        self.Fy1 = Fy
        self.Fy2 = Fy

        self.Fz0 = Fz
        self.Fz1 = Fz
        self.Fz2 = Fz

        self.Mx0 = Mx
        self.Mx1 = Mx
        self.Mx2 = Mx

        self.My0 = My
        self.My1 = My
        self.My2 = My

    def zero_load_values(self) -> None:
        """Sets all load values to zero"""
        self.set_load_values(0,0,0,0,0)

# -------------------------------------------------------------------------------------------------

class DefaultAreaLoad(AreaLoad):
    """`DefaultAreaLoad` represents a `AreaLoad` that stores the default values for future `AreaLoads` that are created.

    An `Exception` will be raised if the `location` property of `DefaultAreaLoad` is accessed.
    
    There is only 1 and always 1 `DefaultAreaLoad` in the `Model`. It is accessed through :any:`CadManager.default_area_load`
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


