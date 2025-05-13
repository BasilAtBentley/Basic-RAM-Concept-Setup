#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .add_property import _bool_property
from .add_property import _enum_string_property
from .add_property import _float_property
from .add_property import _line_segment_location_property
from .add_property import _point_property
from .concrete_spanning_member import ConcreteSpanningMember
from .line_segment_2D import LineSegment2D
from .point_2D import Point2D

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------

class BeamBehavior(Enum):
    """For specifying stiffness behaviors for `Beam`.
    
    Note that the CUSTOM behavior must be set before setting individual stiffness factors."""
    STANDARD_BEAM = "two-way slab"
    NO_TORSION_BEAM = "no-torsion two-way slab"
    CUSTOM = "custom"

    @classmethod
    def _to_API(cls, internal_value: str) -> BeamBehavior:
        """Convert the internal value to the BeamBehavior value (raises exception if invalid)."""
        return BeamBehavior(internal_value) # will raise exception if invalid

    def _to_internal(self) -> str:
        """Convert the enum value into an internal string."""
        return self.value


# -------------------------------------------------------------------------------------------------

class Beam(ConcreteSpanningMember):
    """`Beam` represents a beam along a line segment in the CAD system.
    
    `Beams` are always located on the :any:`StructureLayer` ("Mesh Input" layer).
    """
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []

   
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    width: float = _float_property("Width","Width of the `Beam`.")

    behavior : BeamBehavior = _enum_string_property("BeamBehavior", BeamBehavior, "BeamBehavior: The stiffness behavior for the `Beam`. CUSTOM is required to directly set stiffness factors.""")

    location: LineSegment2D = _line_segment_location_property("Read-only :any:`LineSegment2D` location of the `Beam` spine")

    mesh_as_slab: bool = _bool_property("BeamIsMeshedAsSlab","Meshing algorithms consider the beam exactly the same as a `SlabArea`.")

    # leave these out for now
    # determine a strategy for beam offsets
    # left_point_0  = _point_property("LeftPt0",  "Left miter point at end 0")
    # left_point_1  = _point_property("LeftPt1",  "Left miter point at end 1")
    # right_point_0 = _point_property("RightPt0", "Right miter point at end 0")
    # right_point_1 = _point_property("RightPt1", "Right miter point at end 1")

    # ConcreteSpanningMember OVERRIDES

    def _has_custom_stiffness_behavior(self):
        """This ConcreteSpanningMember has been set to use custom stiffness values.
        (this method must be overridden)"""
        return self.behavior == BeamBehavior.CUSTOM

# -------------------------------------------------------------------------------------------------

class DefaultBeam(Beam):
    """`DefaultBeam` represents a `Beam` that stores the default values for future `Beams` that are created.

    An `Exception` will be raised if the `location` property of `DefaultBeam` is accessed.
    
    There is only 1 and always 1 `DefaultBeam` in the `Model`. It is accessed through :any:`CadManager.default_beam`
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