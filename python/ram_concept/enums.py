#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# to avoid circular module dependencies, when references only used for type hints
# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    pass

# -------------------------------------------------------------------------------------------------

class ElevationReference(Enum):
    """For specifying where elevations are measured from.

    The available values are:

    * ABSOLUTE: elevation values are absolute (no adjustment needed)
    * ABOVE_SOFFIT: elevation values are relative to slab soffit (add to soffit elevation)
    * ABOVE_SURFACE: elevation values are relative to slab surface (add to surface elevation)
    * ABOVE_TOP_COVER: elevation values are relative to top cover elevation (add to top cover elevation)
    * ABOVE_BOTTOM_COVER: elevation values are relative to bottom cover elevation (add to bottom cover elevation)
    * ABOVE_MID_DEPTH: elevation values are relative to mid-depth elevation (add to (surface + soffit)/2)
    """
    ABSOLUTE           = 1
    ABOVE_SOFFIT       = 2
    ABOVE_SURFACE      = 3
    ABOVE_TOP_COVER    = 4
    ABOVE_BOTTOM_COVER = 5
    ABOVE_MID_DEPTH    = 6

    # INTERNAL OPERATIONS

    @classmethod
    def _to_API(cls, internal_value: int) -> ElevationReference:
        """Convert the internal value to the ElevationReference value (raises exception if invalid)."""
        return ElevationReference(internal_value) # will raise exception if invalid

    def _to_internal(self) -> int:
        """Convert the enum value into an internal integer."""
        return self.value

# -------------------------------------------------------------------------------------------------

class SpanSet(Enum):
    """For specifying the latitude-vs-longitude direction of a span (or span-related items).

    The available values are:

    * LATITUDE: the "latitude" direction
    * LONGITUDE: the "longitude" direction
    """
    LATITUDE    = "latitude"
    LONGITUDE   = "longitude"

    # INTERNAL OPERATIONS

    @classmethod
    def _to_API(cls, internal_value: str) -> SpanSet:
        """Convert the internal value to the SpanSet value (raise exception if invalid)."""
        return SpanSet(internal_value) # will raise exception if invalid

    def _to_internal(self) -> str:
        """Convert the enum value into an internal integer."""
        return self.value

# -------------------------------------------------------------------------------------------------

class GeneratedBy(Enum):
    """For specifying the whether the user or program generated information.

    The available values are:

    * PROGRAM: for the generated tendon layer
    * USER:    for the manual tendon layer
    """
    PROGRAM    = "program"
    USER       = "user"

    # INTERNAL OPERATIONS

    @classmethod
    def _to_API(cls, internal_value: str) -> GeneratedBy:
        """Convert the internal value to the GeneratedBy value (raise exception if invalid)."""
        return GeneratedBy(internal_value) # will raise exception if invalid

    def _to_internal(self) -> str:
        """Convert the enum value into an internal integer."""
        return self.value
