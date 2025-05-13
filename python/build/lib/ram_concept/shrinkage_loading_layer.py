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
from .add_property import _cad_entity_list_copy_read_only_property
from .loading_layer import LoadingLayer
from .shrinkage_area_load import ShrinkageAreaLoad

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    #from .area_load import AreaLoad
    #from .line_load import LineLoad
    from .line_segment_2D import LineSegment2D
    from .model import Model
    from .point_2D import Point2D
    from .polygon_2D import Polygon2D

# -------------------------------------------------------------------------------------------------

class ShrinkageLoadingLayer(LoadingLayer):
    """`ShrinkageLoadingLayer` represents a named layer that contains :any:`ShrinkageAreaLoad`, and their results.
    
    The :any:`LoadingType` and :any:`LoadingAnalysisType` of `ShrinkageLoadingLayers` cannot be changed.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    #  PUBLIC PROPERTIES


    shrinkage_area_loads  : List[ShrinkageAreaLoad]  = _cad_entity_list_copy_read_only_property("AreaLoadForShrinkage",  "All the :any:`ShrinkageAreaLoad` on this layer.")

    # CAD ENTITY ADDITION METHODS


    def add_shrinkage_area_load(self, location: Polygon2D) -> ShrinkageAreaLoad:
         """Add a :any:`ShrinkageAreaLoad` at the given location, copying properties from :any:`CadManager.default_shrinkage_area_load`.
                         
        Note that the location will be snapped to the nearest 0.1mm"""
         return self._add_cad_entity_with_polygon("AreaLoadForShrinkage", location)
    
