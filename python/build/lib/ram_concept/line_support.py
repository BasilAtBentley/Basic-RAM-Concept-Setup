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
from .add_property import _line_segment_location_property
from .cad_entity import CadEntity
from .line_segment_2D import LineSegment2D
from .rigid_support import RigidSupport

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class LineSupport(RigidSupport):
    """`LineSupport` is a logical (on/off) support at a line segment that provides support to slabs.

    The r-axis for the support is defined as along the location segment from start to end. The s-axis is
    horizontal and perpendicular to the location segment.
    
    `LineSupports` are always located on the :any:`StructureLayer` ("Mesh Input" layer).
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PROPERTY PROPERTIES

    Fr = _bool_property("RLSFr", "Lateral fixity in r-axis direction (parallel to line)")

    Fs = _bool_property("RLSFs", "Lateral spring stiffness in s-axis direction (perpendicular to line)")

    Fz = _bool_property("RLSFz", "Lateral spring stiffness in z-axis direction")

    Mr = _bool_property("RLSMr", "Rotational spring stiffness about r-axis (parallel to line)")

    Ms = _bool_property("RLSMs", "Rotational spring stiffness about s-axis (perpendicular to line)")

    location : LineSegment2D = _line_segment_location_property("Read-only :any:`LineSegment2D` location of this `LineSupport`.")

    # CONVENIENCE PROPERTY SETTING OPERATIONS

    def set_all_fixities(self, fixity: bool) -> None:
        """Sets the given (uniform) spring stiffness"""
        self.Fr = fixity
        self.Fs = fixity
        self.Fz = fixity
        self.Mr = fixity
        self.Ms = fixity

# -------------------------------------------------------------------------------------------------

class DefaultLineSupport(LineSupport):
    """`DefaultLineSupport` represents a `LineSupport` that stores the default values for future `LineSupport` that are created.

    An `Exception` will be raised if the `location` property of `DefaultLineSupport` is accessed.
    
    There is only 1 and always 1 `DefaultLineSupport` in the `Model`. It is accessed through :any:`CadManager.default_line_support`
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
