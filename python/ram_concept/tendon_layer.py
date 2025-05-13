#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# to avoid circular module dependencies, when references only used for type hints
# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from typing import List
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .add_property import _cad_entity_list_property
from .add_property import _readonly_enum_string_property
from .cad_layer import CadLayer
from .data import Data
from .enums import GeneratedBy
from .enums import SpanSet

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model
    from .tendon_segment import TendonSegment
    from .tendon_node import TendonNode
    from .jack import Jack
    from .line_segment_2D import LineSegment2D
    from .point_2D import Point2D

# -------------------------------------------------------------------------------------------------

class TendonLayer(CadLayer):
    """TendonLayer represents a manual or generated tendon layer in the CAD system.
    
    The TendonLayer is accessible through :any:`CadManager.tendon_layer` and :any:`CadManager.tendon_layers`.
    """
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    generated_by: GeneratedBy = _readonly_enum_string_property("GeneratedBy", GeneratedBy, "The creator (user vs program) of the `Tendons` and `Jacks` on this layer.")
    span_set:     SpanSet     = _readonly_enum_string_property("SpanSet",     SpanSet,     "The span direction set this TendonLayer is associated with.")

    tendon_segments: List[TendonSegment]     = _cad_entity_list_property("Tendons",     "All the :any:`TendonSegment` on this layer.")
    jacks:           List[Jack]              = _cad_entity_list_property("Jacks",       "All the :any:`Jack` on this layer.")
    tendon_nodes:    List[TendonNode]        = _cad_entity_list_property("TendonNodes", "All the :any:`TendonNode` on this layer.")

    # PUBLIC CAD ENTITY ADDITION METHODS

    def add_jack(self, location: Point2D) -> Jack:
        """Add a :any:`Jack` at the given location, copying properties from :any:`CadManager.default_jack`.
                
        Note that the location will be snapped to the nearest 0.1mm and
        a :any:`TendonNode` may be created if none exist at that location."""
        return self._add_cad_entity_with_point("Jack", location)

    def add_tendon_segment(self, location: LineSegment2D) -> TendonSegment:
        """Add a :any:`TendonSegment` at the given location, copying properties from :any:`CadManager.default_tendon_segment`.
                
        Note that the location will be snapped to the nearest 0.1mm and 1 or 2
        :any:`TendonNode` may be created if none exist at that the end points."""
        return self._add_cad_entity_with_line_segment("Tendon", location)