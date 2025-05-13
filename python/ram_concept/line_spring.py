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
from .cad_entity import CadEntity
from .line_segment_2D import LineSegment2D
from .spring import Spring

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class LineSpring(Spring):
    """`LineSpring` is an line segment spring that provides support to slabs.
    
    `LineSprings` are always located on the :any:`StructureLayer` ("Mesh Input" layer).
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PROPERTY PROPERTIES

    kFr0 = _float_property("LSKFr0", "Lateral spring stiffness in r-axis direction at the start point")
    kFr1 = _float_property("LSKFr1", "Lateral spring stiffness in r-axis direction at the end point")

    kFs0 = _float_property("LSKFs0", "Lateral spring stiffness in s-axis direction at the start point")
    kFs1 = _float_property("LSKFs1", "Lateral spring stiffness in s-axis direction at the end point")

    kFz0 = _float_property("LSKFz0", "Lateral spring stiffness in z-axis direction at the start point")
    kFz1 = _float_property("LSKFz1", "Lateral spring stiffness in z-axis direction at the end point")

    kMr0 = _float_property("LSKMr0", "Rotational spring stiffness about r-axis at the start point")
    kMr1 = _float_property("LSKMr1", "Rotational spring stiffness about r-axis at the end point")

    kMs0 = _float_property("LSKMs0", "Rotational spring stiffness about s-axis at the start point")
    kMs1 = _float_property("LSKMs1", "Rotational spring stiffness about s-axis at the end point")

    location : LineSegment2D = _line_segment_location_property("Read-only :any:`LineSegment2D` location of this `LineSpring`.")

    # CONVENIENCE PROPERTY SETTING OPERATIONS

    def set_spring_stiffnesses(self, kFr: float, kFs: float, kFz: float, kMr: float, kMs: float) -> None:
        """Sets the given (uniform) spring stiffness"""
        self.kFr0 = kFr
        self.kFr1 = kFr

        self.kFs0 = kFs
        self.kFs1 = kFs

        self.kFz0 = kFz
        self.kFz1 = kFz

        self.kMr0 = kMr
        self.kMr1 = kMr

        self.kMs0 = kMs
        self.kMs1 = kMs

    def zero_spring_stiffnesses(self) -> None:
        """Sets all spring stiffnesses to zero"""
        self.set_spring_stiffnesses(0,0,0,0,0)

# -------------------------------------------------------------------------------------------------

class DefaultLineSpring(LineSpring):
    """`DefaultLineSpring` represents a `LineSpring` that stores the default values for future `LineSprings` that are created.

    An `Exception` will be raised if the `location` property of `DefaultLineSpring` is accessed.
    
    There is only 1 and always 1 `DefaultLineSpring` in the `Model`. It is accessed through :any:`CadManager.default_line_spring`
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

