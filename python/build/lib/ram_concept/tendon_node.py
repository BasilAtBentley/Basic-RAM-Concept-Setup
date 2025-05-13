#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from typing import TYPE_CHECKING
from typing import List

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .add_property import _float_property
from .add_property import _point_location_property
from .add_property import _readonly_enum_int_property
from .add_property import _readonly_float_property
from .cad_entity import CadEntity
from .point_2D import Point2D
from .cad_entity import CadEntity
from .enums import ElevationReference

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model
    from .tendon_segment import TendonSegment

# -------------------------------------------------------------------------------------------------

class TendonNode(CadEntity):
    """`TendonNode` is a node (profile point) that defines locations and elevations for :any:`TendonSegment` and :any:`Jack`.

    The properties elevation, soffit and surface may become out of date when the structure changes.
    They are always valid after a successfull calc-all.
    
    `TendonNode` are always located on a :any:`TendonLayer`.
    """

    # may want to revisit and add a Node class between this an CadEntity

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PROPERTY PROPERTIES

    elevation_reference: ElevationReference = _readonly_enum_int_property("ElevationReference", ElevationReference, ":any:`ElevationReference`: The reference for calculation elevations.")

    elevation_value = _readonly_float_property("ElevationValue", "The vertical distance from the `elevation_reference` to the elevation.")

    elevation = _readonly_float_property("Elevation", "Readonly: The absolute elevation of this `TendonNode`.")

    soffit = _readonly_float_property("Soffit", "Readonly: slab soffit elevation at this `TendonNode`.")

    surface = _readonly_float_property("Surface", "Readonly: slab surface elevation at this `TendonNode`.")

    location : Point2D = _point_location_property("Read-only :any:`Point2D` location of this `TendonNode`.")

    # OPERATIONS

    def connected_tendon_segments(self)->List[TendonSegment]:
        """Return list of all :any:`TendonSegment` connected to this `TendonNode`."""
        result = self._command("[GET_CONNECTED_TENDONS]")
        return self._model._get_datas_from_bracket_string(result)
        
    def connected_tendon_segments_except(self, excluded_segment: TendonSegment)->List[TendonSegment]:
        """Return list of all :any:`TendonSegment` connected to this `TendonNode`, except the given one.
        This method can be useful for following a chain of :any:`TendonSegment`. An exception is raised
        if the given `excluded_segment` is not connected to this `TendonNode`."""
        tendon_segments = self.connected_tendon_segments()
        tendon_segments.remove(excluded_segment)
        return tendon_segments

    # CadEntity OVERRIDES

    def delete(self) -> None:
        """This method will raise an exception, as `delete` is not available for `TendonNode`."""
        raise Exception("delete() is not supported for TendonNode")



# -------------------------------------------------------------------------------------------------
# note - there is no DefaultTendonNode
