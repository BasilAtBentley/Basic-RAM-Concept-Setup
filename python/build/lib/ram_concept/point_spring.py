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
from .cad_entity import CadEntity
from .point_2D import Point2D
from .spring import Spring

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class PointSpring(Spring):
    """`PointSpring` is a spring at a point that provides support to slabs.
    
    `PointSprings` are always located on the :any:`StructureLayer` ("Mesh Input" layer).
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PROPERTY PROPERTIES

    kFr = _float_property("PSKFr", "Lateral spring stiffness in r-axis direction.")

    kFs = _float_property("PSKFs", "Lateral spring stiffness in s-axis direction.")

    kFz = _float_property("PSKFz", "Lateral spring stiffness in z-axis direction.")

    kMr = _float_property("PSKMr", "Rotational spring stiffness about r-axis.")

    kMs = _float_property("PSKMs", "Rotational spring stiffness about s-axis.")

    location : Point2D = _point_location_property("Read-only :any:`Point2D` location of this `PointSpring`.")

    # CONVENIENCE PROPERTY SETTING OPERATIONS

    # doesn't seem beneficial to expose this
    def _set_spring_stiffnesses(self, kFr: float, kFs: float, kFz: float, kMr: float, kMs: float) -> None:
        """Sets the given (uniform) spring stiffness"""
        self.kFr = kFr
        self.kFs = kFs
        self.kFz = kFz
        self.kMr = kMr
        self.kMs = kMs

    def zero_spring_stiffnesses(self) -> None:
        """Sets all spring stiffnesses to zero"""
        self._set_spring_stiffnesses(0,0,0,0,0)

# -------------------------------------------------------------------------------------------------

class DefaultPointSpring(PointSpring):
    """`DefaultPointSpring` represents a `PointSpring` that stores the default values for future `PointSpring` that are created.

    An `Exception` will be raised if the `location` property of `DefaultPointSpring` is accessed.
    
    There is only 1 and always 1 `DefaultPointSpring` in the `Model`. It is accessed through :any:`CadManager.default_point_spring`
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
