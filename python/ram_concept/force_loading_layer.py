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
from .point_2D import Point2D
from .utilities import _bulk_set

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .area_load import AreaLoad
    from .line_load import LineLoad
    from .line_segment_2D import LineSegment2D
    from .model import Model

    from .point_load import PointLoad
    from .polygon_2D import Polygon2D

# -------------------------------------------------------------------------------------------------

class ForceLoadingLayer(LoadingLayer):
    """`ForceLoadingLayer` represents a named layer that contains force-defining loads, and their results.
    
    Some `ForceLoadingLayers` (balance, self-dead and hyperstatic) are read-only. Modification operations
    attempted on those layers will result in exceptions.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    #  PUBLIC PROPERTIES

    point_loads : List[PointLoad] = _cad_entity_list_copy_read_only_property("PointLoads", "All the :any:`PointLoad` on this layer.")
    line_loads  : List[LineLoad]  = _cad_entity_list_copy_read_only_property("LineLoads",  "All the :any:`LineLoad` on this layer.")
    area_loads  : List[AreaLoad]  = _cad_entity_list_copy_read_only_property("AreaLoads",  "All the :any:`AreaLoad` on this layer.")

    # CAD ENTITY ADDITION METHODS

    def add_point_load(self, location: Point2D) -> PointLoad:
        """Add a :any:`PointLoad` at the given location, copying properties from :any:`CadManager.default_point_load`.       
                        
        Note that the location will be snapped to the nearest 0.1mm.
        An Exception will be raised if this `ForceLoadingLayer` is read-only.       
        """
        self._operation_raise_if_read_only("add_point_load()")
        return self._add_cad_entity_with_point("PointLoad", location)
  
    def add_line_load(self, location: LineSegment2D) -> LineLoad:
        """Add a :any:`LineLoad` at the given location, copying properties from :any:`CadManager.default_line_load`.       
                        
        Note that the location will be snapped to the nearest 0.1mm.
        An Exception will be raised if this `ForceLoadingLayer` is read-only.       
        """
        self._operation_raise_if_read_only("add_line_load()")
        return self._add_cad_entity_with_line_segment("LineLoad", location)
    
    def add_area_load(self, location: Polygon2D) -> AreaLoad:
        """Add a :any:`AreaLoad` at the given location, copying properties from :any:`CadManager.default_area_load`.       
                        
        Note that the location will be snapped to the nearest 0.1mm.        
        An Exception will be raised if this `ForceLoadingLayer` is read-only.       
        """
        self._operation_raise_if_read_only("add_area_load()")
        return self._add_cad_entity_with_polygon("AreaLoad", location)
    
    # Convenience Operations

    def add_point_loads(self, x: List[float], y:List[float], elevation:List[float] = None, Fx:List[float] = None, Fy:List[float] = None, Fz:List[float] = None, Mx:List[float] = None, My:List[float] = None) -> List[PointLoad]:
        """Add a set of :any:`PointLoad` at the given coordinates with the given values. All non-`None` parameters must be Lists of same length.
        `None` values are replaced by zero values."""
        self._operation_raise_if_read_only("add_point_loads()")
        entity_count = len(x)
        if len(y) != entity_count:
            raise Exception("Length of y parameter must be same as length of x parameter.")

        points = [Point2D(x[i], y[i]) for i in range(0,entity_count)]

        # lambda could be used here, but it wouldn't clean up if one of the adds failed
        # point_loads = list(map(lambda x: self.add_point_load(x), points))
        # so we created the _bulk_add method to handle this somewhat generally
        point_loads = self._bulk_add("add_point_load", points)

        try:
            zero_list = [0.0] * entity_count

            _bulk_set(point_loads,"elevation", elevation)
            _bulk_set(point_loads,"Fx", Fx or zero_list)
            _bulk_set(point_loads,"Fy", Fy or zero_list)
            _bulk_set(point_loads,"Fz", Fz or zero_list)
            _bulk_set(point_loads,"Mx", Mx or zero_list)
            _bulk_set(point_loads,"My", My or zero_list)
        except Exception:
            # if setting isn't successful, the entire method is undone
            for point_load in point_loads:
                point_load.delete()
            raise

        return point_loads


    # LoadingLayer OVERRIDES

    # this needs to be overridden whereever deletion is not available
    def delete(self) -> None:
        """Removes this `ForceLoadingLayer` from the :any:`Model`.
        
        An Exception will be raised if this `ForceLoadingLayer` is read-only.
        """
        self._operation_raise_if_read_only("delete()")
        self._delete()
    