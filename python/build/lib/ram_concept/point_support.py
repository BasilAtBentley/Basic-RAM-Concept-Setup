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
from .cad_entity import CadEntity
from .point_2D import Point2D
from .rigid_support import RigidSupport

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class PointSupport(RigidSupport):
    """`PointSupport` is a logical (on/off) support at a point that provides support to slabs.
    
    `PointSupport` are always located on the :any:`StructureLayer` ("Mesh Input" layer).
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PROPERTY PROPERTIES

    Fr = _bool_property("RPSFr", "Lateral fixity in r-axis direction")

    Fs = _bool_property("RPSFs", "Lateral fixity in s-axis direction")

    Fz = _bool_property("RPSFz", "Lateral fixity in z-axis direction")

    Mr = _bool_property("RPSMr", "Rotational fixity about r-axis")

    Ms = _bool_property("RPSMs", "Rotational fixity about s-axis")

    location : Point2D = _point_location_property("Read-only :any:`Point2D` location of this `PointSupport`.")

    angle = _float_property("RPSAngle", "The counter-clockwise angle of the support r-axis (about the z-axis), with angle 0 being parallel to the x-axis.") 

    # CONVENIENCE PROPERTY SETTING OPERATIONS

    def set_all_fixities(self, fixity: bool) -> None:
        """Sets all the fixity properties to the given value"""
        self.Fr = fixity
        self.Fs = fixity
        self.Fz = fixity
        self.Mr = fixity
        self.Ms = fixity

# -------------------------------------------------------------------------------------------------

class DefaultPointSupport(PointSupport):
    """`DefaultPointSupport` represents a `PointSupport` that stores the default values for future `PointSupport` that are created.

    An `Exception` will be raised if the `location` property of `DefaultPointSupport` is accessed.
    
    There is only 1 and always 1 `DefaultPointSupport` in the `Model`. It is accessed through :any:`CadManager.default_point_support`
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
