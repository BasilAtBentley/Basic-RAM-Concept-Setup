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
from .add_property import _enum_string_property
from .add_property import _float_property
from .add_property import _polygon_location_property
from .concrete_spanning_member import ConcreteSpanningMember
from .polygon_2D import Polygon2D

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class SlabAreaBehavior(Enum):
    """For specifying stiffness behaviors for `SlabArea`.
    
    Note that the CUSTOM behavior must be set before setting individual stiffness factors."""
    TWO_WAY_SLAB = "two-way slab"
    ONE_WAY_SLAB = "one-way slab"
    NO_TORION_SLAB = "no-torsion two-way slab"
    CUSTOM = "custom"

    @classmethod
    def _to_API(cls, internal_value: str) -> SlabAreaBehavior:
        """Convert the internal value to the SlabAreaBehavior value (raise exception if invalid)."""
        return SlabAreaBehavior(internal_value) # will raise exception if invalid

    def _to_internal(self) -> str:
        """Convert the enum value into an internal string."""
        return self.value

# -------------------------------------------------------------------------------------------------

class SlabArea(ConcreteSpanningMember):
    """SlabArea represents a polygon-shaped slab in the CAD system.
    
    SlabAreas are always located on the :any:`StructureLayer` ("Mesh Input" layer).
    """
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []

    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    r_axis : float = _float_property("SlabRAxis", "CCW/ACW angle from 3 o'clock to the r-axis (for value of zero, the r-axis is parallel to the global x-axis).")

    behavior : SlabAreaBehavior = _enum_string_property("SlabBehavior", SlabAreaBehavior, "SlabAreaBehavior: The stiffness behavior for the `SlabArea`. CUSTOM is required to directly set stiffness factors.")

    location: Polygon2D = _polygon_location_property("Read-only :any:`Polygon2D` location of the `SlabArea`")    

    # ConcreteSpanningMember OVERRIDES

    def _has_custom_stiffness_behavior(self):
        """This ConcreteSpanningMember has been set to use custom stiffness values.
        (this method must be overridden)"""
        return self.behavior == SlabAreaBehavior.CUSTOM

# -------------------------------------------------------------------------------------------------

class DefaultSlabArea(SlabArea):
    """`DefaultSlabArea` represents a `SlabArea` that stores the default values for future `SlabAreas` that are created.

    An `Exception` will be raised if the `location` property of `DefaultSlabArea` is accessed.
    
    There is only 1 and always 1 `DefaultSlabArea` in the `Model`. It is accessed through :any:`CadManager.default_slab_area`
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