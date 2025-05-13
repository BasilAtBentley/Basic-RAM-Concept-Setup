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
from .add_property import _line_segment_location_property
from .force_load import ForceLoad
from .line_segment_2D import LineSegment2D

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class LineLoad(ForceLoad):
    """`LineLoad` is an line segment load that is applied to slabs.
    
    `LineLoads` are always located on a `ForceLoadingLayer`.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    Fx0 = _float_property("LLFx0", "Force value in the x-axis direction at start of segment")
    Fx1 = _float_property("LLFx1", "Force value in the x-axis direction at end of segment")

    Fy0 = _float_property("LLFy0", "Force value in the y-axis direction at start of segment")
    Fy1 = _float_property("LLFy1", "Force value in the y-axis direction at end of segment")

    Fz0 = _float_property("LLFz0", "Force value in the z-axis direction at start of segment")
    Fz1 = _float_property("LLFz1", "Force value in the z-axis direction at end of segment")

    Mx0 = _float_property("LLMx0", "Moment value about the x-axis at start of segment")
    Mx1 = _float_property("LLMx1", "Moment value about the x-axis at end of segment")

    My0 = _float_property("LLMy0", "Moment value about the y-axis at start of segment")
    My1 = _float_property("LLMy1", "Moment value about the y-axis at end of segment")

    location : LineSegment2D = _line_segment_location_property("Read-only :any:`LineSegment2D` location of this `LineLoad`.")

    # CONVENIENCE PROPERTY SETTING OPERATIONS

    def set_load_values(self, Fx: float, Fy: float, Fz: float, Mx: float, My: float) -> None:
        """Sets the given (uniform) load values"""
        self.Fx0 = Fx
        self.Fx1 = Fx

        self.Fy0 = Fy
        self.Fy1 = Fy

        self.Fz0 = Fz
        self.Fz1 = Fz

        self.Mx0 = Mx
        self.Mx1 = Mx

        self.My0 = My
        self.My1 = My

    def zero_load_values(self) -> None:
        """Sets all load values to zero"""
        self.set_load_values(0,0,0,0,0)

# -------------------------------------------------------------------------------------------------

class DefaultLineLoad(LineLoad):
    """`DefaultLineLoad` represents a `LineLoad` that stores the default values for future `LineLoads` that are created.

    An `Exception` will be raised if the `location` property of `DefaultLineLoad` is accessed.
    
    There is only 1 and always 1 `DefaultLineLoad` in the `Model`. It is accessed through :any:`CadManager.default_line_load`
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



